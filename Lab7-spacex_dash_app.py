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
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': site, 'value': site} for site in ['All'] + list(spacex_df['Launch Site'].unique())],
        value='All',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TASK 2: Callback function to render success-pie-chart based on selected site dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'All':
        # Total successful launches for all sites
        success_counts = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts()
        fig = px.pie(names=success_counts.index, values=success_counts.values, title='Success Launches by Site')
    else:
        # Successful and failed launches for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_counts = site_data['class'].value_counts()
        fig = px.pie(names=['Success', 'Failed'], values=success_counts.values, title=f'Success Launches at {selected_site}')
    return fig


# TASK 4: Callback function to render success-payload-scatter-chart based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'All':
        # Filter data for selected payload range
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        # Plot scatter chart
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload vs. Outcome for All Sites')
    else:
        # Filter data for selected site and payload range
        filtered_data = spacex_df[(spacex_df['Launch Site'] == selected_site) & 
                                  (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                  (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        # Plot scatter chart
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Payload vs. Outcome at {selected_site}')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
