import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# init_notebook_mode(connected= True)

from urllib.request import urlopen
import json

import warnings
#deploying on v22 stack

warnings.filterwarnings('ignore')
bkColor = '#d2d2d2'

#pakistan map
custom_geo = 'https://raw.githubusercontent.com/aahmed96/GISData/patch-2/PAK-GeoJSON/PAK_aa_province.json'
with urlopen(custom_geo) as response:
    pak = json.load(response)

#pakistan data
pakistan_data = 'https://raw.githubusercontent.com/ShahrozTanveer/covid-19-pakistan/master/covid-19-pakistan-data.csv'
df_pakistan = pd.read_csv(pakistan_data,dtype={"fips": str})
df_pakistan['province'] = df_pakistan['province'].replace({'SINDH':'Sindh',
                                                          'PUNJAB':'Punjab',
                                                          'BALOCHISTAN':'Balochistan',
                                                          'KP':'Khyber Pakhtunkhwa',
                                                          'ISLAMABAD':'Islamabad',
                                                          'GB':'Gilgit-Baltistan',
                                                          'AJK':'Azad Jammu and Kashmir'})


df_pakistan = df_pakistan.rename(columns = {
                                            'date':'Date', 'province':'Province',
                                            'total_cases':'Total Reported', 'active':'Total Active', 'recovered':'Total Recoveries',
                                            'deaths':'Total Deaths'})

df_pak_latest = df_pakistan.tail(7)

#global data
df_confirmed = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df_deceased = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
df_recovered = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

df_country_deaths_latest = df_deceased.groupby(["Country/Region"]).sum().reset_index()
df_country_deaths_latest = df_country_deaths_latest.drop(list(df_country_deaths_latest)[1:-1], axis=1)
last_column = df_country_deaths_latest.columns[-1]
df_country_deaths_latest = df_country_deaths_latest.rename(columns = {last_column : 'Total Deaths'})


df_country_recovered_latest = df_recovered.groupby(["Country/Region"]).sum().reset_index()
df_country_recovered_latest = df_country_recovered_latest.drop(list(df_country_recovered_latest)[1:-1], axis=1)
df_country_recovered_latest = df_country_recovered_latest.rename(columns = {last_column : 'Total Recoveries'})

df_country_confirmed_latest = df_confirmed.groupby(["Country/Region"]).sum().reset_index()
df_country_confirmed_latest = df_country_confirmed_latest.drop(list(df_country_confirmed_latest)[1:-1], axis=1)
df_country_confirmed_latest = df_country_confirmed_latest.rename(columns = {last_column : 'Total Reported'})

df_country_all = pd.merge(df_country_confirmed_latest, df_country_recovered_latest,
                         on = 'Country/Region')
df_country_total = pd.merge(df_country_all, df_country_deaths_latest,
                         on = 'Country/Region')
df_country_total['Total Active'] = df_country_total['Total Reported'] - (df_country_total['Total Recoveries'] + df_country_total['Total Deaths'])


#graphs
a = ['aggrnyl','agsunset', 'algae', 'amp', 'armyrose', 'balance',
     'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
     'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
     'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
     'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
     'haline','hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
     'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
     'orrd', 'oryel', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
     'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor',
     'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy',
     'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral',
     'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose',
     'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'twilight',
     'viridis', 'ylgn', 'ylgnbu', 'ylorbr','ylorrd']

df_country_total_sorted = df_country_total.sort_values(by=['Total Reported'],ascending = False)
countries = df_country_total_sorted['Country/Region'].to_list()
#print(countries)
countries_labels = countries.copy()
countries_labels[0] = 'United States of America'
country_options = [dict(label=x, value=y) for x, y in zip(countries_labels, countries)]
country_options.insert(0,{'label': 'Worldwide','value':'Worldwide'})

#graph2
df_country_rec = df_recovered.groupby(["Country/Region"]).sum().reset_index()
df_country_death = df_deceased.groupby(["Country/Region"]).sum().reset_index()
df_country_r = df_confirmed.groupby(["Country/Region"]).sum().reset_index()
drop_columns = ['Lat','Long']
df_global_r = df_country_r.drop(drop_columns, axis = 1)
df_global_r = df_global_r.set_index('Country/Region')
df_global_r = df_global_r.T
df_global_r.index.names = ['Date']
df_global_r['Worldwide'] = df_global_r.sum(axis = 1)
df_global_d = df_country_death.drop(drop_columns, axis = 1)
df_global_d = df_global_d.set_index('Country/Region')
df_global_d = df_global_d.T
df_global_d.index.names = ['Date']
df_global_d['Worldwide'] = df_global_d.sum(axis = 1)

