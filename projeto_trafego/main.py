# ARQUIVO: main.py
import time
import config 
from communication.manager import CommunicationManager
from entities.central import Central
from entities.car import Carro
from entities.person import Person
from entities.city import CityMap

def main():
    manager = CommunicationManager(mode="MQTT")
    cidade = CityMap() # [cite: 56, 61]
    central = Central(manager)
    
    
    carros = []
    print("\n--- Configurando Entidades ---")
    
    # Cria todos os carros listados no config
    for c_conf in config.CARS_CONFIG:
        novo_carro = Carro(c_conf["id"], manager, c_conf["x"], c_conf["y"])
        # Define a velocidade inicial logo de cara para o teste
        novo_carro.velocidade = c_conf["speed"] 
        # Define um destino falso longe para eles andarem
        novo_carro.destino_x = 2000 
        carros.append(novo_carro)
        print(f"   🚗 Criado: {c_conf['id']} em X={c_conf['x']}")

    # Cria todas as pessoas
    pessoas = []
    for p_conf in config.PEOPLE_CONFIG:
        nova_pessoa = Person(p_conf["id"], manager)
        pessoas.append(nova_pessoa)

    time.sleep(2) # Tempo para conexões MQTT estabilizarem

    print("\n--- INICIANDO SIMULAÇÃO ---")
    
    # Loop de Tempo Discreto [cite: 12]
    tempo_total = 0
    
    try:
        while tempo_total < config.SIMULATION_DURATION:
            print(f"\n--- Tempo: {tempo_total}s ---")
            
            # 1. Avança a Central
            central.tick(config.TIME_STEP)
            
            # 2. Avança TODOS os carros da lista automaticamente
            for carro in carros:
                carro.tick(config.TIME_STEP)
            
            tempo_total += config.TIME_STEP
            time.sleep(0.2) # Pausa visual
            
    except KeyboardInterrupt:
        print("Parando...")

    # Gera o gráfico final
    central.gerar_grafico()
    manager.client.loop_stop()

if __name__ == "__main__":
    main()