'''
# Miscelaneous bits and pieces, mostly for trial and error diddling
#
# mark r. yoder, phd
# mark.yoder@gmail.com
#
# this code is free to do with as you will, but it comes with no guarantees. it will probably not work correctly and cause you great sadness,
# so be warned.
'''

import datetime as dtm
import matplotlib.dates as mpd
import pytz
tzutc = pytz.timezone('UTC')

import operator
import math
import random
import numpy
import scipy
import scipy.special
#import scipy.optimize as spo
#import os
#from PIL import Image as ipp
import multiprocessing as mpp
#
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mpl as mpl
#
#import shapely.geometry as sgp
#
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from geographiclib.geodesic import Geodesic as ggp
#
import ANSStools as atp

deg2km = 111.1
deg2rad = 2.0*math.pi/360.

class Map_Lattice(object):
	'''
	# a little class to handle some map lattice projections.
	# in principle, this could be used as a data container [[x,y,z],...] but we'll probably use it 
	# note: also see the dict-o-dicts Bindex object in globalETAS folder.
	'''
	#
	def __init__(self, lons=[-180., 180.], lats=[-90., 90.], d_lat=.5, d_lon=.5, lat_0=None, lon_0=None):
		self.lats = [min(lats), max(lats)]
		self.lons = [min(lons), max(lons)]
		#
		self.lat_0 = (lat_0 or lats[0])
		self.lon_0 = (lon_0 or lons[0])	# these parameters define the lattice/bin starting point.
		#
		self.d_lat=d_lat
		self.d_lon=d_lon
		#
	#
	def lattice_dlat_dlon(self, lons=None, lats=None, d_lat=None, d_lon=None, lat_0=None, lon_0=None):
		lats = (lats or self.lats)
		lons = (lons or self.lons)
		d_lat = (d_lat or self.d_lat)
		d_lon = (d_lon or self.d_lon)
		lat_0 = (lat_0 or self.lat_0)
		lon_0 = (lon_0 or self.lon_0)
		#
		lats = [min(lats), max(lats)]
		lons = [min(lons), max(lons)]
		#
		lat_0 = (lat_0 or lats[0])
		lon_0 = (lon_0 or lons[0])	# these parameters define the lattice/bin starting point.
		#
		return [[x, y]for y in numpy.arange(lat_0, float(int(lats[1]/d_lat))*d_lat, d_lat) for x in numpy.arange(lon_0, float(int(lons[1]/d_lon))*d_lon, d_lon) ]
	def set_lattice_dlat_dlon(self):
		self.lattice = self.lattice_dlat_dlon()
	#
	def lattice_dlat_dlon_km(self, lons=None, lats=None, d_lat=None, d_lon=None, lat_0=None, lon_0=None):
		lats = (lats or self.lats)
		lons = (lons or self.lons)
		d_lat = (d_lat or self.d_lat)
		d_lon = (d_lon or self.d_lon)
		lat_0 = (lat_0 or self.lat_0)
		lon_0 = (lon_0 or self.lon_0)
		#
		lats = [min(lats), max(lats)]
		lons = [min(lons), max(lons)]
		#
		lat_0 = (lat_0 or lats[0])
		lon_0 = (lon_0 or lons[0])	# these parameters define the lattice/bin starting point.
		#
		return [[x*math.cos(y*deg2rad)*deg2km, y*deg2km] for x,y in self.lattice_dlat_dlon()]
		
	def set_lattice_dlat_dlon_km(self):
		self.lattice = self.lattice_dlat_dlon_km()
	#
	def xy_spherical_lattice(self, lons=None, lats=None, d_lat=None, d_lon=None, lat_0=None, lon_0=None, lat_lon=False):
		lats = (lats or self.lats)
		lons = (lons or self.lons)
		d_lat = (d_lat or self.d_lat)
		d_lon = (d_lon or self.d_lon)
		lat_0 = (lat_0 or self.lat_0)
		lon_0 = (lon_0 or self.lon_0)
		#
		lats = [min(lats), max(lats)]
		lons = [min(lons), max(lons)]
		#
		lat_0 = (lat_0 or lats[0])
		lon_0 = (lon_0 or lons[0])	# these parameters define the lattice/bin starting point.
		#####
		#
		# now, let's try an equal_xy transform...
		map_lattice_xy = []
		x,y = lon_lat_2xy(lon_0, lat_0)
		# assume equatorial dx,dy:
		d_x = d_lon*deg2km
		d_y = d_lat*deg2km
		print "increments: ", d_x, d_y
		# initial x_max:
		x_max = lon_lat_2xy(lons[1], lat_0)[0]
		y_max = lon_lat_2xy(lons[1], lats[1])[1]
		#
		print "maxes: ", x_max, y_max
		#
		while y<=y_max and len(map_lattice_xy)<10**9:
			#map_lattice_xy += [[x,y]]
			this_xy = [float(int(x/d_x)*d_x), float(int(y/d_y)*d_y)]
			#
			# return in lat/lon coordinates (with equal xy spacing):
			if lat_lon: this_xy = self.xy2_lon_lat(*this_xy)
			#
			map_lattice_xy += [this_xy]
			x+=d_x
			#
			#new_lon, new_lat = xy2_lon_lat(x,y)
			#if new_lon>lons[1]:
			if x>x_max:
				y+=d_y
				#
				lat = y/deg2km
				x = lon_lat_2xy(lon_0, lat)[0]
				x_max = lon_lat_2xy(lons[1], lat)[0]
				#print "new y: %f/%f :: %f" % (y, lat, x_max)
			
				#
			if y>y_max: break
		return map_lattice_xy
	def set_xy_spherical(self,*args,**kwargs):
		self.lattice = self.xy_spherical_lattice(*args, **kwargs)
	#
	def plot_lattice(self, fignum=0):
		plt.figure(fignum)
		plt.clf()
		plt.plot(*zip(*self.lattice), marker='.', ls='')
	#
	####
	#def lon_lat_2xy(self, lon=0., lat=0., lon_0=0., lat_0=0.):
	def lon_lat_2xy(self, lon=0., lat=0.):
		#lat_0 = (lat_0 or self.lat_0)
		#lon_0 = (lon_0 or self.lon_0)
		
		#lat_0 = self.lat_0
		#lon_0 = self.lon_0
		#
		#return [(lon-lon_0)*math.cos(lat*deg2rad)*deg2km, (lat-lat_0)*deg2km]
		return [(lon)*math.cos(lat*deg2rad)*deg2km, (lat)*deg2km]

	#def xy2_lon_lat(self, x=0., y=0., lon_0=0., lat_0=0.):
	def xy2_lon_lat(self, x=0., y=0.):
		#
		#lat_0 = self.lat_0
		#lon_0 = self.lon_0
		#
		#lat = lat_0 + y/deg2km
		lat = y/deg2km
		#
		if abs(lat)==90.:
			lon=0.
		else:
			#lon = lon_0 + x/(deg2km*math.cos(lat*deg2rad))
			lon = x/(deg2km*math.cos(lat*deg2rad))
		#
		return [lon, lat]
		
