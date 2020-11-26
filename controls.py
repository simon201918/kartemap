#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 23:03:11 2020

@author: simon
"""

import pandas as pd
import os
import numpy as np

import geopy.distance



#%% Import the data to create the csv required for shrotest-path algorithms

AIRLINES_DATA = pd.read_csv('data/airlines.csv',
                       names=['Airline_ID','Name','Alias','IATA','ICAO','Callsign','Country','Active'])
AIRPORT_DATA = pd.read_csv('data/airport.csv',
                     names = ['Airport_ID','Name','City','Country','IATA','IACO','Latitude','Longitude','Altitude','Timezone','DST','Tz_database_time_zone','Type','Source'])
CITY_DATA = pd.read_csv('data/city.csv',names=['city','population'])
ROUTES_DATA = pd.read_csv('data/routes.csv',
                    names=['Airline','Airline_ID','Source_airport','Source_airport_ID','Destination_airport','Destination_airport_ID','Codeshare','Stops','Equipment'])

CITY_POP = pd.read_csv('data/city.csv',names=['city','population'],index_col = 0)

# Extract city list from city
CITY_LIST = CITY_DATA.iloc[:,0].tolist()


# Select the airport list, only keep the airports that located in city list， also drop ?N airports
AIRPORT_DATA.drop(AIRPORT_DATA[AIRPORT_DATA['Airport_ID'] == r'\N'].index, inplace=True)
AIRPORT_LIST = AIRPORT_DATA[(AIRPORT_DATA.Country == 'United States') & (AIRPORT_DATA.City.isin(CITY_LIST))]

# Remove the irrelevant columns in airport list
AIRPORT_LIST = AIRPORT_LIST.loc[:,['Airport_ID','City','Country','IATA','Latitude','Longitude']]

# Create a airport list to merge with routes
airport_merge_source = AIRPORT_LIST.iloc[:,0:2]
airport_merge_source.columns = ['Source_airport_ID', 'Source_City']

airport_merge_destination = AIRPORT_LIST.iloc[:,0:2]
airport_merge_destination.columns = ['Destination_airport_ID', 'Destination_City']

#%% Clean AIRLINES_DATA, remove non-active airlines
AIRLINES_DATA.drop(AIRLINES_DATA[AIRLINES_DATA['Active'] != 'Y'].index, inplace=True)

#%%
# Clean the routes dataset, only keep rountes between target cities
ROUTES_DATA.drop(ROUTES_DATA[ROUTES_DATA['Airline_ID'] == r'\N'].index, inplace=True)
ROUTES_DATA.drop(ROUTES_DATA[ROUTES_DATA['Source_airport_ID'] == r'\N'].index, inplace=True)
ROUTES_DATA.drop(ROUTES_DATA[ROUTES_DATA['Destination_airport_ID'] == r'\N'].index, inplace=True)

ROUTES_DATA = ROUTES_DATA[(ROUTES_DATA.Source_airport.isin(AIRPORT_LIST.IATA)) & (ROUTES_DATA.Destination_airport.isin(AIRPORT_LIST.IATA))]
# Only keep relevant columns
ROUTES_DATA = ROUTES_DATA.loc[:,['Airline','Airline_ID','Source_airport','Source_airport_ID','Destination_airport','Destination_airport_ID']]

# Append city names to rountes so that we can check the connectivity among the cities
# (Note: Source_airport_ID and Destination_airport_ID must be convert to int type to make merge work)
ROUTES_DATA.Source_airport_ID = ROUTES_DATA.Source_airport_ID.astype(int)
ROUTES_DATA.Destination_airport_ID = ROUTES_DATA.Destination_airport_ID.astype(int)

ROUTES_DATA = ROUTES_DATA.merge(airport_merge_source, how = 'left', on = 'Source_airport_ID')
ROUTES_DATA = ROUTES_DATA.merge(airport_merge_destination, how = 'left', on = 'Destination_airport_ID')

# Extract unique routes
UNIQUE_ROUTES = ROUTES_DATA.iloc[:,-2:].drop_duplicates().reset_index(drop=True)


#%% Get the coordinates of cities in the US
coordinate_df = AIRPORT_LIST.groupby('City').mean()

def get_coordinate(city):
    lat = coordinate_df.loc[city,'Latitude']
    long = coordinate_df.loc[city,'Longitude']
    return lat,long

#%% Calculate distance between two cities

def get_distance_in_km(city_A,city_B): 
    import geopy.distance
    # Start City
    lat_a, long_a = get_coordinate(city_A)
    # Destination City
    lat_b, long_b = get_coordinate(city_B)
    # Return distance
    return round(geopy.distance.geodesic((lat_a,long_a), (lat_b,long_b)).km)


UNIQUE_ROUTES['distance'] = np.zeros(shape = [UNIQUE_ROUTES.shape[0],1])

for i in range(UNIQUE_ROUTES.shape[0]):
    UNIQUE_ROUTES['distance'][i] = get_distance_in_km(UNIQUE_ROUTES.Source_City[i],UNIQUE_ROUTES.Destination_City[i])

# UNIQUE_ROUTES.to_csv('data/unique_routes.csv',index = False, header = False)

#%% No round trip problem
# The code below confirms that not all cities have round trips: You may go from A to B, but not the other way round

check = UNIQUE_ROUTES.groupby(['distance']).size().reset_index(name='count')
check[check['count'] == 1]

#%% Use shortest path algorithm to get the shortest route gievn two cities

# Use 'Network Analysis Python Source Code/main.py'

if __name__ == '__main__':
    pass

























