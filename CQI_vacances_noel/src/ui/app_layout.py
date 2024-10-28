import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html
import dash_daq as daq
from dash_extensions import Keyboard
import datetime


layout = dbc.Container([
    Keyboard(id="keyboard_move", captureKeys=["w", "a", "s", "d", "W", "A", "S", "D"], eventProps=["key"], n_keydowns=0),
    Keyboard(id="keyboard_speed", captureKeys=[str(i) for i in range(1, 10)], eventProps=["key"], n_keydowns=0),
    Keyboard(id="keyboard_switch", captureKeys=["u", "U"], eventProps=["key"], n_keydowns=0),
    Keyboard(id="keyboard_servo", captureKeys=["g", "G", "h", "H"], eventProps=["key"], n_keydowns=0),
    Keyboard(id="keyboard_slice", captureKeys=["k", "K", "l", "L"], eventProps=["key"], n_keydowns=0),
    dbc.Row([
        dbc.Col([
            html.H1("CHRONOS")
        ], width=1, align="center"),
        dbc.Col([
            html.Img(id="logo", src="assets/logo2025.png", className="logo", draggable="true")
        ], width=1, align="center", style={"marginBottom" : "0px"}),
    ], justify="center", align="center"),
    dbc.Row([
        dbc.Col([
            html.H4("Vitesse (1-9)"),
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
            html.H4("État des requêtes", style={"marginTop" : "30px"}),
            html.H6(
                id="indicator",
                children="",
                style={'whiteSpace': 'pre-wrap'  }
            ),
        ], width=2, style={"marginRight" : "40px", "textAlign" : "center"}),
        dbc.Col([
            daq.PowerButton(id='power_btn', on=False, size=100, className="power-button", color="var(--color3)"),
            dbc.Button("Lame bas (k)", id="slice_up", className="button", n_clicks=0, size="lg"),
            dbc.Button("Lame haut (l)", id="slice_down", className="button", n_clicks=0, size="lg"),
        ], width=2, align="center", style={"marginRight" : "20px", "textAlign" : "center"}),
        dbc.Col([
            html.H4("Pince gauche (g ←→)"),
            dcc.Slider(
                id="servo1",
                min=70,
                max=165,
                value=165,
                step=5,
                className="slider",
                updatemode="mouseup",
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
            html.H4("Pince droite (h ←→)"),
            dcc.Slider(
                id="servo2",
                min=70,
                max=165,
                value=170,
                step=5,
                className="slider",
                updatemode="mouseup",
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
            html.H4("Voyage dans le temps (F10)"),
            dcc.DatePickerSingle(date=datetime.datetime(2002, 9, 26, 15, 27), style={"border-color": "black"}),
            dbc.Button("Voyager", id="voyage", className="button-sm")
        ], width=5, style={"marginRight" : "20px"}, align="center"),
        dbc.Col([
            html.H4("Balancement"),
            dcc.Slider(
                id="correction",
                min=-7,
                max=7,
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

