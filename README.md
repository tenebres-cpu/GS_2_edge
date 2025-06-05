Nome: Marcelo Affonso Fonseca
RM: 559790



📌 Visão Geral
Este projeto demonstra um sistema completo de monitoramento de temperatura e umidade usando para problema com enchentes:

Simulação no Wokwi: ESP32 virtual + sensor DHT11.

Dashboard em Python: Gráficos interativos em tempo real.

Ideal para estudos de IoT, prototipagem rápida e visualização de dados.

🖥️ (Wokwi) https://wokwi.com/projects/432574060536281089
O Wokwi é uma plataforma de simulação online para projetos de eletrônica e IoT. Neste projeto, ele foi usado para:

🔧 Configuração no Wokwi
Circuito Virtual:

ESP32 conectado ao sensor DHT11 via GPIO4.

Alimentação: 3.3V.

Sem necessidade de hardware físico inicialmente.

Funcionamento:

O sensor gera dados fictícios de temperatura e umidade.

Os dados são exibidos no Serial Monitor do Wokwi.

Vantagens:

Teste rápido sem riscos de danificar componentes.


📊 Dashboard Python
Os dados simulados (ou reais, se usando hardware físico) são enviados para um servidor local que exibe:

Gráficos de temperatura (°C) e umidade (%) atualizados a cada 2 segundos.

Interface acessível em http://127.0.0.1:8050.

Tecnologias:

Python + Dash/Plotly para visualização.

🚀 Como Executar
1. Simulação no Wokwi
Acesse o link do projeto Wokwi.

Inicie a simulação e observe os dados no Serial Monitor.

2. Dashboard Python
Instale as dependências:

bash
pip install dash plotly
Execute:

python grafico.py
🎯 Aplicações
Monitoramento ambiental (estufas, salas de servidor, enchente).


Aprendizado de integração entre hardware e software.
