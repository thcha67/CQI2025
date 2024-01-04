from dash import Dash, html, Input, Output, State, ctx, dcc, clientside_callback
import dash_bootstrap_components as dbc
import requests
import dash_daq as daq


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

drag_mode = "mouseup"

url = "http://192.168.59.75"


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("COSMIC")
        ], width=2, align="center", style={"marginBottom" : "30px"}),
    ], justify="center", align="center"),
    dbc.Row([
        dbc.Col([
            html.H4("Speed"),
            dcc.Slider(
                id="speed",
                min=-100,
                max=100,
                value=0,
                step=1,
                className="vertical-slider",
                updatemode=drag_mode,
                marks=None,
                tooltip={"always_visible": True, "placement": "left"},
                vertical=True,
                verticalHeight=500,
            ),
        ], width=2),
        dbc.Col([
            dbc.Button("Turn right", id="right", color="primary", className="button", n_clicks=0, size="lg"),
            dbc.Button("Turn left", id="left", color="primary", className="button", n_clicks=0, size="lg"),
            dbc.Button("STOP", id="stop", color="danger", className="stop-button")
        ], width=2, align="center"),
        dbc.Col([
            html.H4("Pince"),
            dcc.Slider(
                id="pince",
                min=0,
                max=180,
                value=0,
                step=3,
                className="slider",
                updatemode=drag_mode,
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
            html.H4("Flip"),
            dcc.Slider(
                id="flip",
                min=0,
                max=180,
                value=0,
                step=5,
                className="slider",
                updatemode=drag_mode,
                marks=None,
                tooltip={"always_visible": True, "placement": "bottom"}
            ),
            html.H4("Up/Down"),
            dcc.Slider(
                id="up_down",
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
    html.Div(id='output', style={"display": "none"})
], fluid=True, style={"marginTop" : "50px"})

@app.callback(
    Output("speed", "value"),
    Input("stop", "n_clicks"),
    prevent_initial_call=True
)
def stop(stop):
    return 0

@app.callback(
    Output('output', 'children', allow_duplicate=True),
    Input("pince", "value"),
    Input("flip", "value"),
    Input("up_down", "value"),
    Input("speed", "value"),
    Input("right", "n_clicks"),
    Input("left", "n_clicks"),
    Input("correction", "value"), 
    prevent_initial_call=True
)
def test(pince, flip, up_down, speed, right, left, correction):
    direction = ctx.triggered[0]["prop_id"].split(".")[0]
    if direction == "right":
        right = 1
        left = 0
    elif direction == "left":
        right = 0
        left = 1
    else:
        right = left = 0
    query_string = "/patate?pince={0}&flip={1}&up_down={2}&speed={3}&right={4}&left={5}&correction={6}"
    request = url + query_string.format(pince, flip, up_down, speed, right, left, correction)
    req = requests.get(request)
    print(req)

if __name__ == '__main__':
    app.run_server(debug=False)