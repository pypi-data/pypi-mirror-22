#ifndef __POISSON_SOLVER_C__
#define __POISSON_SOLVER_C__

#ifdef POND_OMP
#include <omp.h>
#endif
#include "proto.h"

// ----------------------- CG Utility -----------------------------------
float _scalarProduct(float* p, float* r, int n)
{
  float prod = 0.0;
#ifdef POND_OMP
#pragma omp parallel for reduction(+:prod)
#endif
  for(int i=0; i<n; i++)
    {
      prod += p[i]*r[i];
    }
  return prod;
}


void _add(float* res, float* a, float* b, float alpha, int n)
{
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n; i++)
    {
      res[i] = a[i] + alpha*b[i];
    }
}

void _copy(float* a, float* b, int n)
{
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n; i++)
    {
      a[i] = b[i];
    }

}

void _set0(float* a, int n)
{
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n; i++)
    {
      a[i] = 0.0;
    }

}

void _mutliply(float* a, float coef, int n)
{
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n; i++)
    {
      a[i] *= coef;
    }
 
}

// ------------------------------ 1D ----------------------------------------

void _poissonSolver1D(PyArrayObject* rho, PyArrayObject* phi, int* n, float h)
{
  float h2 = h*h;
  // lu decomposition
  // first linear system
  (*(float*)PyArray_GETPTR1(phi,0)) =
    -h2*(*(float*)PyArray_GETPTR1(rho,0))*sqrt(1.0/2.0);

  for(int i=1; i<n[0]; i++)
    {
      (*(float*)PyArray_GETPTR1(phi,i)) =
	(-h2*(*(float*)PyArray_GETPTR1(rho,i)) +
	 (*(float*)PyArray_GETPTR1(phi,i-1))*sqrt((i+1.0)/(i+2.0))) *
	sqrt((float)i /(i+1.0));
    }

  // second linear system
  (*(float*)PyArray_GETPTR1(phi,n[0]-1)) *=
    sqrt((float)n[0]/(n[0]+1.0));

  for(int i=n[0]-2; i >= 0; i--)
    {
      (*(float*)PyArray_GETPTR1(phi,i)) =
	((*(float*)PyArray_GETPTR1(phi,i)) +
	 (*(float*)PyArray_GETPTR1(phi,i+1))*sqrt((i+1.0)/(i+2.0))) *
	sqrt((i+1.0) /(i+2.0));
    }
}

// --------------------------- SSOR 1D -----------------------------

float _rAp1D(float* r, float* p, int* n)
{
  float prod = 0.0;
#ifdef POND_OMP
#pragma omp parallel for reduction(+:prod)
#endif
  for(int i=0; i<n[0]; i++)
    {
      float Ap_i;
      Ap_i = -2.0*p[i];
      if (i != 0)
	Ap_i += p[i-1];
      if (i != n[0]-1)
	Ap_i += p[i+1];
      prod += r[i]*Ap_i;
    }
  return prod;
}

void _addAp1D(float* res, float* a, float* p, float alpha, int* n)
{
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n[0]; i++)
    {
      float Ap_i;
      Ap_i = -2.0*p[i];
      if (i != 0)
	Ap_i += p[i-1];
      if (i != n[0]-1)
	Ap_i += p[i+1];
      res[i] = a[i] + alpha*Ap_i;
    }
}

void _solvePreconditioner1D(float* res, float* a, int n)
{
  // SOR coefficient
  float omega = 2.0;
  // b0 is the component along the main diagonal
  float invb0 = 1.0-1.5*omega;
  // inverse it
  invb0 = 1.0/invb0;
  // b1 is the component outside the main diagonal
  float b1 = omega;
  // solving (I + w*E)*res = a
  // where I is the identity
  // A = E+I+F, with F=E^T
  res[0] = a[0]*invb0;
  for(int i=1; i<n; i++)
    {
      res[i] = (a[i] - b1*res[i-1]) * invb0;
    }
  // solving (I + w*F)*res = res_prev
  res[n-1] = res[n-1]*invb0;
  for(int i=n-2; i>=0; i--)
    {
      res[i] = (res[i] - b1*res[i+1]) * invb0;
    }
}

