import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html
import dash_daq as daq
from dash_extensions import EventListener


def get_layout():
    return dbc.Container([
    EventListener(events=[{"event" : "keyup", "props": ["key"]}], id="el_up", logging=True),
    EventListener(events=[{"event" : "keydown", "props": ["key"]}], id="el_down", logging=True),
    dcc.Interval(id="interval", interval=150),
    dbc.Row([
        dbc.Col([
            html.H1("COSMIC")
        ], width=2, align="center", style={"marginBottom" : "30px"}),
    ], justify="center", align="center"),
    dbc.Row([
        dbc.Col([
            html.H4("Speed"),
            daq.Gauge(
                id='speed',
                label="",
                scale={"start": 0, "interval": 1},
                color={"gradient": True, "ranges": {"white": [0,3], "var(--bs-cyan)": [3,6], "var(--bs-blue)": [6,9]}},
                value=0,
                max=9,
            ),
            html.H4("Direction", style={"marginTop" : "30px"}),
            html.H6(
                id='direction',
                children="Not moving",
            ),
            html.H4("Request State", style={"marginTop" : "30px"}),
            html.H6(
                id="indicator",
                children="",
                style={'whiteSpace': 'pre-wrap'}
            ),
        ], width=2, style={"marginRight" : "40px", "textAlign" : "center"}),
        dbc.Col([
            daq.PowerButton(id='power_btn', on=False, size=100, color="var(--bs-blue)", className="power-button"),
            dbc.Button("Button 1", id="btn1", color="primary", className="button", n_clicks=0, size="lg"),
            dbc.Button("Button 2", id="btn2", color="primary", className="button", n_clicks=0, size="lg"),
            html.H4("Switch 1"),
            daq.BooleanSwitch(id='switch1', on=False, color="var(--bs-blue)", className="switch"),
        ], width=2, align="center", style={"marginRight" : "20px", "textAlign" : "center"}),
        dbc.Col([
            html.H4("Servo 1"),
            dcc.Slider(
                id="servo1",
                min=0,
                max=180,
                value=0,
                step=5,
                className="slider",
                updatemode="mouseup",
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
            html.H4("Servo 2"),
            dcc.Slider(
                id="servo2",
                min=0,
                max=180,
                value=0,
                step=5,
                className="slider",
                updatemode="mouseup",
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
            html.H4("Servo 3"),
            dcc.Slider(
                id="servo3",
                min=0,
                max=95,
                value=0,
                step=5,
                className="slider",
                updatemode="mouseup",
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
        ], width=5, style={"marginRight" : "20px"}),
        dbc.Col([
            html.H4("Correction"),
            dcc.Slider(
                id="correction",
                min=0.1,
                max=2,
                value=1,
                step=0.01,
                className="vertical-slider",
                updatemode="mouseup",
                marks=None,
                tooltip={"always_visible": True, "placement": "right"},
                vertical=True,
                verticalHeight=500,
            ),
        ], width=2),
    ]),
    html.Div(id="dummy_input", style={"display" : "none"}),
], fluid=True, style={"marginTop" : "50px"})

