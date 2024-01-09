from dash_extensions.enrich import DashProxy, html, Input, Output, State, ctx, dcc, CycleBreakerTransform, NoOutputTransform
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import requests
import dash_daq as daq
from dash_extensions import EventListener
from time import time


app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[CycleBreakerTransform(), NoOutputTransform()])

drag_mode = "mouseup"

url = "http://192.168.4.1"
template = "/patate?direction={0}&servo1={1}&servo2={2}&servo3={3}&speed={4}&correction={5}&request_count={6}&btn1={7}&btn{2}"

state = {"move": {"w" : False, "a": False, "s": False, "d": False}, 
        "speed": 0, "servo1": 0, "servo2": 0, "servo3": 0, "correction": 1, "btn1": 0, "btn2": 0
    }

direction_dict = [0, 0, 0, 0]

app.layout = dbc.Container([
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
                color={"gradient": True, "ranges": {"green": [0,3], "yellow": [3,6], "red": [6,9]}},
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
                children="No request yet",
                style={'whiteSpace': 'pre-wrap'}
            ),
        ], width=2),
        dbc.Col([
            dbc.Button("Start", id="start", color="primary", className="button", n_clicks=0, size="lg"),
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
                step=5,
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
                step=5,
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
    html.Div(id='request_ok', style={"display": "none"}),
    html.Div(id="dummy_input1", style={"display": "none"}),
    html.Div(id="dummy_input2", style={"display": "none"}),
    dcc.Store(id="store", data=state),
    dcc.Store(id="time_store", data=time(), storage_type="memory"),
    dcc.Store(id="power", data=0, storage_type="memory"),
    dcc.Store(id="direction", data=direction_dict)
], fluid=True, style={"marginTop" : "50px"})

# @app.callback(
#     Output("power", "data", allow_duplicate=True),
#     Input("start", "n_clicks"),
#     prevent_initial_call=True)
# def send_start_time(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     return 1

# w a s d -> forward left backward right
move_dict = {"w": (1, 0, 0, 0), "a": (0, 1, 0, 0), "s": (0, 0, 1, 0), "d": (0, 0, 0, 1)}
direction_dict = {"w": "forward", "a": "left", "s": "backward", "d": "right"}

@app.callback(
    Output("el_up", "event", allow_duplicate=True),
    Input("el_down", "event"),
    prevent_initial_call=True
)
def move(el_down):
    if not el_down:
        raise PreventUpdate
    key = el_down["key"]
    if key not in {"a", "s", "d", "w"}:
        raise PreventUpdate
    direction = direction_dict[key]
    request = url + template.format(
        direction,
        0, 0, 0, 
        9, 1, 0, 
        0, 0
    )
    print(direction)
    r = requests.get(request)
    return None

@app.callback(
    Output("el_down", "event", allow_duplicate=True),
    Input("el_up", "event"),
    prevent_initial_call=True
)
def stop_move(el_up):
    if not el_up:
        raise PreventUpdate
    key = el_up["key"]
    if key not in {"a", "s", "d", "w"}:
        raise PreventUpdate
    request = url + template.format(
        None,
        0, 0, 0, 
        9, 1, 0, 
        0, 0
    )
    print("none")
    r = requests.get(request)
    return None




# move_keys =  state["move"].keys()

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Output("el_up", "event", allow_duplicate=True),
#     Input("el_down", "event"),
#     State("store", "data"),
#     prevent_initial_call=True
# )
# def start_to_move(el_down, store):
#     if not el_down:
#         raise PreventUpdate
#     for command in move_keys: # mettre toutes les directions à False
#         store["move"][command] = False
#     direction_key = el_down["key"]
#     if direction_key not in move_keys:
#         raise PreventUpdate
#     store["move"][direction_key] = True
#     return store, None

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Output("el_down", "event", allow_duplicate=True),
#     Input("el_up", "event"),
#     State("store", "data"),
#     prevent_initial_call=True
# )
# def stop_move(el_up, store):
#     if not el_up:
#         raise PreventUpdate
#     direction_key = el_up["key"]
#     if direction_key not in move_keys:
#         raise PreventUpdate
#     store["move"][direction_key] = False
#     return store, None

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Input("el_down", "event"),
#     Input("dummy_input2", "children"),
#     State("store", "data"),
#     prevent_initial_call=True
# )
# def change_speed(el_down, dummy, store):
#     if not el_down:
#         raise PreventUpdate
#     speed = el_down["key"]
#     if not speed.isdigit():
#         print(speed)
#         raise PreventUpdate # détecter si un chiffre pour voir si c'est une vitesse
#     store["speed"] = int(speed)
#     print("ok")
#     return store

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Input("btn1", "n_clicks"),
#     State("store", "data"),
#     State("interval", "n_intervals"),
# )
# def btn1(n_clicks, store, n_intervals):
#     if n_clicks is None:
#         raise PreventUpdate
#     store["btn1"] = n_intervals
#     return store

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Input("btn2", "n_clicks"),
#     State("store", "data"),
# )
# def btn1(n_clicks, store):
#     if n_clicks is None:
#         raise PreventUpdate
#     store["btn2"] = 1