df_global_rc = df_country_rec.drop(drop_columns, axis = 1)
df_global_rc = df_global_rc.set_index('Country/Region')
df_global_rc = df_global_rc.T
df_global_rc.index.names = ['Date']
df_global_rc['Worldwide'] = df_global_rc.sum(axis = 1)

df_countries = pd.read_csv('countries of the world.csv')
dc = ['Area (sq. mi.)', 'Infant mortality (per 1000 births)',
       'Coastline (coast/area ratio)',
       'Net migration',
     'Arable (%)',
       'Crops (%)', 'Other (%)', 'Climate', 'Birthrate', 'Deathrate'
       ]
df_countries = df_countries.drop(dc, axis = 1)
df_country_total_new = df_country_total
df_country_total_new = df_country_total.rename(columns={'Country/Region':'Country'})
df_country_total_new['Country'] = df_country_total_new['Country'].astype('str')
df_countries['Country'] = df_countries['Country'].astype('str')

df_country_total_new['Country']  = df_country_total_new['Country'].str.strip()
df_countries['Country']  = df_countries['Country'].str.strip()

df_demographics = pd.merge(df_country_total_new,df_countries,on ='Country')
df_demographics['Affected'] = (df_demographics['Total Reported'] / df_demographics['Population'])*100

df_demographics = df_demographics.sort_values(by=['Total Reported'],ascending = False)
affected_dict = dict(zip(df_demographics.Country,df_demographics.Affected ))

app = dash.Dash(__name__)

server = app.server

app.title = 'COVID 19 - Tracking the Pandemic'

