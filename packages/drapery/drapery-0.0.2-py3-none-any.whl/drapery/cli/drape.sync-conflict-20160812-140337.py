import sys
import logging
import click

import fiona
import rasterio
from shapely.geometry import shape, mapping, Point, LineString

import drapery

"""
See
https://github.com/mapbox/rasterio/blob/master/rasterio/rio/sample.py
"""
@click.command()
@click.argument('source_f', nargs=1, type=click.Path(exists=True), metavar='<source_file>')
@click.argument('raster_f', nargs=1, type=click.Path(exists=True), metavar='<raster_file>')
@click.option('-o', '--output', metavar='<output_file>', type=click.Path(), help="Output file path") 
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def cli(source_f, raster_f, output, verbose):
	"""
	Adds z value to a geometry or array of geometries using GEOS sample.

	\b
	Example:
	drape point.shp elevation.tif -o point_z.shp

	"""
	with fiona.open(source_f, 'r') as source:
		source_driver = source.driver
		source_crs = source.crs
		sink_schema = source.schema.copy()
	
		source_geom = source.schema['geometry']
		if source_geom == 'Point':
			sink_schema['geometry'] = '3D Point'
		elif source_geom == 'LineString':
			sink_schema['geometry'] = '3D LineString'
		elif source_geom == '3D Point' or source_geom == '3D LineString':
			pass
		else:
			logging.exception("Source geometry type {} not implemented".format(source_geom))
	
		with rasterio.open(raster_f) as raster:
			if source_crs != raster.crs:
				logging.error("Features and raster have different CRS.")
			with fiona.open(
				output, 'w',
				driver=source_driver,
				crs=source_crs,
				schema=sink_schema) as sink:

				for feature in source:
					try:
						feature_z = drape(raster, feature, source.schema)
						sink.write({
							'geometry': mapping(feature_z),
							'properties': feature['properties'],
						})
					except Exception:
						logging.exception("Error processing feature %s:", feature['id'])
			#print(sink.closed)
		#print(raster.closed)
	#print(source.closed)

def drape(raster, feature, schema):
	"""
	Adds z coordinates to features given a raster
	"""
	coords = feature['geometry']['coordinates']
	geom = feature['geometry']['type']

	#if schema['geometry'] in ['Point', '3D Point']:
	if geom == 'Point':
		xyz = drapery.sample(raster, [coords])
		result = Point(xyz[0])
		#elif schema['geometry'] in ['LineString', '3D LineString']:
	elif geom == 'LineString':
		xyz = drapery.sample(raster, coords)
		points = [Point(x,y,z) for x,y,z in xyz]
		result = LineString(points)
	elif geom == 'Polygon':
		logging.error('drape not implemented for {}'.format(schema['geometry']))
	else:
		logging.error('drape not implemented for {}'.format(schema['geometry']))

	return result
