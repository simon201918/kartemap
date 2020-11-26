#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:04:14 2020

@author: simon
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from controls import CITY_DATA, AIRPORT_DATA, ROUTES_DATA, AIRLINES_DATA, get_coordinate

# Choosing the correct current working directory
# Import warning: If you change the code for cd, you must update the cd in kartemap.cleaning too! The two must be consistant
# os.chdir("/Users/simon/Desktop/Python_2/kartemap")

from main import get_path_distance

#%%

path, distance = get_path_distance('Miami',"Portland")


path[2:-2]

path[2:-2].split("', '")[1]


def coordinate_list_for_map(path):
    lat_list = []
    long_list = []
    
    city_list = path[2:-2].split("', '")

    for city in city_list:
        lat_list.append(get_coordinate(city)[0])
        long_list.append(get_coordinate(city)[1])

    return city_list, lat_list, long_list

    
coordinate_list_for_map(path)
    
    
lat_list_all = []
long_list_all = []
for col in CITY_DATA['city']:
    lat,long = get_coordinate(col)
    lat_list_all.append(lat)
    long_list_all.append(long)
    
    
city = 'Boston'
def get_picture(city):
    return "/assets/{}.png".format(city)
    
CITY_POP = pd.read_csv('data/city.csv',names=['city','population'],index_col = 0)
pop_dict = CITY_POP.to_dict()

def get_pop(city):
    return pop_dict.get('population').get(city)

    
get_pop("Boston")
    
    
    
