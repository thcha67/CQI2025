import os, sys
sys.path.append(os.getcwd())

from dash_extensions.enrich import DashProxy, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import requests

from src.ui.app_layout import layout


DIR_DICT = {"w": "↑", "a": "←", "s": "↓", "d": "→", "None": "·"}
URL = "http://192.168.4.1"

app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = layout


def send_request(path, send=True, print_request=True):
    if print_request:
        print(path)
    if not send: # Disable request for debug
        return "Requesting disabled"
    try:
        code = requests.get(URL + path, timeout=0.5)
        return "Request Success"
    except requests.exceptions.ConnectTimeout:
        message = "Request Timeout"
    except requests.exceptions.ReadTimeout:
        message = "Read Timeout"
    except requests.exceptions.ConnectionError:
        message = "Connection Error"
    except Exception as e:
        message = "Error cause: " + str(e.__cause__)
    return message


@app.callback(
    Output("logo", "src"),
    Input("logo", "n_clicks"),
    prevent_initial_call=True
)
def change_logo(_):
    return "assets/logo2025.png" if _ % 2 == 0 else "assets/logo2025_glow.png"

@app.callback(
    Output("direction", "children", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("keyboard_move", "n_keydowns"),
    State("keyboard_move", "keydown"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def keydown(_, keydown, on):
    if not keydown or not on: 
        raise PreventUpdate
    key = keydown["key"].lower()
    path = f"/direction?direction={key}"
    return DIR_DICT[key], send_request(path, SEND, PRINT)


@app.callback(
    Output("direction", "children", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("keyboard_move", "n_keyups"),
    State("keyboard_move", "keyup"),
    State("keyboard_move", "keys_pressed"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def keyup(_, keyup, keys_pressed, on):
    if not keyup or not on: 
        raise PreventUpdate
    key = list(keys_pressed.keys())[0].lower() if keys_pressed else "None"
    path = f"/direction?direction={key}"
    return DIR_DICT[key], send_request(path, SEND, PRINT)

@app.callback(
    Output("speed", "value", allow_duplicate=True),
    Output("indicator", "children", allow_duplicate=True),
    Input("keyboard_speed", "n_keydowns"),
    State("keyboard_speed", "keydown"),
    State("power_btn", "on"),
)
def change_speed(_, keydown, on):
    if not keydown or not on: 
        raise PreventUpdate
    key = keydown["key"]
    path = f"/speed?speed={key}"
    return int(key), send_request(path, SEND, PRINT)

app.clientside_callback(
    """
    function update_servo(key_pressed) {
        const key = key_pressed.key.toLowerCase();
        let servo;
            if (key === "g") {
                document.getElementById("servo1").querySelector(".rc-slider-handle").focus();
            } else if (key === "h") {
                document.getElementById("servo2").querySelector(".rc-slider-handle").focus();
            } else {
                return window.dash_clientside.no_update;
            }
        return window.dash_clientside.no_update;
    }
    """, 
    Output("logo", "style", allow_duplicate=True), # Dummy output
    Input("keyboard_servo", "keydown"),
    prevent_initial_call=True
)

app.clientside_callback(
    """
    function update_slice_btns(_, key_pressed) {
        const key = key_pressed.key.toLowerCase();
        console.log(key);
        let servo;
            if (key === "k") {
                document.getElementById("slice_up").click();
            } else if (key === "l") {
                document.getElementById("slice_down").click();
            } else {
                return window.dash_clientside.no_update;
            }
        return window.dash_clientside.no_update;
    }
    """, 
    Output("logo", "style", allow_duplicate=True), # Dummy output
    Input("keyboard_slice", "n_keydowns"),
    State("keyboard_slice", "keydown"),
    prevent_initial_call=True
)

@app.callback(
    Output("indicator", "children", allow_duplicate=True),
    Input("servo1", "value"),
    Input("servo2", "value"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def change_state_params(servo1, servo2, on):
    if not on:
        raise PreventUpdate
    path = f"/state?servo1={servo1}&servo2={servo2}"
    return send_request(path, SEND, PRINT)

@app.callback(
    Output("indicator", "children", allow_duplicate=True),
    Input("correction", "value"),
    State("power_btn", "on"),
    prevent_initial_call=True,
)
def change_correction(correction, on):
    if not on:
        raise PreventUpdate
    path = f"/correction?correction={correction}"
    return send_request(path, SEND, PRINT)


@app.callback(
    Output("indicator", "children", allow_duplicate=True),
    Input("slice_up", "n_clicks"),
    Input("slice_down", "n_clicks"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def slice_up_down(_, __, on):
    if not on:
        raise PreventUpdate
    if ctx.triggered_id == "slice_up":
        path = "/slice?up=1&down=0"
    elif ctx.triggered_id == "slice_down":
        path = "/slice?up=0&down=1"
    else:
        raise PreventUpdate
    return send_request(path, SEND, PRINT)

@app.callback(
    Output("indicator", "children", allow_duplicate=True),
    Input("voyage", "n_clicks"),
    State("power_btn", "on"),
    prevent_initial_call=True
)
def time_travel(_, on):
    if on:
        raise PreventUpdate
    path = "/dance"
    return send_request(path, SEND, PRINT)

if __name__ == '__main__':
    SEND = True
    PRINT = True

    app.run(debug=True, host="0.0.0.0")


