import os, sys
sys.path.append(os.getcwd())

from dash_extensions.enrich import DashProxy, Input, Output, State, clientside_callback
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
        requests.get(URL + path, timeout=0.5)
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
    prevent_initial_call=True
)
def change_speed(_, keydown, on):
    if not keydown or not on: 
        raise PreventUpdate
    key = keydown["key"]
    path = f"/speed?speed={key}"
    return int(key), send_request(path, SEND, PRINT)


@app.callback(
    Output("switch", "on"),
    Input("keyboard_switch", "n_keydowns"),
    State("switch", "on"),
    prevent_initial_call=True
)
def toggle_switch(_, on):
    return not on

app.clientside_callback(
    """
    function update_servo(key_pressed) {
        const key = key_pressed.key.toLowerCase();
        let servo;
            if (key === "j") {
                document.getElementById("servo1").querySelector(".rc-slider-handle").focus();
            } else if (key === "k") {
                document.getElementById("servo2").querySelector(".rc-slider-handle").focus();
            } else if (key === "l") {
                document.getElementById("servo3").querySelector(".rc-slider-handle").focus();
            } else {
                return window.dash_clientside.no_update;
            }
        return window.dash_clientside.no_update;
    }
    """, 
    Output("logo", "style"), # Dummy output
    Input("keyboard_servo", "keydown"),
    prevent_initial_call=True
)

@app.callback(
    Output("indicator", "children", allow_duplicate=True),
    Input("servo1", "value"),
    Input("servo2", "value"),
    Input("servo3", "value"),
    Input("correction", "value"),
    Input("switch", "on"),
    prevent_initial_call=True
)
def change_state_params(servo1, servo2, servo3, correction, switch):
    path = f"/state?servo1={servo1}&servo2={servo2}&servo3={servo3}&correction={correction}&attach={1 if switch else 0}"
    return send_request(path, SEND, PRINT)





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
    SEND = True
    PRINT = True

    app.run(debug=True, host="0.0.0.0")


