import time
import config
from communication.manager import CommunicationManager
from entities.central import Central
from entities.car import Carro
from entities.person import Person
from entities.city import CityMap

def main():
    manager = CommunicationManager(mode="MQTT")
    cidade = CityMap() 
    central = Central(manager)
    
    # --- CRIAÇÃO ---
    print("\n--- A Configurar Entidades ---")
    carros = []
    for c_conf in config.CARS_CONFIG:
        novo_carro = Carro(c_conf["id"], manager, c_conf["x"], c_conf["y"])
        novo_carro.velocidade = 0 # Começa parado esperando chamado
        carros.append(novo_carro)

    pessoas = []
    for p_conf in config.PEOPLE_CONFIG:
        nova_pessoa = Person(p_conf["id"], manager)
        pessoas.append(nova_pessoa)

    time.sleep(2) 
    print("\n--- INICIANDO SIMULAÇÃO (1 CARRO, 2 PESSOAS) ---")

    tempo_total = 0
    delta_t = config.TIME_STEP
    
    try:
        while tempo_total < config.SIMULATION_DURATION:
            print(f"\n--- Tempo: {tempo_total}s ---")
            
            # --- EVENTO 1: JOÃO PEDE O CARRO (No tempo 5s) ---
            if tempo_total == 5:
                print(f"   📢 [EVENTO] {pessoas[0].id} pediu um carro!")
                pessoas[0].solicitar_uber()
                # A Central manda o carro andar (Simulando o atendimento)
                manager.enviar_mensagem("CENTRAL", "UBER_01", "MUDAR_VELOCIDADE", {"valor": 15})
                print("   🚕 Carro iniciou a corrida para JOAO.")

            # --- EVENTO 2: MARIA PEDE O CARRO (No tempo 35s) ---
            # O carro já andou bastante (atendeu o João), agora vai atender a Maria
            if tempo_total == 35:
                print(f"   📢 [EVENTO] {pessoas[1].id} pediu um carro!")
                pessoas[1].solicitar_uber()
                # O carro continua andando (ou muda de velocidade/direção) para a Maria
                print("   🚕 Carro finalizou João e foi buscar MARIA.")

            # Avança a simulação
            central.tick(delta_t)
            for carro in carros:
                carro.tick(delta_t)
            
            tempo_total += delta_t
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print("Parando...")

    central.gerar_grafico()
    manager.client.loop_stop()

if __name__ == "__main__":
    main()