import numpy as np
import pandas as pd 
import dash
import plotly.graph_objects as go
from dash import html, dcc
from dash.dependencies import Input, Output

# Only define this ONCE
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-LtrjvnR4GearyFz0csX2kC2ubBfEO1D3zGmO1QL75wzSULKVRWl0z5Cy68LHR9wY',
        'crossorigin': 'anonymous'
    }
]


patients = pd.read_csv('IndividualDetails.csv')

total = patients.shape[0]
active=patients[patients['current_status'] =='Hospitalized'].shape[0]
recovered = patients[patients['current_status']=='Recovered'].shape[0]
deaths = patients[patients['current_status']=='Deceased'].shape[0]

options = [
    {'label':'All', 'value' :'All'},
    {'label' :'Hospitalized', 'value' :'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'}
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)




# Layout
app.layout = html.Div([
    html.H1("Coronavirus Pandemic", style={'color': '#fff', 'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Div([
                html.H3("Total Cases", className='text-light text-center'),
                html.H4(total, className='text-light text-center')
            ], className='card-body')
        ], className='card bg-danger shadow col-md-3'),

        html.Div([
            html.Div([
                html.H3("Recovered", className='text-light text-center'),
                html.H4(recovered, className='text-light text-center')
            ], className='card-body')
        ], className='card bg-success shadow col-md-3'),

        html.Div([
            html.Div([
                html.H3("Deaths", className='text-light text-center'),
                html.H4(deaths, className='text-light text-center')
            ], className='card-body')
        ], className='card bg-dark shadow col-md-3'),

        html.Div([
            html.Div([
                html.H3("Active", className='text-light text-center'),
                html.H4(active, className='text-light text-center')
            ], className='card-body')
        ], className='card bg-warning shadow col-md-3'),

    ], className='row mb-4'),

    html.Div([], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options= options,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ], className='col-md-12')
    ], className='row')

], className='container')

@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(type):

    if type =='All':
       pbar = patients['detected_state'].value_counts().reset_index()
       return {'data' :[go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout' :go.Layout(title='State Total Count')}

    
    else:
        npat = patients[patients['current_status']==type]
        pbar = npat['detected_state'].value_counts().reset_index()
        return {'data' :[go.Bar(x=pbar['detected_state'], y=pbar['count'])],
            'layout' :go.Layout(title='State Total Count')}

# Run server
if __name__ == '__main__':
    app.run(debug=True)




