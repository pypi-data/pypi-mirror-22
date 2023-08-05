#include "proto.h"

// Declare an error
static PyObject *PySolverToolsError;

static PyObject* poissonSolver(PyObject* self, PyObject* args)
{

  // --------------- LOAD OBJECT --------------
  // length of the system
  PyTupleObject* l_tuple = NULL; // (lx, ly, lz)
  PyArrayObject* rho = NULL; // rho[x,y,z]: input
  PyArrayObject* phi = NULL; // phi[x,y,z]: output
  // periodic boundaries
  int periodic = 1;
  
  if (!PyArg_ParseTuple(args, "OO|ii:poissonSolver", &rho, &l_tuple,
			&periodic))
    return NULL;

  if (rho->nd < 1 || rho->descr->type_num != PyArray_FLOAT) {
    PyErr_SetString(PySolverToolsError,
        "argument 1 must be at least one dimentionnal and of type float32");
    return NULL;
  }

  if (!PyTuple_Check(l_tuple))
    {
      PyErr_SetString(PySolverToolsError,"Expect a tuple as second argument");
      return NULL;
    }

  // ---------- COMPUTE SECONDARY VARIABLES ---

  // compute dimension of the system

  // set n
  int* n = (int*) malloc(rho->nd*sizeof(int));
  for(int i=0; i < rho->nd; i++)
    {
      n[i] = rho->dimensions[i];
    }

  // length of the system
  float* l = (float*) malloc(rho->nd*sizeof(float));
  PyObject *iter = NULL;
  iter = PyObject_GetIter(l_tuple);
  for(int i=0; i < rho->nd; i++)
    {
      // copy the length value
      PyObject *next = PyIter_Next(iter);  
      l[i] = (float) PyFloat_AsDouble(next);
      Py_DECREF(next); next = NULL;
    }

  // -------------- SOLVE POISSON ----------------

  phi = _poissonSolver(rho, n, l, periodic);

  // free memory
  Py_DECREF(iter); iter = NULL;
  free(l); l = NULL;
  free(n); n = NULL;
  return phi;
  
}

PyArrayObject* _poissonSolver(PyArrayObject* rho, int* n,
			      float* l, int periodic)
{

  PyArrayObject* phi = NULL; // solution
  PyArrayObject* tmp = NULL; // swap pointers
  PyTupleObject* tmp_tuple = NULL; // swap pointers

  // deal with all the possible cases
  if (rho->nd==1 && !periodic) // LU decomposition
    {
      // change type of n
      npy_intp* dims = (npy_intp*) malloc(sizeof(npy_intp));
      dims[0] = n[0];
      // create array phi
      PyArray_Descr* descr = PyArray_DescrFromType(NPY_FLOAT32);
      phi = PyArray_Zeros(1,dims,descr,0);

      // compute discretization step
      float h = l[0]/(n[0]-1.0);
      // solve poisson
      _poissonSolver1D(rho, phi, n, h);

      // free memory
      free(dims); dims = NULL;
    }
  /*else if (!periodic) // Conjugate Gradient method
    {
      npy_intp* dims = (npy_intp*) malloc(rho->nd*sizeof(npy_intp));
      float* h = (float*) malloc(rho->nd*sizeof(float));
      for(int i=0; i<rho->nd; i++)
	{
	  h[i] = l[i]/(n[i]-1.0);
	  dims[i] = n[i];
	}
      PyArray_Descr* descr = PyArray_DescrFromType(NPY_FLOAT32);
      phi = PyArray_Zeros(rho->nd,dims,descr,0);

      if (rho->nd == 1)
	{
	  // kept for testing
	  _poissonSolverSSOR1D(rho, phi, n, h);
	}
      else if (rho->nd == 2)
	{
	  _poissonSolverSSOR2D(rho, phi, n, h);
	}
      else if (rho->nd == 3)
	{
	  _poissonSolverSSOR3D(rho, phi, n, h);
	}

	}*/
  else // FFT method
    {
      // ------------- LOAD NUMPY FUNCTION -----------
      PyObject *pName, *pModule, *prfftn, *pirfftn;
      // shape of the final object
      PyTupleObject *shape = PyList_New(rho->nd);

      pName = PyString_FromString("numpy.fft");      
      // Load the module object
      pModule = PyImport_Import(pName);

      // get numpy function
      prfftn = PyObject_GetAttrString(pModule,"rfftn");
      pirfftn = PyObject_GetAttrString(pModule,"irfftn");


      // FFT
      tmp_tuple = PyTuple_Pack(1, rho);
      tmp = PyObject_CallObject(prfftn, tmp_tuple);

      Py_DECREF(tmp_tuple); tmp_tuple = NULL;
      // shape of the final object
      for(int i=0; i<rho->nd; i++) {
	long int a = n[i];
	PyList_SetItem(shape, i, PyInt_FromLong(a));
      }
      // dimension specific resolution (maybe can generalize?)
      if (rho->nd==1)
	{
	  _poissonSolverFourier1D(tmp, n, l);
	}
      else if (rho->nd==2)
	{
	  _poissonSolverFourier2D(tmp, n, l);
	}
      else if (rho->nd==3)
	{
	  _poissonSolverFourier3D(tmp, n, l);
	}

      // IFFT
      tmp_tuple = PyTuple_Pack(2, tmp, shape);
      phi = PyObject_CallObject(pirfftn, tmp_tuple);

      Py_DECREF(tmp);       tmp = NULL;
      Py_DECREF(tmp_tuple); tmp_tuple = NULL;

      Py_DECREF(pName);     pName = NULL;
      Py_DECREF(pModule);   pModule = NULL;
      Py_DECREF(prfftn);    prfftn = NULL;
      Py_DECREF(pirfftn);   pirfftn = NULL;
      Py_DECREF(shape);     shape = NULL;
    }
  return phi;
}

