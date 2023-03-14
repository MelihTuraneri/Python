import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv("pages/cleared_laptop_data.csv")

dash.register_page(__name__, path='/', name='Home')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2('Percentage distribution of laptop advertisements', className='card-title text-center mb-4 mt-4'),
                dbc.CardBody(
                    dcc.Graph(id='my-pie', figure=px.pie(df, names='Marka', height=650).update_traces(textposition='inside', textinfo='percent+label')),
                     class_name='bg-dark', style={'height' : '36rem'}
                )
            ], class_name='bg-dark', style={'height' : '36rem'})
        ], xs=12, sm=12, md=12, lg=12, xl=12, xxl=12)
    ])
])