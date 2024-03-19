from dash_extensions.enrich import DashProxy, Input, Output, State, NoOutputTransform
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import os
import sys
sys.path.append(os.getcwd())

from src.ui.app_layout import get_layout
from src.ui.app_utils import send_request_threaded


app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[NoOutputTransform()])

app.layout = get_layout()

dir_dict = {"w": "forward", "a": "left", "s": "backward", "d": "right", "None": "Not moving"}


@app.callback(
    Output("direction", "children", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("keyboard_move", "n_keydowns"),
    State("keyboard_move", "keydown"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def move(_, keydown, on):
    if not keydown or not on:
        raise PreventUpdate
    key = keydown["key"].lower()
    path = f"/direction?dir={key}"
    return dir_dict[key].capitalize(), send_request_threaded(path, *params)


@app.callback(
    Output("direction", "children", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("keyboard_move", "n_keyups"),
    State("keyboard_move", "keyup"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def stop_move(_, keyup, on):
    if not keyup or not on:
        raise PreventUpdate
    path = f"/direction?dir=None"
    return "Not moving", send_request_threaded(path, *params)

@app.callback(
    Output("speed", "value", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("keyboard_speed", "n_keydowns"),
    State("keyboard_speed", "keydown"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def change_speed(_, keydown, on):
    if not keydown or not on:
        raise PreventUpdate
    key = keydown["key"]
    path = f"/speed?speed={key}"
    return int(key), send_request_threaded(path, *params)

@app.callback(
    Output("speed", "value", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("power_btn", "on"),
)
def reset_speed(_):
    path = f"/speed?speed=0"
    return 0, send_request_threaded(path, *params)

@app.callback(
    Output("indicator", "children", allow_duplicate=True),
    Input("servo1", "value"),
    Input("servo2", "value"),
    Input("servo3", "value"),
    Input("correction", "value"),
    Input("switch1", "on"),
)
def change_state_params(servo1, servo2, servo3, correction, switch1):
    switch1 = 1 if switch1 else 0
    path = f"/state?servo1={servo1}&servo2={servo2}&servo3={servo3}&correction={correction}"#&switch1={switch1}"
    send_request_threaded(path, *params)
    return ""

# @app.callback(
#     Input("btn1", "n_clicks"),
#     Input("btn2", "n_clicks"),
# )
# def change_click_params(btn1, btn2):
#     if ctx.triggered_id == "btn1":
#         btn1 = 1
#         btn2 = 0
#     elif ctx.triggered_id == "btn2":
#         btn1 = 0
#         btn2 = 1
#     path = f"/click?btn1={btn1}&btn2={btn2}"
#     send_request(path, *params)

# @app.callback(
#     Input("switch1", "on"),
#     prevent_initial_call=True
# )
# def reverse(on):
#     if not on:
#         raise PreventUpdate
#     send_request("/state?servo1=0&servo2=180&servo3=0")
#     send_request("/speed?speed=9")
#     send_request("/direction?dir=w")

# @app.callback(
#     Input("btn1", "n_clicks"),
#     prevent_initial_call=True
# )
# def interrupteur(*_):
#     send_request("/state?servo1=180&servo2=0")

# @app.callback(
#     Input("btn2", "n_clicks"),
#     prevent_initial_call=True
# )
# def porte(*_):
#     send_request("/state?servo2=65") # à vérifier


if __name__ == '__main__':
    send = False
    print_code = True
    print_request = True
    params = (send, print_code, print_request)

    app.run(debug=True, dev_tools_hot_reload=True)

