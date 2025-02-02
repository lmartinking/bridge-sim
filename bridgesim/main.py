from typing import List, Any

import math
import base64

from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc

from . import config as cfg

from .generator import generate_bridge_svg

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

if cfg.ENV == "PROD":
    app.config.suppress_callback_exceptions = True


def layout() -> html.Div:
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Truss Bridge Simulator")),
            dbc.Col(html.H3("By Atticus Martin-King Tan"), style={'text-align': 'right', 'padding-top': '12px'}),
        ]),

        html.Div([
            dbc.Row([
                dbc.Label("Bridge Span (metres)", html_for='bridge-width', width=2),
                dbc.Col(dcc.Slider(min=10, max=50, step=1, value=10, id='bridge-width'), width=10)
            ]),
            dbc.Row([
                dbc.Label("Bridge Height (metres)", html_for='bridge-height', width=2),
                dbc.Col(dcc.Slider(min=1, max=5, step=0.5, value=1, id='bridge-height'), width=10)
            ]),
            dbc.Row([
                dbc.Label("Number of Triangles", html_for='bridge-triangles', width=2),
                dbc.Col(dcc.Slider(min=3, max=25, step=2, value=3, id='bridge-triangles'), width=10)
            ]),
            dbc.Row([
                dbc.Label("Bridge Load (kN)", html_for='bridge-load', width=2),
                dbc.Col(dcc.Slider(min=0, max=2, step=0.1, value=0.0, id='bridge-load'), width=10)
            ]),
        ], className='mb-3'),

        html.Div(id='bridge'),

        html.Hr(),

        html.Div([
            dbc.Row([
                dbc.Col(html.A("Source Code", href="https://github.com/lmartinking/bridge-sim")),
                dbc.Col(html.P("Made with ❤️ by Atticus & Dad", style={'text-align': 'right'}))
            ])
        ], className='mb-3')
    ])


@app.callback(
    Output('bridge', 'children'),
    Input('bridge-width', 'value'),
    Input('bridge-height', 'value'),
    Input('bridge-triangles', 'value'),
    Input('bridge-load', 'value')
)
def render_bridge(width, height, truss_triangles, load):
    load = float(load)
    width = float(width)
    height = float(height)
    truss_elements = math.ceil(truss_triangles / 2)  # Convert triangles to "elements"

    svg = generate_bridge_svg(width, height, truss_elements, load)
    svg_encoded = base64.b64encode(svg).decode('ascii')

    return [
        html.Img(src=f"data:image/svg+xml;base64,{svg_encoded}", style={'width': '100%'})
    ]


app.layout = layout
app.title = "Truss Bridge Simulator"


def main():
    import logging
    logging.basicConfig(level=logging.INFO)

    is_dev = cfg.ENV != "PROD"

    app.run_server(debug=is_dev, host=cfg.HOST, port=cfg.PORT, dev_tools_ui=is_dev, dev_tools_hot_reload=is_dev)


if __name__ == "__main__":
    main()