app.layout = html.Div([

    html.Div([
        html.H1(['COVID 19'],style = {'textAlign': 'center','letter-spacing': '4px','color':'#fff'}),

        html.H4(['TRACKING THE PANDEMIC'
              ],className = 'row',style = {'textAlign': 'center', 'letter-spacing': '3px','color':'#07a890'})
]),

    html.Div([
dcc.Tabs(
        id='varType',
        value = 'Total Active', children = [
        dcc.Tab(label = 'Active', value = 'Total Active',className='custom-tab',selected_className='custom-tab--selected'),
        dcc.Tab(label='Reported', value= 'Total Reported',className='custom-tab',selected_className='custom-tab--selected'),
        dcc.Tab(label= 'Recovered', value= 'Total Recoveries',className='custom-tab',selected_className='custom-tab--selected'),
        dcc.Tab(label= 'Deceased', value= 'Total Deaths',className='custom-tab',selected_className='custom-tab--selected')
    ], style={'color': '#28334A','font-weight':'300'}),

             dcc.Loading(id='loading1',
                    children =[dcc.Graph(id='worldMap',

                      config= {
                          "scrollZoom":False,
                          "editable":False,
                          "doubleClick":'reset',
                          "displaylogo":False,
                          "modeBarButtonsToRemove":['pan2d','lasso2d','zoomOutGeo','hoverClosestGeo',
                                                    'zoomIn2d','zoomOut2d','autoScale2d','zoomInGeo']
                      }
                      )

                    ], type="cube", color='#008489')
        ],style = {'backgroundColor':'#28334A !important'}),

    html.Div([
        dcc.Tabs(
            id='toggle',
            value = 'choroMap',

            children = [
                dcc.Tab(label='World Map', value='choroMap',className='custom-tab',selected_className='custom-tab--selected'),
                dcc.Tab(label='Pie Chart',value = 'pieChart',className='custom-tab',selected_className='custom-tab--selected'),
                dcc.Tab(label='Pakistan',value = 'pakMap',className='custom-tab',selected_className='custom-tab--selected')
            ]
        )
    ],className='container',style={'width':300,'padding':15}),

html.Div([

        html.H4(['A TIME SERIES VISUALIZATION BY COUNTRY'
              ],className = 'row',style = {'textAlign': 'center', 'letter-spacing': '3px','color':'#fff',
                                          'background': 'radial-gradient(circle, #28334A, #07a890)',
                                           'background-color': bkColor,'padding':30}),

html.Div([
        dcc.Dropdown(
            id='country-drop',
            value = 'Worldwide',
            options= country_options,
            clearable= False,

            placeholder='Select a region'
        )],className='container',style={'width':300,'background': 'radial-gradient(circle, #28334A, #28334A)'},id='wrapper'),
],style={'background': 'radial-gradient(circle, #28334A, #07a890)','padding':15}),



    html.Div([

        html.Div([
            dcc.Loading(id='loading2',
                    children =[
                        dcc.Graph(id='active',
                                  config={
                                      "displaylogo": False,
                                      "scrollZoom": False,
                                      "modeBarButtonsToRemove": ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',
                                                                 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                                                                 'toggleHover', 'resetViews',
                                                                 'hoverClosestCartesian', 'hoverCompareCartesian',
                                                                 'toggleSpikelines']
                                  }
                                  )], type="circle", color='#008489')

                    ], className='featured'
        ),

         html.Div([
                dcc.Loading(id='loading3',
                    children =[
                    dcc.Graph(id='comparison',
                      config={
                          "displaylogo":False,
                          "scrollZoom":False,
                          "modeBarButtonsToRemove": ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d',
                                                     'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleHover',
                                                     'resetViews',
                                                     'hoverClosestCartesian', 'hoverCompareCartesian',
                                                     'toggleSpikelines']
                      },
                      )],type="circle", color='#008489')

                    ],className = 'featuredTwo'

        ),

         html.Div([
            html.Div([
                html.P('SUMMARY', style = {'font-size':24, 'font-weight':'200px',
                                            'text-align':'center','letter-spacing': '3.5px', 'padding-top': 20})
            ],className='row'),

            html.Div([
                html.P(id='date',children =last_column, style={'font-size': 14, 'font-weight': '100px',
                                         'text-align': 'center', 'letter-spacing': '4px'})
            ], className='row'),


            html.Div([
                #starts here
                html.Div([

                html.Div([
                    html.Div([
                        html.P(id='reported-cases',
                               style={'text-align': 'center', 'letter-spacing': '3px', 'font-size': 24})
                    ], className='three columns'),
                    html.Div([
                        html.P(id='recovered-cases',
                               style={'text-align': 'center', 'letter-spacing': '3px', 'font-size': 24})
                    ], className='three columns'),

                    html.Div([
                        html.P(id='active-cases', style={'text-align': 'center', 'letter-spacing': '3px','font-size':24})
                    ],className='three columns'),
                    html.Div([
                        html.P(id='deceased-cases', style={'text-align': 'center', 'letter-spacing': '3px','font-size':24})
                    ], className='three columns'),

                ],className = 'row'),

                html.Div([
                    html.Div([
                        html.P('REPORTED', style={'text-align': 'center', 'letter-spacing': '3.5px','font-size':15})
                    ],className='three columns'),
                    html.Div([
                        html.P('RECOVERED', style={'text-align': 'center', 'letter-spacing': '3.5px','font-size':15})
                    ], className='three columns'),

                    html.Div([
                        html.P('ACTIVE', style={'text-align': 'center', 'letter-spacing': '3.5px','font-size':15})
                    ],className='three columns'),
                    html.Div([
                        html.P('DECEASED', style={'text-align': 'center', 'letter-spacing': '3.5px','font-size':15})
                    ], className='three columns'),

                ],className = 'row'),

                html.Div([
                    html.Div([
                        html.P(id='reported-cases-new',
                               style={'text-align': 'center', 'letter-spacing': '3px', 'font-size': 12,'font-style':'italic',
                                      'color':'#850000'})
                    ], className='three columns'),
                    html.Div([
                        html.P(id='recovered-cases-new',
                               style={'text-align': 'center', 'letter-spacing': '3px', 'font-size': 12,'font-style':'italic',
                                      'color':'#850000'})
                    ], className='three columns'),

                    html.Div([
                        html.P(id='active-cases-new')
                    ],className='three columns'),
                    html.Div([
                        html.P(id='deceased-cases-new', style={'text-align': 'center', 'letter-spacing': '3px','font-size':12,
                                                               'font-style':'italic',
                                                               'color':'#850000'})
                    ], className='three columns'),

                ],className = 'row'),


                ],className='row'),

                #ends here
            html.Div([
                html.Div([
                    html.P('CASE FATALITY RATE',style = {'text-align':'center','letter-spacing': '3px','padding-top':'30px'},
                           className='six columns'),
                    html.P('POPULATION AFFECTED', style={'text-align': 'center', 'letter-spacing': '3px','padding-top':'30px'},
                           className='six columns'),

                ],className = 'row'),

                html.Div([
                    html.P(id='mortality', style={'font-size': 20, 'text-align': 'center', 'letter-spacing': '3px','padding-bottom':'30px'},
                           className='six columns'),
                    html.P(id='affected', style={'font-size': 20, 'text-align': 'center', 'letter-spacing': '3px','padding-bottom':'10px'},
                           className='six columns')

                ], className='row'),

            ],className = 'row'),


            ],className='container'),

        ],className='featuredThree'),

        ],className='detailwrap'),

    html.Div([
        html.Div(['ADIL AHMED 2020'
                 ], className='row'),

        html.A('LinkedIn',href = 'https://www.linkedin.com/in/adilahmed96/',className = 'row',
                   target = "_blank", style={'color':'#fff','text-decoration':'none'})
    ],style={'font-size':10,'textAlign': 'center', 'letter-spacing': '4px', 'color': '#fff',
                                            'background': 'radial-gradient(circle, #28334A, #07a890)',
                                            'background-color': bkColor, 'padding': 30}),

        
],style={'backgroundColor': '#28334A'})