#
class Map_Lattice_equal_angle(Map_Lattice):
	'''
	# equal-angle (d_lat, d_lon) map projection:
	'''
	#
	def __init__(self, lons=[-180., 180.], lats=[-90., 90.], d_lat=.5, d_lon=.5, lat_0=None, lon_0=None):
		#print "locals: ", locals()
		super(Map_Lattice_equal_angle, self).__init__(**{key:val for key,val in locals().iteritems() if key!='self'})
		self.set_lattice_dlat_dlon()
		#
	#

class Map_Lattice_equal_angle_xy(Map_Lattice):
	'''
	# equal-angle (d_lat, d_lon) then projected to xy. note these are equal-theta spaced, not equal xy.
	'''
	#
	def __init__(self, lons=[-180., 180.], lats=[-90., 90.], d_lat=.5, d_lon=.5, lat_0=None, lon_0=None):
		#print "locals: ", locals()
		super(Map_Lattice_equal_angle_xy, self).__init__(**{key:val for key,val in locals().iteritems() if key!='self'})
		self.set_lattice_dlat_dlon_km()
		#
	#

class Map_Lattice_xy_spherical(Map_Lattice):
	'''
	# equal-angle (d_lat, d_lon) map projection:
	'''
	#
	def __init__(self, lons=[-180., 180.], lats=[-90., 90.], d_lat=.5, d_lon=.5, lat_0=None, lon_0=None):
		#print "locals: ", locals()
		super(Map_Lattice_xy_spherical, self).__init__(**{key:val for key,val in locals().iteritems() if key!='self'})
		self.set_xy_spherical(lat_lon=False)
		#
	#
class Map_Lattice_xy_spherical_latlon(Map_Lattice):
	'''
	# equal-angle (d_lat, d_lon) map projection:
	'''
	#
	def __init__(self, lons=[-180., 180.], lats=[-90., 90.], d_lat=.5, d_lon=.5, lat_0=None, lon_0=None):
		#print "locals: ", locals()
		super(Map_Lattice_xy_spherical_latlon, self).__init__(**{key:val for key,val in locals().iteritems() if key!='self'})
		self.set_xy_spherical(lat_lon=True)
		#
	#
		
		
