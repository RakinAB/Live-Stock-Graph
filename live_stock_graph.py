import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import time

# Function to fetch and process data
def fetch_data(ticker):
    # Fetch data
    data = yf.download(ticker, period='1d', interval='1m')
    
    # Calculate moving average
    data['SMA'] = data['Close'].rolling(window=20).mean()
    
    # Calculate Bollinger Bands
    data['BB_upper'] = data['SMA'] + 2 * data['Close'].rolling(window=20).std()
    data['BB_lower'] = data['SMA'] - 2 * data['Close'].rolling(window=20).std()
    
   
    return data

# Function to create the plot
def create_plot(data, ticker):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.7, 0.3], vertical_spacing=0.1)
    
    # Add candlestick trace
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ),
        row=1, col=1
    )
    
    # Add moving average trace
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['SMA'],
            mode='lines',
            name='SMA',
            line=dict(color='blue')
        ),
        row=1, col=1
    )
    
    # Add Bollinger Bands traces
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['BB_upper'],
            mode='lines',
            name='BB Upper',
            line=dict(color='red')
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['BB_lower'],
            mode='lines',
            name='BB Lower',
            line=dict(color='red')
        ),
        row=1, col=1
    )
    
    # Fill between Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['BB_upper'],
            mode='lines',
            line=dict(color='rgba(255,0,0,0)'),
            showlegend=False
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['BB_lower'],
            mode='lines',
            line=dict(color='rgba(255,0,0,0)'),
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.1)',
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Add volume trace
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color='lightgray'
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        template='plotly_dark',
        title=f'{ticker} Live Price',
        xaxis_title='Time',
        yaxis_title='Price',
        yaxis2_title='Volume',
        xaxis_rangeslider_visible=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

# Create the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Live Stock Price Chart", className="text-center text-light mb-4"),
                width=12
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='live-graph', style={'height': '100vh'}),
                width=12
            )
        ),
        dcc.Interval(
            id='interval-component',
            interval=60*1000,  # in milliseconds
            n_intervals=0
        )
    ],
    fluid=True,
    className="bg-dark"
)

@app.callback(Output('live-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    ticker = 'NVDA'
    data = fetch_data(ticker)
    fig = create_plot(data, ticker)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)