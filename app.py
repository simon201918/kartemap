import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

# Choosing the correct current working directory
# Import warning: If you change the code for cd, you must update the cd in kartemap.cleaning too! The two must be consistant
# os.chdir("/Users/simon/Desktop/Python_2/kartemap")

from main import get_path_distance

# drop down list for use in airport codes
from controls import CITY_DATA, CITY_POP, AIRPORT_DATA, ROUTES_DATA, AIRLINES_DATA, get_coordinate

#%%%

def coordinate_list_for_map(path):
    lat_list = []
    long_list = []
    
    city_list = path[2:-2].split("', '")

    for city in city_list:
        lat_list.append(get_coordinate(city)[0])
        long_list.append(get_coordinate(city)[1])

    return city_list, lat_list, long_list


def get_picture(city):
    return "/assets/{}.png".format(city)


pop_dict = CITY_POP.to_dict()

def get_pop(city):
    return pop_dict.get('population').get(city)

#%%

lat_list_all = []
long_list_all = []
for col in CITY_DATA['city']:
    lat,long = get_coordinate(col)
    lat_list_all.append(lat)
    long_list_all.append(long)

#%%
# setup app with stylesheets
app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])

# Create map template
# =============================================================================
# mapbox_access_token = \
#     "pk." \
#     "eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
# 
# =============================================================================
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Map",
    marker= {'size': 10,'color':'#E30909'},
    mapbox=dict(
        #accesstoken=mapbox_access_token,
        style="stamen-terrain",
        center=dict(lon=-78.05, lat=42.54),
        zoom=3,
    ),
)

layout.get('plot_bgcolor')

fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lat = lat_list_all,
    lon = long_list_all,
    marker = layout.get('marker')))


# fig.update_layout = layout

fig.update_layout(
    margin ={'l':30,'t':30,'b':20,'r':40},
    mapbox = {
        'center': {'lon': -78.05, 'lat': 42.54},
        'style': "stamen-terrain",
        'zoom': 2})





controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Start City"),
                dcc.Dropdown(
                    options=[{"label": col, "value": col} for col in CITY_DATA['city']],
                    value="Boston",
                    id="start-city",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Destination City"),
                dcc.Dropdown(
                    options=[{"label": col, "value": col} for col in CITY_DATA['city']],
                    value="New York",
                    id="destination-city",
                ),
            ]
        ),
        dbc.Button(id = 'submit',n_clicks = 0, children = "Submit", outline=True, color="primary", className="mr-1"),
    ],
    body=True,
)


photo_pop_group = dbc.FormGroup(
    [
         dbc.Row(children = [
             dbc.Col(html.H4(id='image-pop-start', children=['Start City'])),
             dbc.Col(html.H4(id='image-pop-destination', children=['Destination City']))
                 ],
                 align="center"
         ),
         html.Br(),
         dbc.Row(children = [
                 dbc.Col(html.Img(id='image-start',src=get_picture('Travel_1'), style={'height':'80%', 'width':'80%'}), md=5),
                 dbc.Col(html.Img(id='image-destination',src=get_picture('Travel_2'), style={'height':'80%', 'width':'80%'}), md=5),
                 ],
                 align="center"
        )
    ]
)


app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Kartemap - An Airport Network Analysis Application", style={'text-align': 'center'})
            )
        ),
        dbc.Row(
            [
                dbc.Col(controls, md=3),
                dbc.Col(
                    dcc.Graph(figure=fig, id="map"), md=7
                ),
            ],
            align="center",
        ),
       
        html.Br(),
        html.H3(id='show-route', children=[]),
        
        html.Br(),
        html.H3(id='show-distance', children=[]),
        
        html.Br(),
        html.Br(),
        
        photo_pop_group
        
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)

#%%

@app.callback(
    [Output(component_id='show-route', component_property='children'),
     Output(component_id='show-distance', component_property='children'),
     Output(component_id='map', component_property='figure'),
     Output(component_id='image-pop-start', component_property='children'),
     Output(component_id='image-pop-destination', component_property='children'),
     Output(component_id='image-start', component_property='src'),
     Output(component_id='image-destination', component_property='src')],
    Input(component_id='submit',component_property='n_clicks'),
    [State(component_id='start-city', component_property='value'),
     State(component_id='destination-city', component_property='value')]
)
def get_path(n_clicks, start_city, destination_city):
    path, distance_km = get_path_distance(start_city,destination_city)
    
    # distance_mile = distance_km * 1.609
    
    city_list, lat_list, long_list = coordinate_list_for_map(path)

    if len(city_list) == 1:
        show_route = ["Think again! It doesn't make sense to travel from {} to {}!".format(start_city, destination_city)]
    elif len(city_list) == 2:
        show_route = ["Looks Great! You may fly directly from {} to {}!".format(start_city, destination_city)]
    elif len(city_list) == 3:
        show_route = ["To travel from {} to {}, you should take a connection flight at {}.".format(start_city, destination_city,city_list[1])]
    else:
        show_route = ["The shortest path to travel from {} to {} is : {}".format(start_city, destination_city, path)]

    show_distance = ["The total distance of this trip is {} miles, or {} km.".format(int(float(distance_km) / 1.609), int(float(distance_km)))]

    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lat = lat_list,
        lon = long_list,
        marker = layout.get('marker')))
    
    fig.update_layout(
    margin ={'l':30,'t':30,'b':20,'r':40},
    mapbox = {
        'center': {'lon': -78.05, 'lat': 42.54},
        'style': "stamen-terrain",
        'zoom': 2})
    
    pop_start_city = ["Population of {} is {}".format(start_city, get_pop(start_city))]
    pop_destination_city = ["Population of {} is {}".format(destination_city, get_pop(destination_city))]
    
    src_start_city = get_picture(start_city)
    src_destination_city = get_picture(destination_city)
    
    return show_route, show_distance, fig, pop_start_city, pop_destination_city, src_start_city, src_destination_city

#%%

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
