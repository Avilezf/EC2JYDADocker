import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# app requires "pip install psycopg2" as well

server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# for your home PostgreSQL test table
# app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:your_password@localhost/test"

database= os.environ.get('postgres')
# for your live Heroku PostgreSQL database
app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:secret@postgres:5432/blockbuster"

db = SQLAlchemy(app.server)


class Actor(db.Model):
    __tablename__ = 'actor'

    Actor_id = db.Column(db.Integer, nullable=False, primary_key=True)
    First_name = db.Column(db.String(40), nullable=False)
    Last_name = db.Column(db.String(40), nullable=False)
    Last_updated = db.Column(db.Date(), nullable=False)

    def __init__(self, Actor_id, First_name, Last_name, Last_updated):
        self.Actor_id = Actor_id
        self.First_name = First_name
        self.Last_name = Last_name
        self.Last_updated = Last_updated


# ------------------------------------------------------------------------------------------------

app.layout = html.Div([
    html.Div([
        dcc.Input(
            id='adding-rows-name',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-columns-button', n_clicks=0)
    ], style={'height': 50}),

    dcc.Interval(id='interval_pg', interval=86400000*7, n_intervals=0),  # activated once/week or when page refreshed
    html.Div(id='postgres_datatable'),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),
    html.Button('Save to PostgreSQL', id='save_to_postgres', n_clicks=0),

   # Create notification when saving to excel
    html.Div(id='placeholder', children=[]),
    dcc.Store(id="store", data=0),
    dcc.Interval(id='interval', interval=1000),

    dcc.Graph(id='my_graph'),
    dcc.Graph(id='my_graph2'),
    dcc.Graph(id='my_graph3'),
    
   

])


# ------------------------------------------------------------------------------------------------


@app.callback(Output('postgres_datatable', 'children'),
              [Input('interval_pg', 'n_intervals')])
def populate_datatable(n_intervals):
    df = pd.read_sql_table('actor', con=db.engine)
    return [
        dash_table.DataTable(
            id='our-table',
            columns=[{
                         'name': str(x),
                         'id': str(x),
                         'deletable': False,
                     } 
                     for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'}
            

        ),
    ]


@app.callback(
    Output('our-table', 'columns'),
    [Input('adding-columns-button', 'n_clicks')],
    [State('adding-rows-name', 'value'),
     State('our-table', 'columns')],
    prevent_initial_call=True)
def add_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'name': value, 'id': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns


@app.callback(
    Output('our-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('our-table', 'data'),
     State('our-table', 'columns')],
    prevent_initial_call=True)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


@app.callback(
    Output('my_graph', 'figure'),
    [Input('our-table', 'data')],
    prevent_initial_call=True)
def display_graph(data):
    conexion1 = psycopg2.connect(database="blockbuster", host='postgres', user="postgres", password="secret", port="5432")
    cursor1=conexion1.cursor()
    cursor1.execute("select count(*) from rental  where extract(year from rental_date) = '2006'")
    year2 = 0
    for fila in cursor1:
        year2 = fila
    year2 = year2[0]
        
    cursor1.execute("select count(*) from rental  where extract(year from rental_date) = '2005'")
    year1 = 0
    for fila in cursor1:
        year1 = fila
    year1 = year1[0]

    years = list([{'2005':int(year1)}, {'2006':int(year2)}])
    conexion1.close()   

     #------------------------------------------------------------------------------------------------

    objects = list(x for sublist in years for x in sublist.keys())
    y_pos = range(len(objects))
    vals = [x for sublist in years for x in sublist.values()]
    fig = go.Figure([go.Bar(x=objects, y=vals)])

    return fig

 #-------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.callback(
    Output('my_graph2', 'figure'),
    [Input('our-table', 'data')],
    prevent_initial_call=True)
def display_graph(data):
    months = []
    month = 0
    conexion1 = psycopg2.connect(database="blockbuster", host='postgres', user="postgres", password="secret", port="5432")

    cursor1=conexion1.cursor()
    cursor1.execute("select count(*) from rental  where extract(year from rental_date) = '2005' and extract(month from rental_date) = '05'")
    for fila in cursor1:
        month = fila
    month = month[0]
    months.append(month)
        
    cursor1.execute("select count(*) from rental  where extract(year from rental_date) = '2005' and extract(month from rental_date) = '06'")
    for fila in cursor1:
        month = fila
    month = month[0]
    months.append(month)

    cursor1.execute("select count(*) from rental  where extract(year from rental_date) = '2005' and extract(month from rental_date) = '07'")
    for fila in cursor1:
        month = fila
    month = month[0]
    months.append(month)

    cursor1.execute("select count(*) from rental  where extract(year from rental_date) = '2005' and extract(month from rental_date) = '08'")
    for fila in cursor1:
        month = fila
    month = month[0]
    months.append(month)

    months = list([{'Mayo':int(months[0])}, {'Junio':int(months[1])}, {'Julio':int(months[2])}, {'Agosto':int(months[3])}])
    conexion1.close()  

    #------------------------------------------------------------------------------------------------

    objects = list(x for sublist in months for x in sublist.keys())
    y_pos = range(len(objects))
    vals = [x for sublist in months for x in sublist.values()]
    fig = go.Figure([go.Bar(x=objects, y=vals)])

    return fig

@app.callback(
    Output('my_graph3', 'figure'),
    [Input('our-table', 'data')],
    prevent_initial_call=True)
def display_graph(data):
    customers = []
    customer = 0
    conexion1 = psycopg2.connect(database="blockbuster", host='postgres', user="postgres", password="secret", port="5432")

    cursor1=conexion1.cursor()
    cursor1.execute("select count(*) from customer where active = '0'")
    for fila in cursor1:
        customer = fila
    customer = customer[0]
    customers.append(customer)
        
    cursor1.execute("select count(*) from customer where active = '1'")
    for fila in cursor1:
        customer = fila
    customer = customer[0]
    customers.append(customer)


    customers = list([{'No Activo':int(customers[0])}, {'Activo':int(customers[1])}])
    conexion1.close()

    #------------------------------------------------------------------------------------------------

    objects = list(x for sublist in customers for x in sublist.keys())
    y_pos = range(len(objects))
    vals = [x for sublist in customers for x in sublist.values()]

    fig = go.Figure([go.Pie(labels=objects, values=vals)])

    return fig



@app.callback(
    [Output('placeholder', 'children'),
     Output("store", "data")],
    [Input('save_to_postgres', 'n_clicks'),
     Input("interval", "n_intervals")],
    [State('our-table', 'data'),
     State('store', 'data')],
    prevent_initial_call=True)
def df_to_csv(n_clicks, n_intervals, dataset, s):
    output = html.Plaintext("The data has been saved to your PostgreSQL database.",
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("", style={'margin': "0px"})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if input_triggered == "save_to_postgres":
        s = 6
        pg = pd.DataFrame(dataset)
        pg.to_sql("actor", con=db.engine, if_exists='replace', index=False)
        return output, s
    elif input_triggered == 'interval' and s > 0:
        s = s - 1
        if s > 0:
            return output, s
        else:
            return no_output, s
    elif s == 0:
        return no_output, s


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')