void _poissonSolverSSOR1D(PyArrayObject* rho,
			  PyArrayObject* phi,
			  int* n,
			  float* h)
{
  /* Algorithm defined in 
   * "A 3-D finite-difference algorithm for DC resistivity
   * modelling using conjugate gradient methods"
   * Naming convention following wikipedia: conjugate gradient method
   * Wikipedia names seems clearer
   */
  float rho_norm = _scalarProduct(
      (float*) rho->data,(float*) rho->data, n[0]);
  float alpha;
  float beta;
  float rsold = 1.0;
  float rsnew;
  // residual
  float* r = (float*) malloc(n[0]*sizeof(float));
  // direction
  float* p = (float*) malloc(n[0]*sizeof(float));
  float* z = (float*) malloc(n[0]*sizeof(float));

  _addAp1D(r,(float*)rho->data,(float*)phi->data,-1.0,n);
  _set0(p,n[0]);
  // loop variables
  int step = 0;
  int test = 1;
  do
    {
      step += 1;
      // Mz = r
      _solvePreconditioner1D(z,r,n[0]);
      // rs = r*z
      rsnew = _scalarProduct(r,z,n[0]);
      // beta = rs_{i-1} / rs_{i}
      beta = rsnew / rsold;
      // p = z + beta*p
      _add(p,z,p,beta, n[0]);
      // alpha = r*z/(p*A*p)
      alpha = rsnew/_rAp1D(p,p,n);
      // r = r - alpha*A*p
      _addAp1D(r, r, p, -alpha, n);
      // x = x + alpha*p
      _add((float*)phi->data, (float*)phi->data, p, alpha, n[0]);
      
      rsold = rsnew;
      // check if convergence is reached
      _addAp1D(z, (float *)rho->data, (float*)phi->data, -1, n);
      rsnew = _scalarProduct(z,z,n[0]);
      if (sqrt(rsnew) < 1e-6*rho_norm)
	{
	  test = 0;
	  printf("Convergence reached in %i steps\n", step);
	}
    } while (step < 1e6 && test);
  if (test)
    {
      printf("WARNING: SSOR did not converge well enough! Error: %g\n", sqrt(rsnew)/rho_norm);
    }  
  free(p);
  free(r);
  _mutliply((float*)phi->data, h[0]*h[0],n[0]);
}


void _poissonSolverFourier1D(PyArrayObject* frho, int* n,
			     float* l)
{
  (*(npy_complex128*)PyArray_GETPTR1(frho,0)).real = 0.0;
  (*(npy_complex128*)PyArray_GETPTR1(frho,0)).imag = 0.0;
#ifdef POND_OMP
  #pragma omp parallel for
#endif
  for(int i=1; i<n[0]/2 + 1; i++)
    {
      float fx2 = 2*i*M_PI/l[0];
      fx2 *= fx2;
      (*(npy_complex128*)PyArray_GETPTR1(frho,i)).real /= -fx2;
      (*(npy_complex128*)PyArray_GETPTR1(frho,i)).imag /= -fx2;
    }
}


//------------------------ 2D ---------------------------------

void _poissonSolverFourier2D(PyArrayObject* frho, int* n,
			     float* l)
{
  int N = n[1]/2 + 1;

  (*(npy_complex128*)PyArray_GETPTR2(frho,0,0)).real = 0.0;
  (*(npy_complex128*)PyArray_GETPTR2(frho,0,0)).imag = 0.0;
#ifdef POND_OMP
  #pragma omp parallel for
#endif
  for(int i=0; i<n[0]; i++)
    {
      for(int j=0; j<N; j++)
	{
	  if (i!=0 || j!=0)
	    {
	      int i_corr = i;
	      if (i>n[0]/2)
		{
		  i_corr -= n[0];
		}
	      float fx2 = 2*i_corr*M_PI/l[0];
	      fx2 *= fx2;
	      float fy2 = 2*j*M_PI/l[1];
	      fy2 *= fy2;
	      
	      (*(npy_complex128*)PyArray_GETPTR2(frho,i,j)).real /= 
		-(fx2+fy2);

	      (*(npy_complex128*)PyArray_GETPTR2(frho,i,j)).imag /= 
		-(fx2+fy2);
	    }
	}
    }
}

