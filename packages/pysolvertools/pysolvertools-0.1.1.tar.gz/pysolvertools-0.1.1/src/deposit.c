#ifndef __DEPOSIT_C__
#define __DEPOSIT_C__


#include "proto.h"

void _deposit1D(PyArrayObject* rho,
		PyArrayObject* pos,
		PyArrayObject* weight,
		float* ori,
		float* l,
		npy_intp* n,
		int periodic)
{
  float dx = l[0]/(n[0]-1.0);
  for(int i=0; i<pos->dimensions[0]; i++)
    {
      // x coordinate
      // put particle inside box
      int j = ((*(float*)PyArray_GETPTR2(pos,i,0)-ori[0])/l[0]);
      // rounding toward 0 => -1 in order to have -> -infty
      if (*(float*)PyArray_GETPTR2(pos,i,0) < ori[0])
	j -= 1;
      float frac = -j*l[0] + *(float*)PyArray_GETPTR2(pos,i,0)-ori[0];
      // compute coordinate
      frac /= dx;
      j = frac;
      frac -= j;

      // deposit
      *(float*)PyArray_GETPTR1(rho,j) +=
	*(float*)PyArray_GETPTR1(weight,i)*(1.0-frac);

      // deal with periodicity
      //x
      int jx1 = j+1;
      if (jx1 > n[0]-1)
	{
	  if (periodic)
	    jx1 = 0;
	  else
	    jx1 = n[0];
	}
      if (jx1 < n[0])
	{
	  *(float*)PyArray_GETPTR1(rho,jx1) +=
	    *(float*)PyArray_GETPTR1(weight,i)*frac;
	}
    }

}


void _deposit2D(PyArrayObject* rho,
		PyArrayObject* pos,
		PyArrayObject* weight,
		float* ori,
		float* l,
		npy_intp* n,
		int periodic)
{
  float dx = l[0]/(n[0]-1.0);
  float dy = l[1]/(n[1]-1.0);
  for(int i=0; i<pos->dimensions[0]; i++)
    {
      // x coordinate
      // put particle inside box
      int jx = ((*(float*)PyArray_GETPTR2(pos,i,0)-ori[0])/l[0]);
      // rounding toward 0 => -1 in order to have -> -infty
      if (*(float*)PyArray_GETPTR2(pos,i,0) < ori[0])
	jx -= 1;
      float fracx = -jx*l[0] + *(float*)PyArray_GETPTR2(pos,i,0)-ori[0];
      // compute coordinate
      fracx /= dx;
      jx = fracx;
      fracx -= jx;

      // y coordinate
      // put particle inside box
      int jy = ((*(float*)PyArray_GETPTR2(pos,i,1)-ori[1])/l[1]);
      // rounding toward 0 => -1 in order to have -> -infty
      if (*(float*)PyArray_GETPTR2(pos,i,1) < ori[1])
	jy -= 1;
      float fracy = -jy*l[1] + *(float*)PyArray_GETPTR2(pos,i,1)-ori[1];
      // compute coordinate
      fracy /= dy;
      jy = fracy;
      fracy -= jy;
      
      // deal with periodicity
      //x
      int jx1 = jx+1;
      if (jx1 > n[0]-1)
	{
	  if (periodic)
	    jx1 = 0;
	  else
	    jx1 = n[0];
	}
      //y
      int jy1 = jy+1;
      if (jy1 > n[1]-1)
	{
	  if (periodic)
	    jy1 = 0;
	  else
	    jy1 = n[1];
	}

      // deposit
      float* tmp = (float*)PyArray_GETPTR2(rho,jx,jy);
      *tmp +=
	*(float*)PyArray_GETPTR1(weight,i)*(1.0-fracx)*(1.0-fracy);

      if (jx1 < n[0])
	{
	  tmp = (float*)PyArray_GETPTR2(rho,jx1,jy);
	  *tmp +=
	    *(float*)PyArray_GETPTR1(weight,i)*fracx*(1.0-fracy);
	  if (jy1 < n[1])
	    {
	      tmp = (float*)PyArray_GETPTR2(rho,jx,jy1);
	      *tmp +=
		*(float*)PyArray_GETPTR1(weight,i)*(1.0-fracx)*fracy;
	      tmp = (float*)PyArray_GETPTR2(rho,jx1,jy1);
	      *tmp +=
		*(float*)PyArray_GETPTR1(weight,i)*fracx*fracy;
	      
	    }
	}
    }
}


