import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html
import dash_daq as daq
from dash_extensions import Keyboard


layout = dbc.Container([
    Keyboard(id="keyboard_move", captureKeys=["w", "a", "s", "d", "W", "A", "S", "D"], eventProps=["key"], n_keydowns=0),
    Keyboard(id="keyboard_speed", captureKeys=[str(i) for i in range(1, 10)], eventProps=["key"], n_keydowns=0),
    Keyboard(id="keyboard_switch", captureKeys=["u", "U"], eventProps=["key"], n_keydowns=0),
    Keyboard(id="keyboard_servo", captureKeys=["j", "J", "k", "K", "l", "L"], eventProps=["key"], n_keydowns=0),
    dbc.Row([
        dbc.Col([
            html.H1("COSMIC")
        ], width=1, align="center"),
        dbc.Col([
            html.Img(id="logo", src="assets/logo2025.png", className="logo", draggable="true")
        ], width=1, align="center", style={"marginBottom" : "0px"}),
    ], justify="center", align="center"),
    dbc.Row([
        dbc.Col([
            html.H4("Speed (1-9)"),
            daq.Gauge(
                id='speed',
                size=200,
                showCurrentValue=True,
                label="",
                scale={"start": 1, "interval": 1},
                color={"gradient": True, "ranges": {"white": [1,3], "var(--color1)": [3,6], "var(--color3)": [6,9]}},
                value=5,
                min=1,
                max=9,
            ),
            html.H4("Direction (w-a-s-d)", style={"marginTop" : "30px"}),
            html.H1(
                id='direction',
                children="·",
                style={"textWeight" : "bold"}
            ),
            html.H4("Request State", style={"marginTop" : "30px"}),
            html.H6(
                id="indicator",
                children="",
                style={'whiteSpace': 'pre-wrap'}
            ),
        ], width=2, style={"marginRight" : "40px", "textAlign" : "center"}),
        dbc.Col([
            daq.PowerButton(id='power_btn', on=False, size=100, className="power-button", color="var(--color3)"),
            dbc.Button("Ouvrir interrupteur", id="btn1", className="button", n_clicks=0, size="lg"),
            dbc.Button("Porte", id="btn2", className="button", n_clicks=0, size="lg"),
            html.H4("Attach (u)"),
            daq.BooleanSwitch(id='switch', on=False, className="switch", color="var(--color3)"),
        ], width=2, align="center", style={"marginRight" : "20px", "textAlign" : "center"}),
        dbc.Col([
            html.H4("Servo 1 (j ←→)"),
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
            html.H4("Servo 2 (k ←→)"),
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
            html.H4("Servo 3 (l ←→)"),
            dcc.Slider(
                id="servo3",
                min=0,
                max=180,
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
                min=-10,
                max=10,
                value=0,
                step=1,
                className="vertical-slider",
                updatemode="mouseup",
                marks=None,
                tooltip={"always_visible": True, "placement": "right"},
                vertical=True,
                verticalHeight=500,
            ),
        ], width=2),
    ]),
], fluid=True)

