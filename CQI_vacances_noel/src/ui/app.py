from dash_extensions.enrich import DashProxy, Input, Output, State, ctx, NoOutputTransform
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import threading
import os
import sys
sys.path.append(os.getcwd())

from src.ui.app_layout import get_layout
from src.ui.app_utils import send_request_threaded


app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], transforms=[NoOutputTransform()])

app.layout = get_layout()

dir_dict = {"w": "forward", "a": "left", "s": "backward", "d": "right", "None": "Not moving"}

@app.callback(
    Output("el_up", "event", allow_duplicate=True),
    Output("direction", "children", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("el_down", "event"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def move(el_down, on):
    if not el_down or not on:
        raise PreventUpdate
    
    key = el_down["key"].lower()
    if key not in {"a", "s", "d", "w"}: raise PreventUpdate

    path = f"/direction?dir={key}"
    message = send_request_threaded(path, **params)
    return None, dir_dict[key].capitalize(), message

@app.callback(
    Output("el_down", "event", allow_duplicate=True),
    Output("direction", "children", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("el_up", "event"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def stop_move(el_up, on):
    if not el_up or not on:
        raise PreventUpdate
    key = el_up["key"].lower()
    if key not in {"a", "s", "d", "w"}:
        raise PreventUpdate
    path = f"/direction?dir={None}"
    message = send_request_threaded(path, **params)
    return None, "Not moving", message

@app.callback(
    Output("speed", "value", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("el_down", "event"),
    Input("dummy_input", "children"), # never triggers but prevents error
    State("power_btn", "on"),
    prevent_initial_call=True
)
def change_speed(el_down, _, on):
    if not el_down or not on:
        raise PreventUpdate
    key = el_down["key"]
    if not key.isdigit():
        raise PreventUpdate
    path = f"/speed?speed={key}"
    message = send_request_threaded(path, **params)
    return int(key), message

@app.callback(
    Output("speed", "value", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("power_btn", "on"),
)
def reset_speed(on):
    path = f"/speed?speed=0"
    message = send_request_threaded(path, **params)
    return 0, message

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
    message = send_request_threaded(path, **params)
    return message

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
    params = dict(
        send=send,
        print_code=print_code,
        print_request=print_request
    )
    app.run(debug=True, dev_tools_hot_reload=True)

