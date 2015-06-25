
import pytz
import os
import math
import numpy
import scipy
import scipy.special
import itertools


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.ion()

def etas_prob_test(r0=500, p_min=.01, p_max=1.5, p_step=.01, t0=0., t1=0., t2=1000., dt2=1.):
	#
	# trying to figure out how to calc an event probability from observed etas rates.
	# start with etas; assume p>1, and a Non-homogeneous Poisson Process (NHPP).
	# so, P = 1 - exp(ingegral[r(t)] ), and r(t) is Omoir.
	#
	# in principle, we get R = int(r) = r0*(p-1)*[t0 + t2]**(1-p) - (t0+t1)**(1-p)]
	# and the idea will be to assume t1=0 and t0 -> 0,
	# so
	# R -> r0*(p-1)*t2^(1-p)
	#
	
	f=plt.figure(0)
	plt.clf()
	ax3d = f.add_subplot(111, projection='3d')
	#
	X = numpy.arange(.001, t2, dt2)
	Y = numpy.arange(p_min, p_max, p_step)
	#Z = R_omori(r0=r0, p=Y, t0=t0, t1=0., t2=X)
	#
	XYZ = [[x,y,R_omori(r0=r0,p=y, t0=t0, t1=0.,t2=x)] for x,y in itertools.product(X,Y)]
	
	# let's do R(p,t)
	
	ax3d.plot(zip(*XYZ)[0],zip(*XYZ)[1], zip(*XYZ)[2],  '.')
	ax3d.set_xlabel('time $t$')
	ax3d.set_ylabel('Omori scaling exponent $p$')
	ax3d.set_zlabel('Integrated Omori Rate $R$')
	#
	#
	f2=plt.figure(1)
	plt.clf()
	ax3d2 = f2.add_subplot(111, projection='3d')
	XYZ = [[x,y,poisson_cum_R(r0=r0,p=y, t0=t0, t1=0.,t2=x)] for x,y in itertools.product(X,Y)]
	
	# let's do R(p,t)
	
	ax3d2.plot(zip(*XYZ)[0],zip(*XYZ)[1], zip(*XYZ)[2],  '.')
	ax3d2.set_xlabel('time $t$')
	ax3d2.set_ylabel('Omori scaling exponent $p$')
	ax3d2.set_zlabel('Poisson Probability based on $R$')
#
def basic_exp_prob(t, t1=0.0, r=1.0):
	'''
	# basic exponential (Poisson, k=1) probability.
	# t is the independent variable, t1 is the initial time (value of the ind. variable), r is the rate, so P = exp(-r*t1) - exp(-r*t2)
	'''
	#
	return exp(-r*t1) - exp(-r*t2)

def omori_prob(t2, t1=0., t0=1., tau=1., p=1.0, c=None):
	# note: the NHHP solution for Omori over time interval t -> t+\Delta t is (for p=1, so int(f) = ln(f):
	# F(\Delta t, t) = ( (c + t + \Delta t)/(c + t) ) ** (-c/\tau)
	# and c = t_0, tau' = tau*t_0**p  (aka, initial interval or rate or whatever).
	# if c is given, assume the (1+t/c) format:
	if c!=None:
		t0=c
		tau *= t**(-p)
	#
	if p==1.0:
		# use logarithmic value:
		F = ((t0 + t2 + (t2-t1))/(t0+t))**(1./tau)
	elif p!=1.0:
		F = numpy.exp(-((t0 + t2)**(1.-p) - (t0+t1)**(1.-p))/(tau*(p-1)))
	#
	return 1.0-F

##################
# modifications to rate/spatial density to account for large aftershocks falling outside the rupture area. eventually, this will require some sort of
# renormalization... or maybe just normalization, to not get into an argument about language.
def f_omori_exp(x, x1=1.0, x0=1.0, chi=1.0, q=1.5):
	'''
	# probability density of omori-exponential distribution
	# x1: exponential factor (exp(-x/x1))
	# x0: omori factor (1/(x0+x))
	# omori function is:
	# f_omori = (1/chi)(x0 + x)**-q
	'''
	#
	f_in =  lambda r: 1.0 - numpy.exp(-r/x1)
	f_out = lambda r: ((x0 + r)**(-q))/chi
	f = lambda r: f_in(r)*f_out(r)
	#
	return f(numpy.array(x))

def F_omori_exp(x, x1=1.0, x0=1.0, chi=1.0, q=1.5):
	'''
	# cumulative omori-exponential (aka, integrated f_omori_exp)
	#  - number of events in an omori-exponential process, probably used for Non-homogeneous Poisson calculations.
	#  - this might warrant some cleaning up, namely to include an x1, x_final range, so we don't always integrate from zero.
	#
	# probability density of omori-exponential distribution
	# x1: exponential factor (exp(-x/x1))
	# x0: omori factor (1/(x0+x))
	# omori function is:
	# f_omori = (1/chi)(x0 + x)**-q
	'''
	#
	if not hasattr(x, '__len__'): x=numpy.array([x])
	# for readability, break this out in components, then return product... or comment and combine.
	f1 = ((x0 + x)**(-q))/(chi*(q-1.0))
	f2 = (q-1.0)*x1*math.exp(x0/x1)*(((x0+x)**q)/x1)
	f3 = scipy.special.gamma((1.0-q), (x0+x)/x1)
	#
	f_diff = ((x0)**(-q))/(chi*(q-1.0)) * ((q-1.0)*x1*math.exp(x0/x1)*(((x0)**q)/x1)*scipy.special.gamma(1.0-q, numpy.array([x0/x1])) - x0 )
	#
	return f1*(f2*f3 - x0 - x) - f_diff
	#return f1*(f2*f3 - x0 - x)

def big_mag_distribution(r0=1.0, r1=1.0, chi=1.0, q=1.5, r_min=0., r_max=100., nits=1000, fnum=0, x_scale='log', y_scale='log'):
	'''
	# plots for "Big aftershocks are farther away" distribution 
	'''
	f_in =  lambda r: 1.0 - numpy.exp(-r/r1)
	f_out = lambda r: ((r0 + r)**(-q))/chi
	f = lambda r: f_in(r)*f_out(r)
	#
	X = numpy.arange(r_min, r_max, float(r_max)/float(nits))
	plt.figure(fnum)
	plt.clf()
	ax=plt.gca()
	#
	ax.set_yscale(x_scale)
	ax.set_xscale(y_scale)
	#
	ax.plot(X, f_in(X), '-', label='exponential P')
	ax.plot(X, f_out(X), '-', label='Omori')
	ax.plot(X, f(X), label='product')
	plt.legend(loc=0, numpoints=1)
	#
	

def R_omori(r0=0., p=1.1, t0=0., t1=0., t2=0.):
	# these throwing errors because 0.0 cannot be raised to negative power, so just trap this case.
	#return r0*(p-1.)*((t0+t2)**(1.-p) - (t0+t1)**(1.-p))
	return r0*(p-1.)*( ((t0+t2) if (t0+t2)!=0.0 else 1e-10)**(1.-p) - (((t0+t1) if (t0+t1)!=0.0 else 1e-10)**(1.-p)))

def poisson_cum_R(r0=0., p=1.1, t0=0., t1=0., t2=0.):
	# there's a better way to do this than **locals(), but since we've not set any variables yet, it will work.
	return 1.0 - numpy.exp(R_omori(**locals()))
