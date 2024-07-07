from typing import List, Any

from dash import Dash, html
import dash_bootstrap_components as dbc

from . import config as cfg

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

if cfg.ENV == "PROD":
    app.config.suppress_callback_exceptions = True


def layout() -> html.Div:
    return dbc.Container([
        html.H1("Bridge Simulator"),
        html.H3("By Atticus Martin-King Tan"),
        html.Hr(),
    ])


app.layout = layout


def main():
    import logging
    logging.basicConfig(level=logging.INFO)

    app.run_server(debug=False, host=cfg.HOST, port=cfg.PORT)


if __name__ == "__main__":
    main()