//----------------------------- CG 2D -------------------------
/*
float _rAp2D(float* r, float* p, float* h, int* n)
{
  // scaling (tmp storing)
  float b0 = 1.0/(h[0]*h[0]) + 1.0/(h[1]*h[1]);
  b0 = 1.0/b0;
  // component x diagonal
  float b1x = b0/(h[0]*h[0]);
  // component y diagonal
  float b1y = b0/(h[1]*h[1]);
  // component main diagonal
  b0 = -2.0;

  float prod = 0.0;
#ifdef POND_OMP
#pragma omp parallel for reduction(+:prod)
#endif
  for(int i=0; i<n[0]; i++)
    {
      for(int j=0; j<n[1]; j++)
	{
	  float Ap_i;
	  Ap_i = p[i*n[1]+j]*b0;
	  if (i != 0)
	    Ap_i += p[(i-1)*n[1]+j]*b1x;
	  if (i != n[0]-1)
	    Ap_i += p[(i+1)*n[1]+j]*b1x;
	  if (j != 0)
	    Ap_i += p[i*n[1]+j-1]*b1y;
	  if (j != n[1]-1)
	    Ap_i += p[i*n[1]+j+1]*b1y;
	  prod += r[i*n[1]+j]*Ap_i;
	}
    }
  return prod;
}

void _addAp2D(float* res, float* a, float* p, float alpha, float* h, int* n)
{
  // scaling (tmp storing)
  float b0 = 1.0/(h[0]*h[0]) + 1.0/(h[1]*h[1]);
  b0 = 1.0/b0;
  // component x diagonal
  float b1x = b0/(h[0]*h[0]);
  // component y diagonal
  float b1y = b0/(h[1]*h[1]);
  // component main diagonal
  b0 = -2.0;
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n[0]; i++)
    {
      for(int j=0; j<n[1]; j++)
	{
	  float Ap_i;
	  Ap_i = p[i*n[1]+j]*b0;
	  if (i != 0)
	    Ap_i += p[(i-1)*n[1]+j]*b1x;
	  if (i != n[0]-1)
	    Ap_i += p[(i+1)*n[1]+j]*b1x;
	  if (j != 0)
	    Ap_i += p[i*n[1]+j-1]*b1y;
	  if (j != n[1]-1)
	    Ap_i += p[i*n[1]+j+1]*b1y;
	  res[i] = a[i*n[1]+j] + alpha*Ap_i;
	}
    }
}

void _solvePreconditioner2D(float* res, float* a, float* h, int* n)
{
  float omega = 2.0;
  // scaling (tmp storing)
  float b0 = 1.0/(h[0]*h[0]) + 1.0/(h[1]*h[1]);
  b0 = 1.0/b0;
  // component x diagonal
  float b1x = b0/(h[0]*h[0]);
  // component y diagonal
  float b1y = b0/(h[1]*h[1]);
  // component main diagonal
  b0 = 1.0-1.5*omega;
  b1x *= omega;
  b1y *= omega;
  float invb0 = 1.0/b0;
  
  // solving (I + w*E)*res = a
  // where I is the identity
  // A = E+I+F, with F=E^T
  res[0] = a[0]*invb0;
  for(int j=1; j<n[1]; j++)
    {
      res[j] = (a[j] - b1y*res[j-1]) * invb0;
    }
  for(int i=1; i<n[0]; i++)
    {
      int ind = i*n[1];
      res[ind] = (a[ind] - b1x*res[ind-n[1]]) * invb0;
      for(int j=1; j<n[1]; j++)
	{
	  ind = i*n[1] + j;
	  res[ind] = (a[ind] - b1y*res[ind-1] - b1x*res[ind-n[1]]) * invb0;
	}
    }

  
  // solving (I + w*F)*res = res_prev
  int N = n[0]*n[1];
  res[N-1] = a[N-1]*invb0;
  for(int j=n[1]-2; j>=0; j--)
    {
      int ind = (n[0]-1)*n[1] + j;
      res[ind] = (a[ind] - b1y*res[ind+1]) * invb0;
    }
  for(int i=n[0]-2; i>=0; i--)
    {
      int ind = (i+1)*n[1]-1;
      res[ind] = (a[ind] - b1x*res[ind+n[1]])*invb0;
      for(int j=n[1]-2; j>=0; j--)
	{
	  ind = i*n[1] + j;
	  res[ind] = (a[ind] - b1y*res[ind+1] - b1x*res[ind+n[1]]) * invb0;
	}
    }
}


void _poissonSolverSSOR2D(PyArrayObject* rho,
			  PyArrayObject* phi,
			  int* n,
			  float* h)
{

  int N = n[0]*n[1];
  float rho_norm = _scalarProduct(
      (float*) rho->data,(float*) rho->data, N);
  float alpha;
  float beta;
  float rsold = 1.0;
  float rsnew;
  // residual
  float* r = (float*) malloc(N*sizeof(float));
  // direction
  float* p = (float*) malloc(N*sizeof(float));
  float* z = (float*) malloc(N*sizeof(float));

  _addAp2D(r,(float*)rho->data,(float*)phi->data,-1.0,h,n);
  _set0(p,N);
  // loop variables
  int step = 0;
  int test = 1;
  do
    {
      step += 1;
      // Mz = r
      _solvePreconditioner2D(z,r,h,n);
      // rs = r*z
      rsnew = _scalarProduct(r,z,N);
      // beta = rs_{i-1} / rs_{i}
      beta = rsnew / rsold;
      // p = z + beta*p
      _add(p,z,p,beta, N);
      // alpha = r*z/(p*A*p)
      alpha = rsnew/_rAp2D(p,p,h,n);
      // r = r - alpha*A*p
      _addAp2D(r, r, p, -alpha, h, n);
      // x = x + alpha*p
      _add((float*)phi->data, (float*)phi->data, p, alpha, N);
      
      rsold = rsnew;
      // check if convergence is reached
      _addAp2D(z, (float *)rho->data, p, -1, h, n);
      rsnew = _scalarProduct(z,z,N);
      if (sqrt(rsnew) < 1e-6*rho_norm)
	{
	  test = 0;
	  printf("Convergence reached in %i steps\n", step);
	}
    } while (step < 1e5 && test);
  if (test)
    {
      printf("WARNING: SSOR did not converge well enough! Error: %g\n", sqrt(rsnew)/rho_norm);
    }  
  free(p);
  free(r);
  alpha = 1.0/(h[0]*h[0]) + 1.0/(h[1]*h[1]);
  _mutliply((float*)phi->data, 1.0/alpha,N);
}


//----------------------------- 3D ----------------------------
*/
void _poissonSolverFourier3D(PyArrayObject* frho, int* n,
			     float* l)
{
  int nz = n[2]/2 + 1;

  (*(npy_complex128*)PyArray_GETPTR3(frho,0,0,0)).real = 0.0;
  (*(npy_complex128*)PyArray_GETPTR3(frho,0,0,0)).imag = 0.0;
#ifdef POND_OMP
  #pragma omp parallel for
#endif
  for(int i=0; i<n[0]; i++)
    {
      for(int j=0; j<n[1]; j++)
	{
	  for(int k=0; k<nz; k++)
	    {
	      if (i!=0 || j!=0 || k!=0)
		{
		  int i_corr = i;
		  if (i>n[0]/2)
		    {
		      i_corr -= n[0];
		    }
		  int j_corr = j;
		  if (j>n[1]/2)
		    {
		      j_corr -= n[1];
		    }
		  float fx2 = 2*i_corr*M_PI/l[0];
		  fx2 *= fx2;
		  float fy2 = 2*j_corr*M_PI/l[1];
		  fy2 *= fy2;
		  float fz2 = 2*k*M_PI/l[2];
		  fz2 *= fz2;
		  
		  (*(npy_complex128*)PyArray_GETPTR3(frho,i,j,k)).real /=
		    -(fx2+fy2+fz2);
		  
		  (*(npy_complex128*)PyArray_GETPTR3(frho,i,j,k)).imag /=
		    -(fx2+fy2+fz2);

		}
	    }
	}
    }
}

