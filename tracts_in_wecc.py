print("importing packages \n")
import numpy as np
from scipy.spatial import cKDTree
import matplotlib as mpl
import pandas as pd
import geopandas as gpd
import os
import psycopg2
from operator import itemgetter
from shapely.geometry import Polygon, shape, Point
import shapely.wkt 
import time
import pathos.multiprocessing as mp
from pathos.parallel import stats
import sqlalchemy
from sqlalchemy import create_engine
import csv
from scipy import spatial

#make pg connection
host = ''
dbase = ''
user = ''
pwd = ''
con = create_engine('postgresql://{user}:{pwd}@{host}:5432/{dbase}'.format(host=host, dbase=dbase, user=user, pwd=pwd), echo=False)
connection = con.raw_connection()

sql_wecc = "select boundary, the_geom_4326 from dhetting.wecc_boundary;"
wecc = gpd.GeoDataFrame.from_postgis(sql_wecc, con, geom_col='the_geom_4326')
wecc = wecc.to_crs(epsg=4326)
wecc.plot()
print("wecc: \n", wecc.head())

sql_tracts = "select geoid, gisjoin, statefp, countyfp, the_geom_4326 from nhgis.us_tracts_2016 where statefp in ('30', '48', '53', '56', '08', '06', '16', '04', '49', '32', '41', '35', '46');"
tracts = gpd.GeoDataFrame.from_postgis(sql_tracts, con, geom_col='the_geom_4326')
tracts = tracts.to_crs(epsg=4326)
tracts = tracts[tracts.statefp != '31']
all_tracts_list = ['53', '56', '08', '06', '16', '04', '49', '32', '41']
wecc_tracts = tracts.loc[tracts.statefp.isin(all_tracts_list)]
part_tracts_list = ['46', '30', '35']
some_tracts = tracts.loc[tracts.statefp.isin(part_tracts_list)]
some_tracts.tail(20)

countrow_some = some_tracts.shape[0]
countrow_all = wecc_tracts.shape[0]
print("ALL TRACTS IN WECC:", countrow_all, "\nSOME TRACTS IN WECC:", countrow_some)

tracts_intersection = gpd.overlay(some_tracts, wecc, how='intersection')
tracts_intersection.plot()
tracts_intersection.head(20)

tracts_intersection = tracts_intersection.rename(columns={'geometry':'the_geom_4326'}).set_geometry('the_geom_4326')results = pd.concat([tracts_intersection, wecc_tracts])
countrow_results = results.shape[0]
print(countrow_results)

final_destination = '/projects/kwaechte/data/'
name='tracts_in_wecc'
# results.to_file(str(final_destination)+str(name)+".json", driver="GeoJSON")
filetype = '.csv'
csvresults = results.drop('the_geom_4326', axis=1)
csvresults.to_csv(str(final_destination)+str(name)+str(filetype))
print("export complete")
