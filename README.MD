# 🚦 Simulação de Tráfego IoT com MQTT

Este projeto simula um sistema de controle de tráfego inteligente utilizando Python. O sistema monitora a posição de veículos autônomos e previne colisões em cruzamentos através de uma Central de Controle conectada via protocolo MQTT.

## 📋 Funcionalidades
- **Veículos Autônomos:** Entidades que se movem e reportam telemetria.
- **Central de Controle:** Monitora distâncias e envia ordens de parada/movimento.
- **Comunicação MQTT:** Uso de *broker* público (test.mosquitto.org) para comunicação em tempo real.
- **Prevenção de Colisões:** Algoritmo que detecta proximidade e freia carros automaticamente.

## 🚀 Como Rodar

1. Clone o repositório:
   ```bash
   git clone [https://github.com/BrendaLCRRR/SIMULACAO_TRAFEGO.git](https://github.com/BrendaLCRRR/SIMULACAO_TRAFEGO.git)