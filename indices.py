'''
# some experimental and developmental indexing codes.

'''

import numpy
import pylab as plt
import math
import scipy
import datetime as dtm
import pytz
import matplotlib.dates as mpd
import multiprocessing as mpp
import random
#
import ANSStools as atp
import rtree
from rtree import index
#
def rtree_test1(lons=[-124., -114.], lats=[30., 41.5], mc=3.0):
	#
	# get an earthquake catalog from ANSS:
	# def catfromANSS(lon=[135., 150.], lat=[30., 41.5], minMag=4.0, dates0=[dtm.datetime(2005,01,01, tzinfo=tzutc), None], Nmax=None, fout=None, rec_array=True):
	anss_cat = atp.catfromANSS(lon=lons, lat=lats, minMag=mc, dates0=[dtm.datetime(2000,01,01, tzinfo=atp.tzutc), None], Nmax=None, fout=None, rec_array=True)
	#
	#return anss_cat
	# now, set up an index. do we need a bunch of indices, or is that the whole point of this?
	#
	idx = index.Index()
	# our bounding box:
	left,bottom,right,top = lons[0], lats[0], lons[1], lats[1]
	bounds = (left, bottom, right, top)
	#
	# now, insert all item indices from anss_cat into idx. nominally, we could insert the row as an object, or an index as an object... or we can synch the id with the
	# row index, and use the id as the index. note we insert elements as points, with left=right, top=bottom.
	[idx.insert(j, (rw['lon'], rw['lat'], rw['lon'], rw['lat'])) for j,rw in enumerate(anss_cat)]
	#
	# now, how 'bout find each point's NN:
	NN_1s=[list(idx.nearest((rw['lon'], rw['lat'], rw['lon'], rw['lat']),1)) for j,rw in enumerate(anss_cat)]
	NN_2s=[list(idx.nearest((rw['lon'], rw['lat'], rw['lon'], rw['lat']),2)) for j,rw in enumerate(anss_cat)]
	#
	idx2 = index.Index()
	idx2.insert(0, (0.,0.,1.,1.))
	idx2.insert(1, (1.5,.5,1.5,.5))		# point at 1.5,.5
	idx2.insert(2, (.5, 1.5, .5, 1.5))	# point at .5, 1.5
	#
	# note, if we are looking for NNs to an object in the database (index), it will find itself first. this is not "find the NNs of object X in the index";
	# the object/window is independent and external.
	print "indersections: ", list(idx2.intersection((0.,0.,1.,1.)))
	print "NNs:         : ", list(idx2.nearest((0.,0.,1.,1.),2))
	#
	return NN_1s, NN_2s



####################################
if __name__=='__main__':
	pass
else:
	plt.ion()