void _deposit3D(PyArrayObject* rho,
		PyArrayObject* pos,
		PyArrayObject* weight,
		float* ori,
		float* l,
		npy_intp* n,
		int periodic)
{
  
  float dx = l[0]/(n[0]-1.0);
  float dy = l[1]/(n[1]-1.0);
  float dz = l[2]/(n[2]-1.0);
  for(int i=0; i<pos->dimensions[0]; i++)
    {
      // x coordinate
      // put particle inside box
      int jx = ((*(float*)PyArray_GETPTR2(pos,i,0)-ori[0])/l[0]);
      // rounding toward 0 => -1 in order to have -> -infty
      if (*(float*)PyArray_GETPTR2(pos,i,0) < ori[0])
	jx -= 1;
      float fracx = -jx*l[0] + *(float*)PyArray_GETPTR2(pos,i,0)-ori[0];
      // compute coordinate
      fracx /= dx;
      jx = fracx;
      fracx -= jx;

      // y coordinate
      // put particle inside box
      int jy = ((*(float*)PyArray_GETPTR2(pos,i,1)-ori[1])/l[1]);
      // rounding toward 0 => -1 in order to have -> -infty
      if (*(float*)PyArray_GETPTR2(pos,i,1) < ori[1])
	jy -= 1;
      float fracy = -jy*l[1] + *(float*)PyArray_GETPTR2(pos,i,1)-ori[1];
      // compute coordinate
      fracy /= dy;
      jy = fracy;
      fracy -= jy;
      
      // z coordinate
      // put particle inside box
      int jz = ((*(float*)PyArray_GETPTR2(pos,i,2)-ori[1])/l[2]);
      // rounding toward 0 => -1 in order to have -> -infty
      if (*(float*)PyArray_GETPTR2(pos,i,2) < ori[1])
	jz -= 1;
      float fracz = -jz*l[2] + *(float*)PyArray_GETPTR2(pos,i,2)-ori[1];
      // compute coordinate
      fracz /= dz;
      jz = fracz;
      fracz -= jz;

      // deal with periodicity
      //x
      int jx1 = jx+1;
      if (jx1 > n[0]-1)
	{
	  if (periodic)
	    jx1 = 0;
	  else
	    jx1 = n[0];
	}
      //y
      int jy1 = jy+1;
      if (jy1 > n[1]-1)
	{
	  if (periodic)
	    jy1 = 0;
	  else
	    jy1 = n[1];
	}
      //z
      int jz1 = jz+1;
      if (jz1 > n[2]-1)
	{
	  if (periodic)
	    jz1 = 0;
	  else
	    jz1 = n[2];
	}
      // deposit
      *(float*)PyArray_GETPTR3(rho,jx,jy,jz) +=
	*(float*)PyArray_GETPTR1(weight,i)*
	(1.0-fracx)*(1.0-fracy)*(1.0-fracz);

      if (jx1 < n[0])
	{
	  *(float*)PyArray_GETPTR3(rho,jx1,jy,jz) +=
	    *(float*)PyArray_GETPTR1(weight,i)*
	    fracx*(1.0-fracy)*(1.0-fracz);
	  if (jy1 < n[1])
	    {
	      *(float*)PyArray_GETPTR3(rho,jx,jy1,jz) +=
		*(float*)PyArray_GETPTR1(weight,i)*
		(1.0-fracx)*fracy*(1.0-fracz);
	      *(float*)PyArray_GETPTR3(rho,jx1,jy1,jz) +=
		*(float*)PyArray_GETPTR1(weight,i)*
		fracx*fracy*(1.0-fracz);
	      if (jz1 < n[2])
		{
		  *(float*)PyArray_GETPTR3(rho,jx,jy,jz1) +=
		    *(float*)PyArray_GETPTR1(weight,i)*
		    (1.0-fracx)*(1.0-fracy)*fracz;
		  *(float*)PyArray_GETPTR3(rho,jx,jy1,jz1) +=
		    *(float*)PyArray_GETPTR1(weight,i)*
		    (1.0-fracx)*fracy*fracz;
		  *(float*)PyArray_GETPTR3(rho,jx1,jy1,jz1) +=
		    *(float*)PyArray_GETPTR1(weight,i)*
		    fracx*fracy*fracz;
		  *(float*)PyArray_GETPTR3(rho,jx1,jy,jz1) +=
		    *(float*)PyArray_GETPTR1(weight,i)*
		    fracx*(1.0-fracy)*fracz;
		}
	    }
	}
    }
}


#endif //__DEPOSIT_C__
