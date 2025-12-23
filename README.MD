# 🚖 Simulador de Tráfego Autônomo - Sistema de Atendimento ("Uber")

**Disciplina:** Introdução a Python em Engenharia
**Versão:** 3.0 (Lógica de Atendimento Sequencial)

## 📋 Descrição do Projeto
Este projeto simula um ambiente de tráfego inteligente onde veículos autônomos recebem ordens de uma **Central de Controlo via MQTT**.
O foco desta versão é a **Gestão de Recursos Compartilhados**: Um único carro deve atender a solicitações de passageiros diferentes em momentos distintos, sem conflitos.

## ⚙️ Cenário de Teste Atual (Versão 3)
O sistema está configurado para demonstrar o atendimento sequencial:
1.  **Recurso:** 1 Carro Autônomo (`UBER_01`).
2.  **Solicitantes:** 2 Passageiros (`JOAO` e `MARIA`).
3.  **Lógica:** O carro começa parado. Os pedidos ocorrem dinamicamente durante a execução.

### ⏱ Cronologia da Simulação
* **T = 0s:** Início da simulação. Carro aguarda na base.
* **T = 5s:** 🟢 **JOAO_PRIMEIRO** solicita o carro. A Central despacha o veículo (Velocidade sobe para 15 m/s).
* **T = 35s:** 🟡 **MARIA_DEPOIS** solicita o carro. O veículo, que já estava em movimento, recebe a nova ordem e continua o atendimento (simulando buscar o próximo passageiro).

## 🚀 Como Executar
1. Instale as dependências:
   ```bash
   pip install paho-mqtt matplotlib
