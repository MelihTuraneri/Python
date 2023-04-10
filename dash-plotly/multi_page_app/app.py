import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Huge thanks to Charming Data link:https://www.youtube.com/@CharmingData

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO], title='DashBoard', suppress_callback_exceptions=True, use_pages=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

sidebar = dbc.Card([
    dbc.CardBody([
        html.H3('Charts', className='text-center card-title mt-2 mb-3'),
        html.Hr(style={"borderWidth": "0.5vh", "width": "100%", "borderColor": "#F3DE8A", "opacity": "unset"}),
        dbc.Nav([
            dbc.NavLink([
                 html.Div(page["name"], className="ms-2 text-center"),
            ],
                href=page["path"],
                active="exact",
            )
            for page in dash.page_registry.values()
        ],  
                vertical=True,
                pills=True,
                class_name='bg-opacity-50 bg-dark'
        )
    ])
], class_name='bg-dark bg-opacity-25')


app.layout = dbc.Container([
    dbc.Row([
        html.H1('Scraped Laptop Data Dashboard', className='text-center card-title mt-3 mb-5 bg-opacity-25'),
    ]),
    dbc.Row([
        dbc.Col(sidebar, xs=12, sm=12, md=12, lg=2, xl=2),
        dbc.Col([
            dash.page_container
        ], xs=12, sm=12, md=12, lg=10, xl=10, xxl=10)
    ])    
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug = True, port = 3000)
