# Import required libraries
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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(
                                                            id='site-dropdown',
                                                            options=[
                                                                {'label': 'All Sites', 'value': 'ALL'},
                                                                {'label': 'CCAFSLC-40', 'value': 'CCAFS LC-40'},
                                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                            ],
                                                            value='ALL',
                                                            placeholder="Select a Launch Site here",
                                                            searchable=True
                                                        ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                               
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
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

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
@app.callback(
                                    Output(component_id='success-pie-chart', component_property='figure'),
                                    Input(component_id='site-dropdown', component_property='value')
                                )
def get_pie_chart(entered_site):
                                    filtered_df = spacex_df
                                
                                    if entered_site == 'ALL':
                                        # Filter data for successful launches
                                        success_df = filtered_df[filtered_df['class'] == 1]
                                
                                        # Create the pie chart
                                        fig = px.pie(
                                            success_df,
                                            values='class',
                                            names='Launch Site',
                                            title='Success Counts for All Launch Sites'
                                        )
                                
                                        return fig
                                
                                    else:
                                        # Filter data for successful launches for the selected site
                                        success_df = filtered_df[filtered_df['LaunchSite'] == entered_site]
                                        
                                
                                        # Create the pie chart
                                        fig = px.pie(
                                            success_df,
                                            values='class',
                                            names='Launch Site',
                                            title=f"Success Counts for Launch Site: {entered_site}"
                                        )
                                
                                    return fig

@app.callback(
                                    Output(component_id='success-payload-scatter-chart', component_property='figure'),
                                    [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')]
                                )
def update_scatter_chart(selected_site, selected_payload):            
                                        low, high =selected_payload
                                        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
                                        filtered_df1 = spacex_df[mask]
                                        if  selected_site =='ALL':
                                            fig = px.scatter(filtered_df1, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                            title='Correlation of Payload and Successful Missions for All Sites')
                                            return fig
                                        else:
                                            filtered_df2= filtered_df1[filtered_df1['Launch Site'] ==  selected_site]
                                            fig = px.scatter(filtered_df2, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                                            title=f'Correlation of Payload and Successful Missions for site {selected_site}')
                                            return fig



# Run the app
if __name__ == '__main__':
    app.run_server()