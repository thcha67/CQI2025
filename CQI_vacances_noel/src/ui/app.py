from dash import Dash, html, Input, Output, State, ctx, dcc, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import requests
import dash_daq as daq
from dash_extensions import EventListener


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

drag_mode = "mouseup"

url = "http://192.168.4.1"

state = {"move": {"w" : False, "a": False, "s": False, "d": False}, 
        "speed": 0, "servo1": None, "servo2": None, "servo3": None, "correction": 1
    }

app.layout = dbc.Container([
    EventListener(events=[{"event" : "keyup", "props": ["key"]}], id="el_up", logging=True),
    EventListener(events=[{"event" : "keydown", "props": ["key"]}], id="el_down", logging=True),
    dcc.Interval(id="interval", interval=50),
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
                value=0,
                max=9,
            ),
            html.H4("Direction"),
            html.H6(
                id='direction',
                children="Not moving",
            ),
        ], width=2),
        dbc.Col([
            dbc.Button("Button 1", id="btn1", color="primary", className="button", n_clicks=0, size="lg"),
            dbc.Button("Button 2", id="btn2", color="primary", className="button", n_clicks=0, size="lg"),
            dbc.Button("STOP", id="stop", color="danger", className="stop-button")
        ], width=2, align="center"),
        dbc.Col([
            html.H4("Servo 1"),
            dcc.Slider(
                id="servo1",
                min=0,
                max=180,
                value=0,
                step=3,
                className="slider",
                updatemode=drag_mode,
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
                updatemode=drag_mode,
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
            html.H4("Servo 3"),
            dcc.Slider(
                id="servo3",
                min=0,
                max=95,
                value=0,
                step=3,
                className="slider",
                updatemode=drag_mode,
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
        ], width=6),
        dbc.Col([
            html.H4("Correction"),
            dcc.Slider(
                id="correction",
                min=0.1,
                max=2,
                value=1,
                step=0.01,
                className="vertical-slider",
                updatemode=drag_mode,
                marks=None,
                tooltip={"always_visible": True, "placement": "right"},
                vertical=True,
                verticalHeight=500,
            ),
        ], width=2),
    ]),
    html.Div(id='output', style={"display": "none"}),
    daq.Indicator(
        id="indicator",
        label="No request yet",
        labelPosition="right",
        value=True,
        color="white",
        ),
    dcc.Store(id="store", data=state)
], fluid=True, style={"marginTop" : "50px"})


move_keys =  state["move"].keys()

@app.callback(
    Output("store", "data", allow_duplicate=True),
    Output("el_up", "event", allow_duplicate=True),
    Input("el_down", "event"),
    State("store", "data"),
    prevent_initial_call=True
)
def start_to_move(el_down, store):
    if not el_down:
        raise PreventUpdate
    for command in move_keys: # mettre toutes les directions à False
        store["move"][command] = False
    direction_key = el_down["key"]
    if direction_key not in move_keys:
        raise PreventUpdate
    store["move"][direction_key] = True
    return store, None


@app.callback(
    Output("store", "data", allow_duplicate=True),
    Output("el_down", "event", allow_duplicate=True),
    Input("el_up", "event"),
    State("store", "data"),
    prevent_initial_call=True
)
def stop_move(el_up, store):
    if not el_up:
        raise PreventUpdate
    direction_key = el_up["key"]
    if direction_key not in move_keys:
        raise PreventUpdate
    store["move"][direction_key] = False
    return store, None


@app.callback(
    Output("store", "data", allow_duplicate=True),
    Input("el_down", "event"),
    Input("el_up", "event"), # ajouté parce deux callbacks ne peuvent pas avoir les mêmes inputs
    State("store", "data"),
    prevent_initial_call=True
)
def change_speed(el_down, dummy, store):
    if not el_down or ctx.triggered_id == "el_up":
        raise PreventUpdate
    speed = el_down["key"]
    if not speed.isdigit():
        raise PreventUpdate # détecter si un chiffre pour voir si c'est une vitesse
    store["speed"] = int(speed)
    return store




direction_dict = {"w": "forward", "a": "left", "s": "backward", "d": "right"}

@app.callback(
    Output("indicator", "label", allow_duplicate=True),
    Output("indicator", "color", allow_duplicate=True),
    Output("speed", "value", allow_duplicate=True),
    Output("direction", "children", allow_duplicate=True),
    Input("interval", "n_intervals"),
    State("store", "data"),
    prevent_initial_call=True
)
def send_request(n, store):
    template = "/patate?direction={0}&servo1={1}&servo2={2}&servo3={3}&speed={4}&correction={5}&request_count={6}"
    direction_key = next((key for key, value in store["move"].items() if value), None)
    direction = direction_dict.get(direction_key, None)
    request = url + template.format(
        direction,
        store["servo1"], store["servo2"], store["servo3"], store["speed"], store["correction"], n
    )

    color = "red"
    message = "Debug"
    # try:
    #     #print(request)
    #     requests.get(request, timeout=1)
    #     message = "Request Sent"
    #     color = "green"
    # except requests.exceptions.ConnectTimeout:
    #     message = "Request Timeout"
    # except requests.exceptions.ReadTimeout:
    #     message = "Read Timeout"
    # except Exception:
    #     message = "Unknown Request Error"
    
    displayed_speed = store["speed"]
    displayed_direction = direction.capitalize() if direction else "Not moving"

    return message, color, displayed_speed, displayed_direction




if __name__ == '__main__':
    app.run_server(debug=True)
