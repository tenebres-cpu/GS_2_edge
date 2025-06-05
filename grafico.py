import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import paho.mqtt.client as mqtt
from datetime import datetime
import json
import threading

# Configuração MQTT
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "fiware/sensor/dht11"

# Dados recebidos (agora mantendo apenas 3 valores)
data = {
    "temperature": [],
    "humidity": [],
    "time": []
}

# Inicializar o dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Monitoramento de Temperatura e Umidade (DHT11)", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Graph(id='temperature-graph'),
        dcc.Interval(id='interval-update', interval=2000, n_intervals=0)
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='humidity-graph'),
    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
])

# Callback para atualizar os gráficos
@app.callback(
    Output('temperature-graph', 'figure'),
    Output('humidity-graph', 'figure'),
    Input('interval-update', 'n_intervals')
)
def update_graphs(n):
    # Mostrar apenas os últimos 3 valores
    display_data = {
        "temperature": data["temperature"][-3:],
        "humidity": data["humidity"][-3:],
        "time": data["time"][-3:]
    }
    
    # Gráfico de barras para temperatura
    temp_fig = {
        'data': [go.Bar(
            x=display_data['time'],
            y=display_data['temperature'],
            name='Temperatura (°C)',
            marker_color='coral',
            width=0.5
        )],
        'layout': go.Layout(
            title='Temperatura (Últimas 3 leituras)',
            yaxis={'title': '°C'},
            xaxis={'title': 'Tempo'},
            plot_bgcolor='#f9f9f9'
        )
    }
    
    # Gráfico de barras para umidade
    humidity_fig = {
        'data': [go.Bar(
            x=display_data['time'],
            y=display_data['humidity'],
            name='Umidade (%)',
            marker_color='lightblue',
            width=0.5
        )],
        'layout': go.Layout(
            title='Umidade (Últimas 3 leituras)',
            yaxis={'title': '%'},
            xaxis={'title': 'Tempo'},
            plot_bgcolor='#f9f9f9'
        )
    }
    
    return temp_fig, humidity_fig

# Funções MQTT para receber dados
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT (código {rc})")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("Dados recebidos:", payload)
        
        # Adiciona novos dados
        data['temperature'].append(payload['temperature'])
        data['humidity'].append(payload['humidity'])
        data['time'].append(datetime.now().strftime("%H:%M:%S"))
        
        # Mantém no máximo 20 valores na memória (mas só mostra os últimos 3)
        if len(data['temperature']) > 20:
            data['temperature'] = data['temperature'][-20:]
            data['humidity'] = data['humidity'][-20:]
            data['time'] = data['time'][-20:]
    except Exception as e:
        print("Erro ao processar mensagem:", e)

# Configurar cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Iniciar loop MQTT em uma thread separada
mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
mqtt_thread.daemon = True
mqtt_thread.start()

if __name__ == '__main__':
    app.run(debug=True, port=8050)