@app.callback(dash.dependencies.Output('worldMap','figure'),
              [dash.dependencies.Input('varType', 'value'),
               dash.dependencies.Input('toggle','value')]
              )



def update_chormap(varType,toggle):

    selectType = varType

    figType = toggle

    if selectType == 'Total Active':
        colorScale = a[18]
        bck = '#f2f2f2'

    elif selectType == 'Total Reported':
        colorScale = a[5]
        bck = '#f2f2f2'

    elif selectType == 'Total Deaths':
        colorScale = a[3]
        bck = '#cccccc'

    elif selectType == 'Total Recoveries':
        colorScale = a[19]
        bck = '#cccccc'


    data = dict(
        type='choropleth',
        locations=df_country_total['Country/Region'],
        locationmode='country names',
        z=df_country_total[selectType],
        text=df_country_total[selectType],
        # text = df_country_latest['Country/Region'],
        marker_line_color='white',
        colorscale=colorScale,
        #colorbar_title=selectType,
        hovertemplate="<b>%{location}</b><extra>%{text}</extra>"
    )

    layout = dict(
        #title=selectType + ' - COVID-19',
        paper_bgcolor= bck,
        height = 500,
        margin=dict(l=40, t=45, r=50, b=45),
        transition =dict(
        duration = 500,
        easing ='cubic-in-out'),
        geo=dict(
            showframe=False,
            showocean=True,
            projection={'type': 'equirectangular'},
            bgcolor=bck,
            oceancolor=bck
        )

    )

    pchart = px.pie(df_country_total, values=selectType, names='Country/Region',color_discrete_sequence=px.colors.sequential.RdBu)
    pchart.update_traces(textposition='inside')
    pchart.update_layout(paper_bgcolor='#f0f0f0')
    # fig.update_layout(uniformtext_mode='hide')
    pchart.update_traces(textposition='inside', textinfo='percent+label')

    #pakistans map
    pakmap = go.Figure(go.Choroplethmapbox(geojson=pak, locations=df_pak_latest.fips, z=df_pak_latest[selectType],
                                           colorscale=colorScale, text=df_pak_latest.Province,
                                           marker_opacity=0.8, marker_line_width=1.5, marker_line_color='white',
                                           hovertemplate="<b>%{text}</b>" + " <br><i>Count: </i>%{z}<extra></extra>"))
    pakmap.update_layout(mapbox_style='carto-positron',
                         mapbox_zoom=4.2, mapbox_center={"lat": 30.7968, "lon": 69.0510}
                         #,width=700
                         )

    pakmap.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                         plot_bgcolor = '#000',paper_bgcolor = '#fafaf8')

    if figType == 'choroMap':
        return (
            go.Figure(data=[data], layout=layout)
        )
    elif figType == 'pakMap':
        return(
            pakmap
        )
    else:
        return(
           pchart
    )

@app.callback([dash.dependencies.Output('active','figure'),
               dash.dependencies.Output('comparison','figure'),
               dash.dependencies.Output('reported-cases','children'),
               dash.dependencies.Output('recovered-cases','children'),
               dash.dependencies.Output('active-cases','children'),
               dash.dependencies.Output('deceased-cases','children'),
               dash.dependencies.Output('reported-cases-new','children'),
               dash.dependencies.Output('recovered-cases-new','children'),
               dash.dependencies.Output('active-cases-new','children'),
               dash.dependencies.Output('active-cases-new','style'),
               dash.dependencies.Output('deceased-cases-new','children'),

               dash.dependencies.Output('mortality','children'),
               dash.dependencies.Output('affected','children')
               ],
              [dash.dependencies.Input('country-drop', 'value')]
              )


