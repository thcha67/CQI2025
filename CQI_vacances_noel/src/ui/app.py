from dash import Dash, html, Input, Output, State, ctx, dcc, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import requests
import dash_daq as daq
from dash_extensions import EventListener


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

drag_mode = "mouseup"

url = "http://192.168.4.1"


app.layout = dbc.Container([
    EventListener(events=[{"event" : "keyup", "props": ["key"]}], id="el_up", logging=True),
    EventListener(events=[{"event" : "keydown", "props": ["key"]}], id="el_down", logging=True),
    dcc.Interval(id="interval", interval=10),
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
        )
], fluid=True, style={"marginTop" : "50px"})


# @app.callback(
#     Output("speed", "value"),
#     Input("stop", "n_clicks"),
#     prevent_initial_call=True
# )
# def stop(stop):
#     return 0


# @app.callback(
#     Output("indicator", "label", allow_duplicate=True),
#     Output("indicator", "color", allow_duplicate=True),
#     Output("speed", "value", allow_duplicate=True),
#     Input("el_up", "event"),
#     Input("pince", "value"),
#     Input("flip", "value"),
#     Input("up_down", "value"),
#     Input("correction", "value"),
#     State("speed", "value"),
#     prevent_initial_call=True
# )
# def send_request(events, pince, flip, up_down, correction, speed):
#     if not events:
#         raise PreventUpdate
#     key = events["key"]
#     if key in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}:
#         speed = key
#     query_string = "/patate?key={0}"#&pince={1}&flip={2}&up_down={3}&speed={4}&correction={5}"
#     request = url + query_string.format(key)#, pince, flip, up_down, speed, correction)
#     try:
#         req = requests.get(request, timeout=1)
#         return "Request Sent", "green", int(speed)
#     except requests.exceptions.ConnectTimeout:
#         print(int(speed))
#         return "Request Timeout ", "red", no_update
#     except requests.exceptions.ReadTimeout:
#         return "Read Timeout", "red", no_update
#     except Exception as e:
#         print(e)
#         return "Unknown Request Error", "red", no_update

key_dict = {
    "a": "left",
    "d": "right",
    "w": "forward",
    "s": "backward"
}

@app.callback(
    Output("indicator", "label", allow_duplicate=True),
    Output("indicator", "color", allow_duplicate=True),
    Output("speed", "value", allow_duplicate=True),
    Input("interval", "n_intervals"),
    Input("el_up", "event"),
    State("el_down", "event"),
    State("speed", "value"),
    State("servo1", "value"),
    State("servo2", "value"),
    State("servo3", "value"),
    State("correction", "value"),
    prevent_initial_call=True
)
def send_request(n_intervals, events_up, events_down, speed, servo1, servo2, servo3, correction):
    request = "/patate?direction={0}&servo1={1}&servo2={2}&servo3={3}&speed={4}&correction={5}"
    if ctx.triggered_id == "interval":
        if not events_down:
            raise PreventUpdate
        key_down = events_down["key"]
        if key_down in key_dict:
            direction = key_dict[key_down]
            request = url + request.format(direction, servo1, servo2, servo3, speed, correction)
        else:
            raise PreventUpdate
    else:
        if not events_up:
            raise PreventUpdate
        key_up = events_up["key"]
        if events_down.get("key") != key_up:
            raise PreventUpdate
        else:
            request = url + request.format(None, servo1, servo2, servo3, speed, correction)
    try:
        requests.get(request, timeout=1)
        return "Request Sent", "green", int(speed)
    except requests.exceptions.ConnectTimeout:
        return "Request Timeout ", "red", no_update
    except requests.exceptions.ReadTimeout:
        return "Read Timeout", "red", no_update
    except Exception as e:
        return "Unknown Request Error", "red", no_update






if __name__ == '__main__':
    app.run_server(debug=True)
