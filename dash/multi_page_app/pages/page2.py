import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv("pages/cleared_laptop_data.csv")

dash.register_page(__name__, path='/Brands', name='Brands')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                    html.H2('Number of advertisements for brands', className='card-title text-center mb-4'),
                    dbc.Row([
                        dbc.Col([
                        dcc.Dropdown(id='brands_chosen', multi=True, value=["Asus", "Acer", "Dell", "Apple", "MSI"],
                                    style={"color": "#000000"}, className='fs-5 mb-2',
                                        options=[{'label': html.Span(x, style={'color': 'Black'}, className='text-center'), 'value': x}
                                                    for x in sorted(df["Marka"].unique())]),
                        ],width=6),
                        dbc.Col([
                            html.H6("Why it's not happening?", id='hover-target', className='text-decoration-underline text-danger'),
                            dbc.Popover([
                                dbc.PopoverHeader("Choose brands!!", className=''),
                                dbc.PopoverBody("Choose brands to print them on chart!!"),
                            ],
                                id="popover",
                                placement="bottom",
                                target="hover-target",
                                trigger="hover",
                            )
                        ],width=3),
                    ]),
                    dcc.Loading(children=[dbc.Card(dcc.Graph(id='my-bar', figure={}), body=True, color="dark")], color="#3D76DA", type="cube"),
            ], class_name='bg-dark'),
        ], xs=12, sm=12, md=8, lg=12, xl=12, xxl=12)
    ])
])

@callback(
    Output('my-bar', 'figure'),
    Input('brands_chosen', 'value')
)

def update_graph(value):
    dff = df.query(f'Marka=={value}')
    fig = px.histogram(dff, x='Marka', color='Site',title='Marka').update_layout(showlegend=True, title_x=0.5, 
                                                                                    yaxis_title="İlan Sayısı",
                                                                                    font=dict(
                                                                                        size=18
                                                                                    )
    )
    return fig