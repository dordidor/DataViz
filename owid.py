import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

# Dataset Processing

df = pd.read_csv('owid_output.csv')

# Requirements for the dash core components

"""
country_options = [
    {'label': 'Country Portugal', 'value': 'Portugal'},
    {'label': 'Country Spain', 'value': 'Spain'},
    {'label': 'Country France', 'value': 'France'}
]

Equivalent way to iteratively build country_options from the dataset's countries:
"""
country_options = [
    dict(label='Country ' + country, value=country)
    for country in df['location'].unique()]
 

data_options = [
    {'label': 'Total Cases', 'value': 'total_cases'},
    {'label': 'Log Cases', 'value': 'log_cases'},
    {'label': 'New Cases', 'value': 'new_cases'}
]

# The app itself

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Countries COVID Cases'),

    dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['Portugal'],
        multi=True
    ),

    html.Br(),

    dcc.RadioItems(
        id='data_radio',
        options=data_options,
        value='total_cases'
    ),

    dcc.Graph(id='graph_example'),

    html.Br(),

    dcc.RangeSlider(
        id='days_slider',
        min=0,
        max=120,
        value=[0, 120],
        marks={'0': 'Day 0',
               '30': 'Day 30',
               '60': 'Day 60',
               '90': 'Day 90',
               '120': 'Day 120'},
        step=1
    )
])


@app.callback(
    Output('graph_example', 'figure'),
    [Input('country_drop', 'value'),
     Input('data_radio', 'value'),
     Input('days_slider', 'value')]
)


def update_graph(countries, cases, days):
    filtered_by_days_df = df[(df['days_since'] >= 0) & (df['days_since'] <= 365)]

    scatter_data = []

    for country in countries:
        filtered_by_days_and_country_df = filtered_by_days_df.loc[filtered_by_days_df['location'] == country]

        temp_data = dict(
            type='scatter',
            y=filtered_by_days_and_country_df[cases],
            x=filtered_by_days_and_country_df['days_since'],
            name=country
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Days'),
                          yaxis=dict(title='cases')
                          )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