def update_multifig(input_value):
    area = input_value

    recoveries = df_global_rc[area].to_list()
    deaths = df_global_d[area].to_list()
    reported = df_global_r[area].to_list()
    x = len(reported)
    days = np.arange(0, x, 1)


    data = {'Days': days, 'Reported': reported, 'Deaths': deaths, 'Recoveries': recoveries}
    df_world = pd.DataFrame(data)
    df_world['Active'] = df_world.Reported - df_world.Recoveries - df_world.Deaths
    headers = (df_world.columns.to_list())[1:]
    summary = df_world.iloc[-1, 1:]
    trace1 = go.Scatter(
        x=df_world["Days"],
        y=df_world["Active"],
        mode='markers',
        marker=dict(
            size=10,
            color=df_world["Deaths"],  # set color equal to a variable
            colorscale=a[18]+'_r',
            #colorscale='Electric_r',
            showscale=True
        ),
        hovertemplate=
        '<b>Active Cases</b>: %{y:.0f}' +
        '<br><b>Days</b>: %{x}<br>' +
        '<b>Deaths: %{text}</b><extra></extra>',
        # text = ['Deaths {}'.format(i + 1) for i in range(5)],
        text=df_world["Deaths"],
        name='Active Cases and Deaths',

    )

    dataActive = [trace1]
    layoutActive = go.Layout(
        paper_bgcolor='#dedede' ,
        plot_bgcolor='#dedede',
        transition = dict(
                duration = 700,
                easing = 'cubic-in-out'
            ),
        showlegend=False,
        font=dict(family='Helvetica Neue', size=12, color='#28334A'),
        title="Number of Active Cases and Deaths - " + area,
        xaxis=dict(title='Number of Days since outbreak',fixedrange=True),
        yaxis=dict(title='Number of Active Cases',fixedrange=True)

    )

    marker_size = 8

    trace1 = go.Scatter(
        x=df_world["Days"],
        y=df_world["Reported"],
        mode='markers',
        marker=dict(
            size=marker_size,
            color='#FBDE44',  # set color equal to a variable
            # colorscale='Electric',
            # showscale=True
        ),
        hovertemplate=
        '<b>Reported: </b>: %{y:.0f}' +
        '<br><b>Days</b>: %{x}<br>',
        name='Reported'
    )

    trace2 = go.Scatter(
        x=df_world["Days"],
        y=df_world["Recoveries"],
        mode='markers',
        marker=dict(
            size=marker_size,
            color='#28334A',  # set color equal to a variable
            # colorscale='Electric',
            # showscale=True
        ),
        hovertemplate=
        '<b>Recoveries: </b>: %{y:.0f}' +
        '<br><b>Days</b>: %{x}<br>',
        name='Recovered'
    )

    trace3 = go.Scatter(
        x=df_world["Days"],
        y=df_world["Deaths"],
        mode='markers',
        marker=dict(
            size=marker_size,
            color='#F65058',  # set color equal to a variable
            # colorscale='Electric',
            # showscale=True
        ),
        hovertemplate=
        '<b>Deceased: </b>: %{y:.0f}' +
        '<br><b>Days</b>: %{x}<br>',
        name='Deceased'
    )

    dataThree = [trace1, trace2, trace3]
    layoutThree = go.Layout(
        paper_bgcolor= '#dedede',
        plot_bgcolor='#dedede',

        showlegend=True,
        font=dict(family='Helvetica Neue', size=12, color='#28334A'),
        title="Reported, Recovered and Deceased - " + area,
        xaxis=dict(title='Number of Days since outbreak',fixedrange=True),
        yaxis=dict(title='Number of Cases',fixedrange=True),
        hovermode='x'

    )

    mortalityRate = str(round((summary[1]/summary[0])*100,2))+'%'

    difference = df_world.iloc[-2, 1:]

    change = summary - difference

    if (change[3] > 0):
        new_active = 'UP +' +format(change[3], ",d")
        active_color = '#850000'

    else:
        new_active = 'DOWN ' +format(change[3], ",d")
        active_color = '#00663a'

    if 'Worldwide' not in affected_dict.keys():
        affected_dict['Worldwide'] = summary[0]/7800000000
    pAffected = str(round(affected_dict.get(area,0),4))+'%'

    return(
        go.Figure(data=dataActive, layout=layoutActive),
        go.Figure(data=dataThree, layout=layoutThree),
        format(summary[0],",d"),
        format(summary[2], ",d"),
        format(summary[3], ",d"),
        format(summary[1], ",d"),
        'UP +'+ format(change[0], ",d"),
        'UP +' +format(change[2], ",d"),
        new_active,
        {'text-align': 'center', 'letter-spacing': '3px', 'font-size':12,'font-style':'italic','color':active_color},
        'UP +'+format(change[1], ",d"),
        mortalityRate,
        pAffected
    )

if __name__ == '__main__':
    app.run_server(debug=True)
