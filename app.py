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

    html.Label("Selecciona una variable para el histograma:"),
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[0]
    ),

    dcc.Graph(id='histogram'),

    html.H2("Estadísticas Descriptivas"),
    html.Div(id='summary-stats'),

    html.H2("Selecciona variables para el scatter plot:"),
    html.Div([
        dcc.Dropdown(
            id='x-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype != 'object'],
            value=df.select_dtypes(include=['number']).columns[0],
            style={'width': '50%'}
        ),
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if df[col].dtype != 'object'],
            value=df.select_dtypes(include=['number']).columns[1],
            style={'width': '50%'}
        ),
    ], style={'display': 'flex', 'gap': '10px'}),

    dcc.Graph(id='scatter-plot'),
    
    html.Label("Selecciona una variable para el gráfico de barras:"),
    dcc.Dropdown(
        id='bar-chart-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns[0]
    ),
    dcc.Graph(id='bar-chart')
])

@app.callback(
    Output('histogram', 'figure'),
    Output('summary-stats', 'children'),
    [Input('variable-dropdown', 'value')]
)
def update_histogram(selected_variable):
    fig = px.histogram(df, x=selected_variable, title=f"Histograma de {selected_variable}")

    stats = df[selected_variable].describe().to_frame().reset_index()
    stats.columns = ["Estadística", "Valor"]
    stats_table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in stats.columns])),
        html.Tbody([
            html.Tr([
                html.Td(stats.iloc[i][col]) for col in stats.columns
            ]) for i in range(len(stats))
        ])
    ])
    
    

    return fig, stats_table

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_scatter_plot(x_variable, y_variable):
    fig = px.scatter(df, x=x_variable, y=y_variable, title=f"Scatter Plot de {x_variable} vs {y_variable}")
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('bar-chart-dropdown', 'value')]
)
def update_bar_chart(selected_variable):
    # Calcular el conteo de cada valor único en la variable seleccionada
    count_df = df[selected_variable].value_counts().reset_index()
    count_df.columns = [selected_variable, 'Frecuencia']  # Renombrar columnas

    # Crear gráfico de barras
    fig = px.bar(count_df, x=selected_variable, y='Frecuencia',
                 labels={selected_variable: "Categoría", "Frecuencia": "Frecuencia"},
                 title=f"Gráfico de Barras de {selected_variable}")
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
