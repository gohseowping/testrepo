import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],  # Set the initial value to the minimum and maximum payload values
        marks={
            0: {'label': '0 kg'},
            2500: {'label': '2500 kg'},
            5000: {'label': '5000 kg'},
            7500: {'label': '7500 kg'},
            10000: {'label': '10000 kg'}
        }
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Callbacks
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie(value):
    filtered_df = spacex_df
    if value == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == value].groupby(['Launch Site', 'class']).size().reset_index(
            name='class count')
        title = f"Total Success Launches for site {value}"
        fig = px.pie(filtered_df, values='class count', names='class', title=title)
        return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload):
    low, high = selected_payload
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df1 = spacex_df[mask]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df1,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation of Payload and Successful Missions for All Sites'
        )
        return fig
    else:
        filtered_df2 = filtered_df1[filtered_df1['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df2,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation of Payload and Successful Missions for site {selected_site}'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
