import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Carregar o dataset
df = pd.read_csv("C:/Users/João/Desktop/COISAS DO JOÃO/LoL_2021/League of Legends 2021 World Championship Play-In Groups Statistics - Raw Data.csv")

# Iniciar a aplicação Dash
app = dash.Dash(__name__)

# Função para gerar gráficos de distribuição aprimorados
def generate_histogram(df, column, title, color='royalblue', nbins=15):
    fig = px.histogram(df, x=column, nbins=nbins, title=title)
    fig.update_traces(marker_color=color, opacity=0.7, 
                      marker_line=dict(width=1, color='darkblue'))
    
    mean_value = df[column].mean()
    median_value = df[column].median()
    
    fig.add_annotation(
        x=mean_value, y=5, 
        text=f'Média: {mean_value:.2f}', 
        showarrow=True, arrowhead=2, 
        ax=0, ay=-40, 
        font=dict(size=12, color='green'), 
        bgcolor='white', opacity=0.7
    )
    
    fig.add_annotation(
        x=median_value, y=5, 
        text=f'Mediana: {median_value:.2f}', 
        showarrow=True, arrowhead=2, 
        ax=0, ay=-40, 
        font=dict(size=12, color='red'), 
        bgcolor='white', opacity=0.7
    )
    
    fig.update_layout(
        xaxis_title=column, 
        yaxis_title="Frequência",
        plot_bgcolor='rgba(255, 255, 255, 0.9)', 
        paper_bgcolor='rgba(255, 255, 255, 0.9)', 
        font=dict(family='Lato, sans-serif', color='#2c3e50'), 
        title_x=0.5, 
        title_font=dict(size=24, family='Roboto, sans-serif', color='#34495e'),
        xaxis=dict(showgrid=False),  
        yaxis=dict(showgrid=True, gridcolor='lightgrey'),  
        bargap=0.2
    )
    
    return fig

# Função para gráficos de dispersão com linha de tendência
def generate_scatter(df, x_col, y_col, color_col, title, marker_size=10):
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=title)
    fig.update_traces(marker=dict(size=marker_size, opacity=0.7))
    
    # Regressão linear para a linha de tendência
    x = df[x_col]
    y = df[y_col]
    # Calcular os coeficientes da regressão linear (y = mx + b)
    m, b = np.polyfit(x, y, 1)
    # Gerar os valores da linha de tendência
    trendline_y = m * x + b
    
    # Adicionar a linha de tendência ao gráfico
    fig.add_trace(go.Scatter(
        x=x, 
        y=trendline_y, 
        mode='lines', 
        name='Linha de Tendência', 
        line=dict(color='red', width=3, dash='dash')
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(255, 255, 255, 0.9)',
        font=dict(family='Lato, sans-serif', color='#2c3e50'),
        title_x=0.5
    )
    return fig

# Função para gráficos de boxplot
def generate_boxplot(df, x_col, y_col, title, color='indianred'):
    fig = px.box(df, x=x_col, y=y_col, title=title)
    fig.update_traces(marker=dict(color=color, size=7))
    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(255, 255, 255, 0.9)',
        font=dict(family='Lato, sans-serif', color='#2c3e50'),
        title_x=0.5
    )
    return fig

# Gráficos
fig_kda = generate_histogram(df, "Kills", "Distribuição de Kills")
fig_kda_relacao = generate_scatter(
    df, 
    "Kills", 
    "Deaths", 
    "Result", 
    "Relação entre Kills e Deaths por Resultado"
)
fig_gold = generate_boxplot(df, "Team", "Gold Earned", "Distribuição de Gold Earned por Time", color='indianred')
fig_champion_damage = generate_boxplot(df, "Position", "Champion Damage Share", "Champion Damage Share por Position", color='seagreen')

# Layout da aplicação Dash
app.layout = html.Div(
    children=[
        # Título Principal
        html.H1(
            "Dashboard de Análise Estatística do Mundial de League of Legends de 2021", 
            style={
                'textAlign': 'center', 
                'marginBottom': '50px', 
                'fontFamily': 'Roboto, sans-serif', 
                'fontWeight': '700', 
                'color': '#2c3e50', 
                'fontSize': '40px',
                'letterSpacing': '1px'
            }
        ),
        
        # Seção para os gráficos
        html.Div(
            children=[
                html.Div(
                    children=[ 
                        html.H3("Distribuição de Kills", style={'textAlign': 'center', 'fontFamily': 'Lato, sans-serif', 'color': '#34495e', 'fontSize': '24px'}),
                        dcc.Graph(figure=fig_kda),
                    ],
                    style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}
                ),
                html.Div(
                    children=[
                        html.H3("Relação entre Kills e Deaths por Resultado", style={'textAlign': 'center', 'fontFamily': 'Lato, sans-serif', 'color': '#34495e', 'fontSize': '24px'}),
                        dcc.Graph(figure=fig_kda_relacao),
                    ],
                    style={'width': '48%', 'display': 'inline-block'}
                ),
            ],
            style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'marginBottom': '50px'}
        ),
        
        # Seção para outros gráficos
        html.Div(
            children=[
                html.Div(
                    children=[ 
                        html.H3("Distribuição de Gold Earned por Time", style={'textAlign': 'center', 'fontFamily': 'Lato, sans-serif', 'color': '#34495e', 'fontSize': '24px'}),
                        dcc.Graph(figure=fig_gold),
                    ],
                    style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%'}
                ),
                html.Div(
                    children=[
                        html.H3("Champion Damage Share por Position", style={'textAlign': 'center', 'fontFamily': 'Lato, sans-serif', 'color': '#34495e', 'fontSize': '24px'}),
                        dcc.Graph(figure=fig_champion_damage),
                    ],
                    style={'width': '48%', 'display': 'inline-block'}
                ),
            ],
            style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}
        ),
    ],
    style={
        'padding': '20px', 
        'fontFamily': 'Roboto, sans-serif', 
        'backgroundColor': '#ecf0f1',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
        'borderRadius': '10px'
    }
)

# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
