
import time
from projeto_trafego.communication.manager import CommunicationManager
from projeto_trafego.entities.car import Car
from projeto_trafego.entities.central import Central

def main():
    print(">>> INICIANDO SISTEMA DE TRÁFEGO VIA MQTT <<<")
    
    # Mude para "LOCAL" se estiver sem internet
    com_manager = CommunicationManager(mode="MQTT")
    
    # Pausa para conexão
    time.sleep(2) 

    central = Central(com_manager, config_cidade={})
    
    # Setup dos Carros
    carro_h = Car("CAR_H", com_manager, pos_inicial=(0, 100))
    carro_v = Car("CAR_V", com_manager, pos_inicial=(500, 0))

    print("[SETUP] Enviando rotas via rede...")
    # Simula envio da Central
    central._enviar_ordem("CAR_H", destino=(1000, 100), velocidade=30)
    central._enviar_ordem("CAR_V", destino=(500, 1000), velocidade=30)

    # Loop de Simulação
    for t in range(30):
        print(f"\n=== T = {t}s ===")
        
        carro_h.atualizar_fisica()
        carro_v.atualizar_fisica()
        
        carro_h.enviar_status()
        carro_v.enviar_status()
        
        central.monitorar_seguranca()
        
        # Distância visual
        dist = ((carro_h.pos[0] - carro_v.pos[0])**2 + (carro_h.pos[1] - carro_v.pos[1])**2)**0.5
        print(f"   Distância entre carros: {dist:.1f}m")
        
        time.sleep(1)

    print("\n--- FIM DA SIMULAÇÃO ---")
    central.exibir_relatorio_final()
    com_manager.client.loop_stop()

if __name__ == "__main__":
    main()
