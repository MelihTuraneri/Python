import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv("pages/cleared_laptop_data.csv")

dash.register_page(__name__, path='/Screen-Size', name='Screen Size')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                    html.H2('Number of advertisements for each screen size', className='card-title text-center mb-4'),
                    dbc.Row([
                        dbc.Col([
                        dcc.Dropdown(id='screens_chosen', multi=True, value=['14 inç', '15,6 inç', '13 inç', '17,3 inç',],
                                    style={"color": "#000000"}, className='fs-5 mb-2',
                                        options=[{'label': html.Span(x, style={'color': 'Black'}, className='text-center'), 'value': x}
                                                    for x in sorted(df["Ekran Boyutu"].unique())]),
                        ],width=6),
                        dbc.Col([
                            html.H6("Why it's not happening?", id='hover-target', className='text-decoration-underline text-danger'),
                            dbc.Popover([
                                dbc.PopoverHeader("Choose screen sizes!!", className=''),
                                dbc.PopoverBody("Choose screen size to print them on chart!!"),
                            ],
                                id="popover",
                                placement="bottom",
                                target="hover-target",
                                trigger="hover",
                            )
                        ],width=3),
                    ]),
                    dcc.Loading(children=[dbc.Card(dcc.Graph(id='my-bar2', figure={}), body=True, color="dark")], color="#3D76DA", type="cube"),
            ], class_name='bg-dark'),
        ])
    ])
])

@callback(
    Output('my-bar2', 'figure'),
    Input('screens_chosen', 'value')
)

def update_graph(value):
    dff = df.query(f'`Ekran Boyutu` == {value}')
    fig = px.histogram(dff, x='Ekran Boyutu', color='Marka',title='Ekran Boyutu', 
                       width=1200, height=600).update_layout(showlegend=True, title_x=0.5, 
                                                             yaxis_title="İlan Sayısı",
                                                             font=dict(
                                                                    size=18
                                                                )
    )
    return fig