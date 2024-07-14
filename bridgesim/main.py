from typing import List, Any

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
        html.H1("Bridge Simulator"),
        html.H3("By Atticus Martin-King Tan"),
        
        html.Hr(),
        
        html.Div([
            dbc.Row([
                dbc.Label("Bridge Width (metres)", html_for='bridge-width', width=2),
                dbc.Col(dcc.Slider(min=10, max=50, step=1, value=10, id='bridge-width'), width=10)
            ]),
            dbc.Row([
                dbc.Label("Bridge Height (metres)", html_for='bridge-height', width=2),
                dbc.Col(dcc.Slider(min=1, max=5, step=0.5, value=1, id='bridge-height'), width=10)
            ]),
            dbc.Row([
                dbc.Label("Bridge Truss Elements", html_for='bridge-truss-elements', width=2),
                dbc.Col(dcc.Slider(min=3, max=10, step=1, value=3, id='bridge-truss-elements'), width=10)
            ]),
            dbc.Row([
                dbc.Label("Bridge Load (kN)", html_for='bridge-load', width=2),
                dbc.Col(dcc.Slider(min=0, max=1, step=0.1, value=0.0, id='bridge-load'), width=10)
            ]),
        ], className='mb-3'),

        html.Hr(),

        html.Div(id='bridge')
    ])


@app.callback(
    Output('bridge', 'children'),
    Input('bridge-width', 'value'),
    Input('bridge-height', 'value'),
    Input('bridge-truss-elements', 'value'),
    Input('bridge-load', 'value')
)
def render_bridge(width, height, truss_elements, load):
    load = float(load)
    width = float(width)
    height = float(height)
    truss_elements = int(truss_elements)

    svg = generate_bridge_svg(width, height, truss_elements, load)
    svg_encoded = base64.b64encode(svg).decode('ascii')

    return [
        html.Img(src=f"data:image/svg+xml;base64,{svg_encoded}", style={'width': '100%'})
    ]


app.layout = layout


def main():
    import logging
    logging.basicConfig(level=logging.INFO)

    is_dev = cfg.ENV != "PROD"

    app.run_server(debug=is_dev, host=cfg.HOST, port=cfg.PORT, dev_tools_ui=is_dev, dev_tools_hot_reload=is_dev)


if __name__ == "__main__":
    main()
