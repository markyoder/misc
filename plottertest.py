import matplotlib.pyplot as plt
import math
import scipy

def plotme(L=1000.0, dL=10.0, bumpfact=2.0, rimfact=2.0, tau=1.0, t0=1.0, p=1.1):
	#
	X=scipy.arange(float(L))/float(dL)
	oneses=scipy.ones(L)
	Y=map(omori, X, oneses*tau, oneses*t0, oneses*p)
	Y1=map(omori1, X, oneses*tau, oneses*t0, oneses*p, oneses*bumpfact, oneses*rimfact)
	#
	plt.figure(0)
	plt.clf()
	plt.ion()
	#
	plt.plot(X,Y, '-.')
	plt.plot(X,Y1, '--')
	
	plt.figure(1)
	plt.clf()
	plt.ion()
	#
	plt.loglog(X,Y, '-.')
	plt.loglog(X,Y1, '--')

def omori(x,tau=1.0, t0=1.0, p=1.1):
	yomori = (1.0/(tau * (t0 + x)**p))
	#
	return yomori	


def omori1(x,tau=1.0, t0=1.0, p=1.1, bumpfact=3.0, rimfact=2.0):
	#yomori = (1.0/(tau * (t0 + x)**p))*math.exp(-((x-t0)**2.0)/(x*x))
	t0prime=rimfact*t0
	yomori = (1.0/(tau * (t0 + x)**p))*math.exp((bumpfact*(x-t0prime))/(x + t0prime))
	#
	return yomori
	
