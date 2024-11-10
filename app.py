import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Cargar los datos
df = pd.read_csv('data/join/join.csv')

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Análisis Exploratorio de Datos (EDA)"),

    html.Label("Selecciona una variable para el gráfico de líneas:"),
    dcc.Dropdown(
        id='line-chart-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype != 'object'],
        value=df.select_dtypes(include=['number']).columns[0]
    ),

    dcc.Graph(id='line-chart'),

    html.Label("Selecciona variables para el scatter plot:"),
    html.Div([
        dcc.Dropdown(
            id='x-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype != 'object'],
            value=df.select_dtypes(include=['number']).columns[0],
            style={'width': '200px'}
        ),
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype != 'object'],
            value=df.select_dtypes(include=['number']).columns[1],
            style={'width': '200px'}
        ),
    ], style={'display': 'flex', 'gap': '100px', 'width': '100px'}),

    dcc.Graph(id='scatter-plot')
])

@app.callback(
    Output('line-chart', 'figure'),
    [Input('line-chart-dropdown', 'value')]
)
def update_line_chart(selected_variable):
    fig = px.line(df, x=df.index, y=selected_variable, title=f"Gráfico de Líneas de {selected_variable}")
    return fig

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_scatter_plot(x_variable, y_variable):
    fig = px.scatter(df, x=x_variable, y=y_variable, title=f"Scatter Plot de {x_variable} vs {y_variable}")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