//----------------------------- CG 3D -------------------------
/*
float _rAp3D(float* r, float* p, float* invh2, int* n)
{
  float prod = 0.0;
#ifdef POND_OMP
#pragma omp parallel for reduction(+:prod)
#endif
  for(int i=0; i<n[0]; i++)
    {
      for(int j=0; j<n[1]; j++)
	{
	  float Ap_i;
	  Ap_i = -2.0*p[i*n[1]+j]*(invh2[0]+invh2[1]);
	  if (i != 0)
	    Ap_i += p[(i-1)*n[1]+j]*invh2[0];
	  if (i != n[0]-1)
	    Ap_i += p[(i+1)*n[1]+j]*invh2[0];
	  if (j != 0)
	    Ap_i += p[i*n[1]+j-1]*invh2[1];
	  if (j != n[1]-1)
	    Ap_i += p[i*n[1]+j+1]*invh2[1];
	  prod += r[i*n[1]+j]*Ap_i;
	}
    }
  return prod;
}

void _addAp3D(float* res, float* a, float* p, float alpha, float* invh2, int* n)
{
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n[0]; i++)
    {
      for(int j=0; j<n[1]; j++)
	{
	  float Ap_i;
	  Ap_i = -2.0*p[i*n[1]+j]*(invh2[0]+invh2[1]);
	  if (i != 0)
	    Ap_i += p[(i-1)*n[1]+j]*invh2[0];
	  if (i != n[0]-1)
	    Ap_i += p[(i+1)*n[1]+j]*invh2[0];
	  if (j != 0)
	    Ap_i += p[i*n[1]+j-1]*invh2[1];
	  if (j != n[1]-1)
	    Ap_i += p[i*n[1]+j+1]*invh2[1];
	  res[i] = a[i*n[1]+j] + alpha*Ap_i;
	}
    }
}


void _solvePreconditioner3D(float* res, float* a, float h2, int* n)
{
#ifdef POND_OMP
#pragma omp parallel for
#endif
  for(int i=0; i<n[0]; i++)
    {
      for(int j=0; j<n[1]; j++)
	{
	  res[i*n[1]+j] = 0.5*a[i*n[1]+j]*h2;
	}
    }
  
}

void _poissonSolverSSOR3D(PyArrayObject* rho,
			PyArrayObject* phi,
			int* n,
			float* h)
{
  printf("Still need to write it!");
  float* invh2 = (float*) malloc(rho->nd*sizeof(float));
  for(int i=0; i<rho->nd; i++)
    invh2[i] = 1.0/(h[i]*h[i]);
  float alpha;
  float beta;
  float rsold;
  int N = n[0]*n[1]*n[2];
  // residual
  float* r = (float*) malloc(N*sizeof(float));
  // direction
  float* p = (float*) malloc(N*sizeof(float));

  _addAp3D(r,(float*)rho->data,(float*)phi->data,-1.0,invh2,n);
  _copy(p,r,N);
  rsold = _scalarProduct(r,r,N);
  
  // loop variables
  int step = 0;
  int test = 1;
  float rsnew;
  do
    {
      step += 1;
      // alpha = r*r/(p*A*p)
      alpha = rsold/_rAp3D(p,p,invh2,n);
      // x = x + alpha*p
      _add((float*)phi->data, (float*)phi->data, p, alpha, N);
      // r = r - alpha*A*p
      _addAp3D(r, r, p, -alpha, invh2, n);
      // r*r
      rsnew = _scalarProduct(r,r,N);
      if (rsnew < 1e-10)
	{
	  test = 0;
	  printf("Convergence reached\n");
	  break;
	}
      beta = rsnew / rsold;
      // p = r + beta*p
      _add(p,r,p,beta, N);
      rsold = rsnew;
    } while (step < 1e6);
  if (test)
    {
      printf("WARNING: CG did not converge well enough! Error: %g\n", rsold);
    }  
  free(p);
  free(r);
  free(invh2);
}
*/
#endif //__POISSON_SOLVER_C__