//-------------------- DEPOSIT ----------------------------

static PyObject* deposit(PyObject* self, PyObject* args)
{

  // --------------- LOAD OBJECT --------------
  PyTupleObject* ori_tuple = NULL; // (Ox, Oy, Oz)
  PyTupleObject* l_tuple = NULL; // (lx, ly, lz)
  PyTupleObject* n_tuple = NULL; // (Nx, Ny, Nz)
  PyArrayObject* pos = NULL; // pos[index,(x,y,z)]: input
  PyArrayObject* weight = NULL; // weight[index]: input
  PyArrayObject* rho = NULL;
  int periodic = 0;
  
  if (!PyArg_ParseTuple(args, "OOOOO|i:desposit", &pos, &weight,
			&ori_tuple, &l_tuple, &n_tuple, &periodic))
    return NULL;
  

  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
    PyErr_SetString(PySolverToolsError,
	"argument 1 must be at least one dimentionnal and of type float32");
    return NULL;
  }

  if (weight->nd != 1 || weight->descr->type_num != PyArray_FLOAT) {
    PyErr_SetString(PySolverToolsError,
        "argument 2 must be at least one dimentionnal and of type float32");
    return NULL;
  }

  // ---------- COMPUTE SECONDARY VARIABLES ---

  
  // compute dimension of the system
  int dim = pos->dimensions[1];

  if (!PyTuple_Check(l_tuple))
    {
      PyErr_SetString(PySolverToolsError,"Expect a tuple for L");
      return NULL;
    }
  if (!PyTuple_Check(n_tuple))
    {
      PyErr_SetString(PySolverToolsError,"Expect a tuple for N");
      return NULL;
    }
  if (!PyTuple_Check(ori_tuple))
    {
      PyErr_SetString(PySolverToolsError,"Expect a tuple for O");
      return NULL;
    }

  // Discretization
  npy_intp* n = (npy_intp*) malloc(dim*sizeof(npy_intp));
  // length of the system
  float* l = (float*) malloc(dim*sizeof(float));
  float* ori = (float*) malloc(dim*sizeof(float));
  PyObject *iter = NULL;
  PyObject *iterN = NULL;
  PyObject *iterO = NULL;
  iter = PyObject_GetIter(l_tuple);
  iterN = PyObject_GetIter(n_tuple);
  iterO = PyObject_GetIter(ori_tuple);

  for(int i=0; i < dim; i++)
    {
      // copy the length value
      PyObject *next = PyIter_Next(iter);
      PyObject *nextN = PyIter_Next(iterN);
      PyObject *nextO = PyIter_Next(iterO);
      if (!PyFloat_Check(next)) {
	PyErr_SetString(PySolverToolsError,"L was expecting a python float");
	return NULL;
      }
      if (!PyInt_Check(nextN)) {
	PyErr_SetString(PySolverToolsError,"N was expecting an int");
	return NULL;
      }
      if (!PyFloat_Check(nextO)) {
	PyErr_SetString(PySolverToolsError,"O was expecting a python float");
	return NULL;
      }
	  
      l[i] = PyFloat_AsDouble(next);
      ori[i] = PyFloat_AsDouble(nextO);
      n[i] = PyInt_AsLong(nextN);
      Py_DECREF(next); next = NULL;
      Py_DECREF(nextN); nextN = NULL;
      Py_DECREF(nextO); nextO = NULL;
    }
  Py_DECREF(iter); iter = NULL;
  Py_DECREF(iterN); iterN = NULL;
  Py_DECREF(iterO); iterO = NULL;
  
  // -------------- Do the deposit ----------------

  // create rho
  PyArray_Descr* descr = PyArray_DescrFromType(NPY_FLOAT32);
  rho = PyArray_Zeros(dim,n,descr,1);

  _deposit(pos, weight, rho, ori, l, n, periodic);

  // free memory
  free(l); l = NULL;
  free(n); n = NULL;
  return PyArray_Return(rho);
  
}


PyArrayObject* _deposit(PyArrayObject* pos,
			PyArrayObject* weight,
			PyArrayObject* rho,
			float* ori,
			float* l,
			npy_intp* n,
			int periodic) {

  // dimension specific resolution (maybe can generalize?)
  if (rho->nd==1)
    {
      _deposit1D(rho, pos, weight, ori, l, n, periodic);
    }
  else if (rho->nd==2)
    {
      _deposit2D(rho, pos, weight, ori, l, n, periodic);
    }
  else if (rho->nd==3)
    {
      _deposit3D(rho, pos, weight, ori, l, n, periodic);
    }
}




static PyMethodDef PySolverToolsMethods[] = {
    {"poissonSolver", poissonSolver, METH_VARARGS,
     "Solve the poisson equation."},
    {"deposit", deposit, METH_VARARGS,
     "Make the deposit."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_pysolvertools(void)
{
  PyObject *m;
  m = Py_InitModule("_pysolvertools", PySolverToolsMethods);
  import_array();
  // first error name
  PySolverToolsError = PyErr_NewException("pysolvertools.error", NULL, NULL);
  Py_INCREF(PySolverToolsError);
  PyModule_AddObject(m, "error", PySolverToolsError);
}
