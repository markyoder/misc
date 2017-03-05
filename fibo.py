'''
# Fibonacci sequences are commonly asked about in coding tests. Here are several variations on how to code
# Fibonacci sequence using class structures, data containers, and all that stuff. We also talk a bit about 
# sequences that don't start at 0. whether or not this constitutes a true Fibonacci sequence is an academic
# discussion.
'''

import math
import pylab as plt
import numpy
import scipy.optimize as spo
import matplotlib as mpl
import os

def fibo(n_stop=10, n_start=0, fibo0=0.):
	fibos=[0+fibo0,1+fibo0]
	#
	while len(fibos)<(n_stop):
		fibos += [fibos[-2]+fibos[-1]]
	return fibos[n_start:n_stop]

class Fiborator(object):
	def __init__(self, n_stop=10, n_start=0, fibo0=0):
		self.n_fibo=1
		#
		self.n0 = 0 + fibo0
		self.n1 = 1 + fibo0
		#
		while self.n_fibo<n_stop:
			self.next_fibo
		#
	#
	@property
	def this_fibo(self):
		return self.n1
	#
	@property
	def next_fibo(self):
		next_val = self.n0 + self.n1
		self.n0 = self.n1
		self.n1 = next_val
		self.n_fibo+=1
		#
		return self.n1
	#
	def prev(self,n=1):
		if n==1:
			return self.prev_fibo
		else:
			return [self.prev_fibo for j in range(n)]
	def next(self,n=1):
		if n==1:
			return self.next_fibo
		else:
			return [self.next_fibo for j in range(n)]
		#
	#
	def __repr__(self):
		return str(self.this_fibo)
		
	@property
	def prev_fibo(self):
		if self.n_fibo<=1: return self.n1
		#
		n0 = self.n1-self.n0
		self.n1 = self.n0
		self.n0 = n0
		#
		self.n_fibo-=1
		#
		return self.n1

#
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
		for j in range(N_stop):
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
			X = list(range(len(seq)))
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
		print("fits: A=%f, x0=%f, alpha=%f" % (math.exp(a), x0, alpha))
		#
		Y_fits = numpy.exp(a + alpha*(X-x0))
		print(lin_fits)
		#alpha, x0 = exp_fits[0]
		#
		plt.plot(X,Y, 'b.-')
		plt.plot(X, Y_fits, 'g--')

def fibo_box_sequence(N=10, x_padding=.1, y_padding=.1, clr_0='b', fill_alpha=.6, output_dir='/home/myoder/Dropbox/Research/ACES/China2015/talks/nepal/images'):
	# make some fibo-boxes:
	#
	# first, solid:
	f=fibo_boxes(N=N, x_padding=0., y_padding=0., clr_0=clr_0, fill_alpha=1.0)
	plt.savefig(os.path.join(output_dir, 'fibo_solid.png'))
	#
	# now with borders:
	f=fibo_boxes(N=N, x_padding=0., y_padding=0., clr_0='b', fill_alpha=.6)
	plt.savefig(os.path.join(output_dir, 'fibo_borders.png'))
	#
	#... and splitting...
	f=fibo_boxes(N=N, x_padding=x_padding, y_padding=y_padding, clr_0='b', fill_alpha=.6)
	plt.savefig(os.path.join(output_dir, 'fibo_split_1.png'))
	
	f=fibo_boxes(N=N, x_padding=2.*x_padding, y_padding=2.*y_padding, clr_0='b', fill_alpha=.6)
	plt.savefig(os.path.join(output_dir, 'fibo_split_2.png'))
	
	f=fibo_boxes(N=N, x_padding=x_padding, y_padding=y_padding, clr_0=None, fill_alpha=.6)
	plt.savefig(os.path.join(output_dir, 'fibo_split_colors.png'))
#
def fibo_boxes(N=10, x_padding=0., y_padding=0., clr_0=None, fill_alpha=.6):
	F=Fibos(N_stop=N)
	plt.figure(0)
	plt.clf()
	#
	colors_ =  mpl.rcParams['axes.color_cycle']
	dy,dx=list(range(2))
	x=0
	y=0
	for j,f in enumerate(F[1:]):
		side_len=f
		if clr_0==None:
			clr = colors_[j%len(colors_)]
		else:
			clr = clr_0
		#
		square = list(zip(*[[x,y], [x+side_len, y], [x+side_len,y+side_len], [x, y+side_len], [x,y]]))
		print(square)
		plt.plot(*square, marker='', ls='-', lw=2.5, color=clr)
		plt.fill(*square, color=clr, alpha=fill_alpha)
		#
		x=x+dx*(side_len + x_padding*side_len) - dy*(F[j] + y_padding*side_len)
		y=y+dy*(side_len + y_padding*side_len) - dx*(F[j] + x_padding*side_len)
		
		#
		dx = (1+dx)%2
		dy = (1+dy)%2
	#
	ax=plt.gca()
	ax.set_ylim([-.1*max(square[1]), 1.1*max(square[1])])
	ax.set_xlim([-.1*max(square[0]), 1.1*max(square[0])])
	#plt.gca().set_ylim([-1., 150.])
		
	

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
	indices, Ns = list(zip(*numbers))
	countses = {x:Ns.count(x) for x in Ns}
	
	#return countses
	
	X,Y = list(zip(*sorted([rw for rw in countses.items()], key=lambda x: x[0])))
	#
	#
	#Y_sum = [sum(Y) - sum(Y[0:j+1]) for y,j in enumerate(Y)]
	Y_sum = []
	for j in range(len(Y)):
		Y_sum+=[sum(Y[j:])]
	
	print("Y's: ", Y_sum, Y)
	
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
