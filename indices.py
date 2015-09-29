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

#class T_square(object):
#	# a tsunami square object.
#	def __init__(self, x=0., y=0., z=0.):
#		self.x=x
#		self.y=y
#		self.z=z
		#
	#
def rtree_test2(lons=[-124., -114.], lats=[30., 41.5], anss_cat=None, mc=3.0):
	#
	# get an earthquake catalog from ANSS:
	# def catfromANSS(lon=[135., 150.], lat=[30., 41.5], minMag=4.0, dates0=[dtm.datetime(2005,01,01, tzinfo=tzutc), None], Nmax=None, fout=None, rec_array=True):
	# use rtree index to select objects (earthquakes) from a geo-spatial region.
	# note also nearest-neighbor test script(s).
	if anss_cat==None: anss_cat = atp.catfromANSS(lon=lons, lat=lats, minMag=mc, dates0=[dtm.datetime(2000,01,01, tzinfo=atp.tzutc), None], Nmax=None, fout=None, rec_array=True)
	cols, formats = [list(x) for x in zip(*anss_cat.dtype.descr)]
	#
	print "catalog fetched. now set up index..."
	#
	#return anss_cat
	# now, set up an index. do we need a bunch of indices, or is that the whole point of this?
	#
	idx = index.Index()
	# our bounding box:
	left,bottom,right,top = lons[0], lats[0], lons[1], lats[1]
	bounds = (left, bottom, right, top)
	#print "bounds: ", bounds
	#return anss_cat
	#
	# now, insert all item indices from anss_cat into idx. nominally, we could insert the row as an object, or an index as an object... or we can synch the id with the
	# row index, and use the id as the index. note we insert elements as points, with left=right, top=bottom.
	[idx.insert(j, (rw['lon'], rw['lat'], rw['lon'], rw['lat'])) for j,rw in enumerate(anss_cat)]
	# 
	# now, we can use idx to get the index (row number) of elements inside some bounding rectangle like (i think):
	# note: height, width, etc. have to be defined. this is basically pseudo-code at this point.
	ev_x = numpy.mean(lons)
	ev_y = numpy.mean(lats)
	zone_width = .3*abs(lons[1]-lons[0])
	zone_height =  .3*abs(lats[1]-lats[0])
	print "mean position: ", ev_x, ev_y, zone_width, zone_height
	#
	event_neighbor_indices = list(idx.intersection((ev_x-zone_width, ev_y-zone_height, ev_x + zone_width, ev_y+zone_height)))
	event_neighbors = [anss_cat[j] for j in event_neighbor_indices]
	lat_index = cols.index('lat')
	lon_index = cols.index('lon')
	#
	zone_box = [[ev_x-zone_width, ev_y-zone_height],[ev_x+zone_width, ev_y-zone_height], [ev_x+zone_width, ev_y+zone_height], [ev_x-zone_width, ev_y+zone_height], [ev_x-zone_width, ev_y-zone_height]]
	#
	plt.figure(0)
	plt.clf()
	plt.plot(anss_cat['lon'], anss_cat['lat'], '.', color='b')
	plt.plot(*zip(*zone_box), color='g',  ls='--', lw=1.5, alpha=.8)
	plt.plot(*zip(*[[anss_cat[k][lon_index], anss_cat[k][lat_index]] for k in event_neighbor_indices]), marker = '+', ls='', color='g', alpha=.7)
	plt.plot([ev_x], [ev_y], '*', ms=15, color='r')
	#
	return anss_cat, idx


class T_square_lattice(object):
	# container and scripts for tsunami square stuff.
	#
	def __init__(self, x0=0., y0=1., z0=0., x_max=100., y_max=100., dx=1., dy=1., Z=None):
		if Z==None:
			numpy.array(Z=[[z0 for j in xrange(round((x_max-x0)/dx))] for k in xrange(round((y_max-y_0)/dy))])
		#
	def nudge(self, j,k):
		pass

#def my_t_squares():
	

####################################
if __name__=='__main__':
	pass
else:
	plt.ion()
