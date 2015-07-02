import math
import pylab as plt
import numpy
import scipy.optimize as spo

def fibo(n_start=1, n_stop=10):
	fibos=[0,1]
	#
	while len(fibos)<(n_stop):
		fibos += [fibos[-2]+fibos[-1]]
	return fibos


class Fibos(list):
	#
	def __init__(self, n_0=0, n_1=1,N_stop=15):
		self.n_0 = n_0
		self.n_1 = n_1
		self.N_stop  = N_stop
		#
		#self.append([0,1])
		#for j in xrange(n_stop):
		#	self.append(self[-2]+self[-1])
		self+=self.fibo(n_0=n_0, n_1=n_1, N_stop=N_stop)
		#
	#
	def fibo(self, n_0=0, n_1=1, N_stop=10):
		fibos=[n_0, n_1]
		fibos.sort()
		#
		for j in xrange(N_stop):
			fibos += [fibos[-2]+fibos[-1]]
		return fibos
	#
	def fibo_inv(self, n_1, n_2, N_max=50):
		# inverse fibonacci sequence, starting with the big one.
		seq = sorted([n_1, n_2])
		seq.reverse()
		#
		#while seq[-1]>-10*seq[0]:
		while len(seq)<N_max:
			seq+=[seq[-2]-seq[-1]]
		#
		#
		return seq
	#
	def plot_seq(self, seq=None, log_y=True, log_x=False, fnum=0, alpha=.5, x0=0.):
		#
		if seq==None: seq=self
		#
		plt.figure(0)
		plt.clf()
		ax=plt.gca()
		#
		ax.set_yscale(('log' if log_y else 'linear'))
		ax.set_xscale(('log' if log_x else 'linear'))
		#
		if not hasattr(seq[0], '__len__'): 
			X = range(len(seq))
			Y = seq
		elif len(seq)==2 and len(seq[0])>2:
			X=seq[0]
			Y=seq[1]
		else:
			X,Y=zip(*seq)[0:2]
		#
		# and fit the exponential:
		# pois_fits2 = spo.curve_fit(f_Poisson, numpy.array(X2), numpy.array(Y2), numpy.array([float(len(X2)), 1.0]))
		#exp_fits = spo.curve_fit(lambda x,x0,alpha: numpy.exp(alpha*(x-x0)), numpy.array(X), numpy.array(Y), numpy.array([.5, 0.]))
		#
		#exp_fits = spo.curve_fit(f_lin, numpy.array(X), numpy.array(numpy.log(Y)), numpy.array([1.0,.5, 0.]))
		lin_fits = spo.curve_fit(lambda x,a,x0,alpha: a + alpha*(x-x0), numpy.array(X), numpy.array(numpy.log(Y)), numpy.array([0.0,.5, 0.]))
		a,x0,alpha = lin_fits[0]
		self.fit_a=a
		self.fit_x0=x0
		self.fit_alpha=alpha
		#
		print "fits: A=%f, x0=%f, alpha=%f" % (math.exp(a), x0, alpha)
		#
		Y_fits = numpy.exp(a + alpha*(X-x0))
		print lin_fits
		#alpha, x0 = exp_fits[0]
		#
		plt.plot(X,Y, 'b.-')
		plt.plot(X, Y_fits, 'g--')

def f_exp(x,A,x0,alpha):
	return A*numpy.exp(alpha*(x-x0))

def doit(N_stop=15):
	F=Fibos(n_0=0, n_1=1, N_stop=N_stop)
	F.plot_seq()
	#
	return F
#
def fiborator(l_fibo=[0,1], fibo_len=10):
	# fibonacci iterator style:
	l_fibo += [l_fibo[-2]+l_fibo[-1]]
	# note this is recursive, but not a nested recursion
	while len(l_fibo)<fibo_len:
		l_fibo=fiborator(l_fibo=l_fibo, fibo_len=fibo_len)
	return l_fibo

def nested_fibo(N_fibo=10):
	# nested fibonacci sequence -- fibonacci within fibonacci.
	# for now, assume a complete fibonacci sequence starting with 0,1,1 or 1,1. fundamentally, we start at 2.	
	#
	fibo_seed=Fibos(n_0=1, n_1=1, N_stop=N_fibo)
	#print "fibo_seed: ", fibo_seed
	fibo_index = {k:f for k,f in enumerate(fibo_seed)}
	fibo_index_l = [[k,f] for k,f in enumerate(fibo_seed)]
	#
	#seed_index = fibo_seed.index(3)		# should be 3 or 4.
	#seed_index_0 = fibo_seed.index(1)
	seed_index=2
	#seed_index=seed_index_0
	#
	#fibo_index = {j:x for j,x in enumerate(F)}
	#return fibo_index
	#
	#nested_fibos = [0,1]
	nested_fibos = [[0,1], [1,1]]	#[key,val] pairs.
	#
	#for k,f in enumerate(nested_fibos[1:]):
	k=len(nested_fibos)
	while True:
		# append any lesser sequences.
		#nested_fibos += fibo_seed[0:seed_index+1]
		nested_fibos += [rw for rw in fibo_index_l if rw[0]<nested_fibos[-1][0]]
		#
		if seed_index<len(fibo_seed):
			nested_fibos += [fibo_index_l[seed_index]]
			seed_index+=1
		#
		k+=1
		if k>len(nested_fibos): break
	
	return nested_fibos

def plot_nested_fibo(N_fibo=10, fignum=0, x_scale='linear', y_scale='linear'):
	numbers = nested_fibo(N_fibo)
	indices, Ns = zip(*numbers)
	countses = {x:Ns.count(x) for x in Ns}
	
	#return countses
	
	X,Y = zip(*sorted([rw for rw in countses.iteritems()], key=lambda x: x[0]))
	#
	#
	#Y_sum = [sum(Y) - sum(Y[0:j+1]) for y,j in enumerate(Y)]
	Y_sum = []
	for j in xrange(len(Y)):
		Y_sum+=[sum(Y[j:])]
	
	print "Y's: ", Y_sum, Y
	
	plt.figure(fignum)
	plt.clf()
	ax = plt.gca()
	#ax2 = ax.twinx()
	ax.set_xscale(x_scale)
	ax.set_yscale(y_scale)
	ax.plot(X,Y, '.-')
	#
	plt.figure(fignum+1)
	ax2 = plt.gca()
	ax2.set_yscale(y_scale)
	ax2.set_xscale(x_scale)
	ax2.plot(X,Y_sum, 'g.-')
	ax.set_xlabel('Fibonacci number $N_f$')
	ax.set_ylabel('Count $N$ (pdf)')
	ax2.set_ylabel('count $N$, cumulative')
	
		

if __name__=='__main__':
	pass
else:
	plt.ion()