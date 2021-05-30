import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd
import numpy as np
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

import psycopg2

#Base de datos
conexion1 = psycopg2.connect(database="blockbuster", user="postgres", password="secret", port="5433")
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
print('Salida:')
print(years)
conexion1.close()

#-------------------------------------------------------------------------------------------------------------------

#Dispose los rango de edad
edadmayor = (data['edad'] >= 55) & (data['edad'] <= 95)
edadmedia = (data['edad'] >= 24) & (data['edad'] < 55)
edadmenor = (data['edad'] >= 1) & (data['edad'] < 24)

data.loc[edadmayor,'RangoEdad'] = 'edadmayor'
data.loc[edadmedia,'RangoEdad'] = 'edadmedia'
data.loc[edadmenor,'RangoEdad'] = 'edadmenor'

#Creacion nuevo dataframe con departamentos
alldepartamentos=np.array(data['departamento'].unique())
numeros=np.arange(start=1, stop=28, step=1)

index=0
arraydptos = np.zeros(27)
for i in alldepartamentos:
    temp=data[data['departamento']==i]
    arraydptos[index] =temp.shape[0];
    index=index+1;

arraydptos2=np.array(arraydptos)

columns = ['Departamentos'] 

dfdptos = pd.DataFrame(data=alldepartamentos ,index=numeros, columns=columns) 

dfdptos["Total casos"]=arraydptos2

fig2 = px.pie(dfdptos, values="Total casos", names="Departamentos") 

#Grafica de Recuperado/Fallecido
columns = ['Casos'] 
data3=data[data['recuperado']=="Recuperado"]

dfrecu = pd.DataFrame(data=data3.shape,columns=columns) 
dfrecu["Estado"]=['Recuperado','Fallecido']

fig3 = px.pie(dfrecu, values="Casos", names="Estado") 

#Rango de Edad
columns = ['Casos'] 
x1=data[data['RangoEdad']=="edadmayor"].shape[0]
x2=data[data['RangoEdad']=="edadmedia"].shape[0]
x3=data[data['RangoEdad']=="edadmenor"].shape[0]


datar = {'Casos':  [x1, x2, x3]}


dran = pd.DataFrame(data=datar,columns=columns) 
dran["Rango Edad"]=['Personas Mayores[>55]', 'Personas Adultas[>25]',' Personas Jovenes [25<]']


fig4 = px.pie(dran, values="Casos", names="Rango Edad") 

#Histograma
data.drop(data.index[data['sexo'] == "m"], inplace = True)
fig5 = px.histogram(data, x="sexo") 


#Fuente de Contagio
columns = ['Casos'] 
x1=data[data['contagio']=="Importado"].shape[0]
x2=data[data['contagio']=="Relacionado"].shape[0]
x3=data[data['contagio']=="En estudio"].shape[0]


datar = {'Casos':  [x1, x2, x3]}


dcontagio = pd.DataFrame(data=datar,columns=columns) 
dcontagio["Fuente Contagio"]=['Importado', 'Relacionado','En estudio']


fig6 = px.pie(dcontagio, values="Casos", names="Fuente Contagio") 


data = data[['departamento','municipio','edad','sexo','contagio','recuperado','inicio_sintomas','recuperacion']].copy();

fig = px.bar(data, x="departamento", y="edad", color="recuperado", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Casos Covid-19 Colombia'),

    html.Div(children='''
        uwu.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    html.H1(children='Casos por Departamentos'),
    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),
    html.H1(children='Porcentaje de recuperados/fallecidos'),
     dcc.Graph(
        id='example-graph3',
        figure=fig3
    ),
    html.H1(children='Porcentaje infectados por rango de edad'),
    dcc.Graph(
        id='example-graph4',
        figure=fig4
    ),
    html.H1(children='Casos por sexo'),
    dcc.Graph(
        id='example-graph5',
        figure=fig5
    ),
    html.H1(children='Porcentaje de fuente de contagio'),
    dcc.Graph(
        id='example-graph6',
        figure=fig6
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8000,debug=True)