#     return store

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Input("servo1", "value"),
#     State("store", "data"),
#     prevent_initial_call=True
# )
# def change_servo1_click(servo1, store):
#     store["servo1"] = servo1
#     return store

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Input("servo2", "value"),
#     State("store", "data"),
#     prevent_initial_call=True
# )
# def change_servo2_click(servo2, store):
#     store["servo2"] = servo2
#     return store

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Input("servo3", "value"),
#     State("store", "data"),
#     prevent_initial_call=True
# )
# def change_servo3_click(servo3, store):
#     store["servo3"] = servo3
#     return store

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Input("correction", "value"),
#     State("store", "data"),
#     prevent_initial_call=True
# )
# def change_correction_click(correction, store):
#     store["correction"] = correction
#     return store

# @app.callback(
#     Output("store", "data", allow_duplicate=True),
#     Output("power", "data", allow_duplicate=True),
#     Output("speed", "value", allow_duplicate=True),
#     Output("direction", "children", allow_duplicate=True),
#     Input("stop", "n_clicks"),
#     prevent_initial_call=True)
# def stop(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     return state, 0, 0, "Not moving"


# direction_dict = {"w": "forward", "a": "left", "s": "backward", "d": "right"}

# @app.callback(
#     Output("indicator", "children", allow_duplicate=True),
#     Output("speed", "value", allow_duplicate=True),
#     Output("direction", "children", allow_duplicate=True),
#     Output("store", "data", allow_duplicate=True),
#     Input("start", "n_clicks"),
#     Input("interval", "n_intervals"),
#     State("store", "data"),
#     State("power", "data"),
#     prevent_initial_call=True
# )
# def send_request(n_clicks, n_intervals, store, power):
#     if ctx.triggered_id == "start":
#         if n_clicks is None or n_clicks != 1 or power == 1:
#             raise PreventUpdate
#     if ctx.triggered_id == "interval":
#         if power == 0:
#             raise PreventUpdate
#     #print(store)
#     # btn1 = 0
#     # if n_intervals - store["btn1"] < 4:
#     #     btn1 = 1
#     # print(n_intervals, store["btn1"], btn1)
#     direction_key = next((key for key, value in store["move"].items() if value), None)
#     direction = direction_dict.get(direction_key, None)
#     speed = store["speed"]
#     request = url + template.format(
#         direction,
#         store["servo1"], store["servo2"], store["servo3"], 
#         speed, store["correction"], n_intervals, 
#         0, 0
#     )
#     message = "Debug"
#     try:
#         #print("sent", n_intervals)
#         r = requests.get(request, timeout=0.5)
#         #print("receivec", r.text)
#         message = "Request Sent"
#     except requests.exceptions.ConnectTimeout:
#         message = "Request Timeout"
#     except requests.exceptions.ReadTimeout:
#         message = "Read Timeout"
#     except requests.exceptions.ConnectionError:
#         message = "Connection Error \n" + f"Request #{n_intervals}"
#     except Exception as e:
#         message = str(e.__context__)
    
#     displayed_speed = store["speed"]
#     displayed_direction = direction.capitalize() if direction else "Not moving"


#     return message, displayed_speed, displayed_direction, store



if __name__ == '__main__':
    app.run_server(debug=True)