def map_transform_plotter(lons=[-180., 180.], lats=[-90., 90.], d_lat=.5, d_lon=.5, lat_0=None, lon_0=None):
	# visualize some map transformations...
	#
	# handle some data...:
	lats = [min(lats), max(lats)]
	lons = [min(lons), max(lons)]
	#
	if lat_0==None: lat_0=lats[0]
	if lon_0==None: lon_0=lons[0]
	#
	# make a lattice:
	map_lattice = [[x, y]for y in numpy.arange(lat_0, float(int(lats[1]/d_lat))*d_lat, d_lat) for x in numpy.arange(lon_0, float(int(lons[1]/d_lon))*d_lon, d_lon) ]
	#
	# projecting equal degree partitioning -> km:
	map_lattice_km = [[x*math.cos(y*deg2rad)*deg2km, y*deg2km] for x,y in map_lattice]
	#
	map_lattice_xy = xy_spherical_lattice(lons=lons, lats=lats, d_lat=d_lat, d_lon=d_lon, lat_0=lat_0, lon_0=lon_0)
		
	#
	plt.figure(0)
	plt.clf()
	plt.plot(*zip(*map_lattice), color='b', marker='.', ls='')
	#
	#
	plt.figure(1)
	plt.clf()
	plt.plot(*zip(*map_lattice_km), color='b', marker='.', ls='')
	#
	plt.figure(2)
	plt.clf()
	plt.plot(*zip(*map_lattice_xy), color='b', marker='.', ls='')
	#
	return map_lattice_xy
	
def xy_spherical_lattice(lons=[-180., 180.], lats=[-90., 90.], d_lat=.5, d_lon=.5, lat_0=None, lon_0=None):
	# now, let's try an equal_xy transform...
	map_lattice_xy = []
	x,y = lon_lat_2xy(lon_0, lat_0)
	# assume equatorial dx,dy:
	d_x = d_lon*deg2km
	d_y = d_lat*deg2km
	print "increments: ", d_x, d_y
	# initial x_max:
	x_max = lon_lat_2xy(lons[1], lat_0)[0]
	y_max = lon_lat_2xy(lons[1], lats[1])[1]
	#
	print "maxes: ", x_max, y_max
	#
	while y<=y_max and len(map_lattice_xy)<10**9:
		#map_lattice_xy += [[x,y]]
		map_lattice_xy += [[float(int(x/d_x)*d_x), float(int(y/d_y)*d_y)]]
		x+=d_x
		#
		#new_lon, new_lat = xy2_lon_lat(x,y)
		#if new_lon>lons[1]:
		if x>x_max:
			y+=d_y
			#
			lat = y/deg2km
			x = lon_lat_2xy(lon_0, lat)[0]
			x_max = lon_lat_2xy(lons[1], lat)[0]
			#print "new y: %f/%f :: %f" % (y, lat, x_max)
			
			#
		if y>y_max: break
	return map_lattice_xy
#
def lon_lat_2xy(lon=0., lat=0., lon_0=0., lat_0=0.):
	return [(lon-lon_0)*math.cos(lat*deg2rad)*deg2km, (lat-lat_0)*deg2km]

def xy2_lon_lat(x=0., y=0., x_0=0., y_0=0.):
	lat = (y-y_0)/deg2km
	#
	if abs(lat)==90.:
		lon=0.
	else:
		lon = (x-x_0)/(deg2km*math.cos(lat*deg2rad))
	#
	return [lon, lat]

class Ellipse(object):
	def __init__(self, a=1.0, b=.5, ab_ratio=None, theta=0.):
		if a==None and b==None: a,b = 1.0, .5
		if not (a==None and b==None): ab_ratio=a/float(b)
		#
		if a==None: a=b*ab_ratio
		if b==None: b=a/ab_ratio
		#
		self.a = a
		self.b = b
		#
		if theta>1.1*math.pi*2.0: theta*=deg2rad
		self.theta=theta
		#
		self.ab_ratio = ab_ratio
		self.h = ((a-b)/(a+b))**2
	#
	@property
	def area(self):
		return math.pi*self.a*self.b

	@property
	def circumference_exact(self):
		
		return math.pi*(self.a+self.b)*scipy.special.hyp2f1(-.5, -.5, 1.0, self.h)
	
	@property
	def circumference_approx1(self):
		# there are two good approximations from Ramanujan (see wikipedia); this is one of them...
		#
		return math.pi*(self.a+self.b)*(1. + 3.*self.h/(10 + math.sqrt(4. - 3.*self.h)))
	#
	def poly(self, n_points=100):
		d_theta = 2.0*math.pi/n_points
		poly = [[self.a*math.cos(theta), self.b*math.sin(theta)] for theta in numpy.arange(0., 2.0*math.pi+d_theta, d_theta)]
		# there's probably a smarter way to do this...
		if self.theta!=0.:
			poly = numpy.dot([[math.cos(self.theta), -math.sin(self.theta)],[math.sin(self.theta), math.cos(self.theta)]], poly)
		return ploy

if __name__=='__main__':
	# do background stuff...
	pass
else:
	# be interactive...
	plt.ion()
