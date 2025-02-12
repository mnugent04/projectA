from dash import Dash, dcc, html, Input, Output, callback_context
import plotly.express as px
import pandas as pd

df = pd.read_csv("CO_scv_2023.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month

# seasons
season_map = {
    "Winter": [12, 1, 2],
    "Spring": [3, 4, 5],
    "Summer": [6, 7, 8],
    "Fall": [9, 10, 11],
}

# map months to seasons
df["Season"] = df["Month"].map({m: s for s, ms in season_map.items() for m in ms})

app = Dash(__name__)

app.layout = html.Div([
    html.P('Click below to change the season!'),

    # buttons for seasons or all seasons
    html.Div([
        html.Button("All Seasons", id="all-seasons-btn", n_clicks=0),
        html.Button("Winter", id="winter-btn", n_clicks=0),
        html.Button("Spring", id="spring-btn", n_clicks=0),
        html.Button("Summer", id="summer-btn", n_clicks=0),
        html.Button("Fall", id="fall-btn", n_clicks=0),
    ], style={'margin-bottom': '10px'}),

    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("all-seasons-btn", "n_clicks"),
    Input("winter-btn", "n_clicks"),
    Input("spring-btn", "n_clicks"),
    Input("summer-btn", "n_clicks"),
    Input("fall-btn", "n_clicks")
)
def update_graph(all_seasons, winter, spring, summer, fall):
    call_context = callback_context

    if call_context.triggered:
        button_id = call_context.triggered[0]["prop_id"].split(".")[0]
        selected_season = button_id.replace("-btn", "").capitalize()

    if call_context.triggered[0]["prop_id"].split(".")[0] == "all-seasons-btn" or not call_context.triggered:
        season_totals = df.groupby("Season")["Daily Max 8-hour CO Concentration"].sum().reset_index()
        fig = px.bar(season_totals, x="Season", y="Daily Max 8-hour CO Concentration",
                     title=f"Santa Clarita CO Concentrations by Season (2023)",
                     labels={"Daily Max 8-hour CO Concentration": "Total CO (ppm)"},
                     text_auto=True)
    else:
        filtered_df = df[df["Season"] == selected_season]

        seasonal_totals = filtered_df.groupby("Month")["Daily Max 8-hour CO Concentration"].sum().reset_index()

        # bar chart
        fig = px.bar(seasonal_totals, x="Month", y="Daily Max 8-hour CO Concentration",
                     title=f"Santa Clarita CO Concentrations during {selected_season} (2023)",
                     labels={"Month": "Month", "Daily Max 8-hour CO Concentration": "CO (ppm)"},
                     text_auto=True)

    # make it look better more SwD
    fig.update_layout(
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        title=dict(
            x=0.5,
            font=dict(size=24)
        ),
        plot_bgcolor="white",
        bargap=0.2
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

