import os

# --- DEFINIÇÃO DOS CÓDIGOS ---

codigo_main = r"""
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
"""

codigo_manager = r"""
import json
import paho.mqtt.client as mqtt
import time

class CommunicationManager:
    def __init__(self, mode="LOCAL"):
        self.mode = mode
        self.carros = {}
        self.central = None
        self.broker = "test.mosquitto.org"
        self.port = 1883
        self.base_topic = "projeto_trafego_aluno_xyz/v1" 
        
        if self.mode == "MQTT":
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            print(f"[MQTT] Conectando ao broker {self.broker}...")
            try:
                self.client.connect(self.broker, self.port, 60)
                self.client.loop_start()
            except Exception as e:
                print(f"[ERRO MQTT] {e}")

    def registrar_carro(self, carro_obj):
        self.carros[carro_obj.id] = carro_obj
        if self.mode == "MQTT":
            topic = f"{self.base_topic}/{carro_obj.id}"
            self.client.subscribe(topic)
            print(f"[MQTT] Carro {carro_obj.id} ouvindo: {topic}")

    def registrar_central(self, central_obj):
        self.central = central_obj
        if self.mode == "MQTT":
            topic = f"{self.base_topic}/CENTRAL"
            self.client.subscribe(topic)
            print(f"[MQTT] Central ouvindo: {topic}")

    def enviar_mensagem(self, remetente, destino, tipo, dados):
        msg = {"remetente": remetente, "tipo": tipo, "dados": dados}
        if self.mode == "LOCAL":
            self._enviar_local(remetente, destino, tipo, dados)
        elif self.mode == "MQTT":
            self._enviar_mqtt(destino, msg)

    def _enviar_local(self, remetente, destino, tipo, dados):
        if destino == "CENTRAL" and self.central:
            self.central.receber_mensagem(remetente, tipo, dados)
        elif destino in self.carros:
            self.carros[destino].receber_mensagem(remetente, tipo, dados)

    def _enviar_mqtt(self, destino_id, payload):
        topic = f"{self.base_topic}/{destino_id}"
        self.client.publish(topic, json.dumps(payload))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0: print("[MQTT] Conectado com sucesso!")
        else: print(f"[MQTT] Erro conexão: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            destino_real = msg.topic.split('/')[-1]
            if destino_real == "CENTRAL" and self.central:
                self.central.receber_mensagem(payload['remetente'], payload['tipo'], payload['dados'])
            elif destino_real in self.carros:
                self.carros[destino_real].receber_mensagem(payload['remetente'], payload['tipo'], payload['dados'])
        except: pass
"""

codigo_car = r"""
import math

class Car:
    def __init__(self, id_carro, comunicador, pos_inicial=(0,0)):
        self.id = id_carro
        self.comunicador = comunicador
        self.pos = list(pos_inicial)
        self.velocidade = 0 
        self.destino_atual = None
        self.rota = []
        self.indice_rota = 0
        self.comunicador.registrar_carro(self)

    def atualizar_fisica(self):
        if self.velocidade > 0 and self.rota and self.indice_rota < len(self.rota):
            alvo = self.rota[self.indice_rota]
            dx = alvo[0] - self.pos[0]
            dy = alvo[1] - self.pos[1]
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist < 1.0:
                self.pos = list(alvo)
                self.indice_rota += 1
                if self.indice_rota >= len(self.rota):
                    self.velocidade = 0
                    self.rota = []
                    self.comunicador.enviar_mensagem(self.id, "CENTRAL", "CHEGUEI", {"pos": self.pos})
                return

            passo = self.velocidade
            if passo >= dist:
                self.pos = list(alvo)
                self.indice_rota += 1
            else:
                fator = passo / dist
                self.pos[0] += dx * fator
                self.pos[1] += dy * fator

    def enviar_status(self):
        msg = {"pos": self.pos, "vel": self.velocidade, "status": "LIVRE" if not self.rota else "ANDANDO"}
        self.comunicador.enviar_mensagem(self.id, "CENTRAL", "STATUS", msg)

    def receber_mensagem(self, remetente, tipo, dados):
        if tipo == "MOVER":
            if 'velocidade' in dados: self.velocidade = dados['velocidade']
            if 'destino' in dados:
                self.destino_atual = dados['destino']
                self.rota = [ [dados['destino'][0], self.pos[1]], dados['destino'] ] # Rota em L
                if math.dist(self.pos, self.rota[0]) < 1: self.rota.pop(0)
                self.indice_rota = 0
"""

codigo_central = r"""
class Central:
    def __init__(self, comunicador, config_cidade):
        self.comunicador = comunicador
        self.frota_estados = {} 
        self.bloqueados = set()
        self.historico = {} 
        self.comunicador.registrar_central(self)

    def receber_mensagem(self, remetente, tipo, dados):
        if tipo == "STATUS":
            self.frota_estados[remetente] = dados
            self._salvar_historico(remetente, dados)
        elif tipo == "CHEGUEI":
            print(f"[CENTRAL] {remetente} chegou ao destino.")

    def _salvar_historico(self, id_carro, dados):
        if id_carro not in self.historico: self.historico[id_carro] = []
        self.historico[id_carro].append({"pos": list(dados['pos']), "vel": dados.get('vel', 0)})

    def monitorar_seguranca(self):
        ids = list(self.frota_estados.keys())
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                id_a, id_b = ids[i], ids[j]
                pos_a, pos_b = self.frota_estados[id_a]['pos'], self.frota_estados[id_b]['pos']
                dist = ((pos_a[0]-pos_b[0])**2 + (pos_a[1]-pos_b[1])**2)**0.5
                
                if dist < 40:
                    if id_a not in self.bloqueados:
                        print(f"🛑 [CENTRAL] ALERTA COLISÃO! Parando {id_a}...")
                        self._enviar_ordem(id_a, velocidade=0)
                        self.bloqueados.add(id_a)
                elif dist > 60:
                    if id_a in self.bloqueados:
                        print(f" [CENTRAL] Liberando {id_a}...")
                        self._enviar_ordem(id_a, velocidade=30)
                        self.bloqueados.remove(id_a)

    def _enviar_ordem(self, id_carro, destino=None, velocidade=None):
        cmd = {}
        if destino: cmd["destino"] = destino
        if velocidade is not None: cmd["velocidade"] = velocidade
        if cmd: self.comunicador.enviar_mensagem("CENTRAL", id_carro, "MOVER", cmd)
            
    def exibir_relatorio_final(self):
        print("\n=== RELATÓRIO HISTÓRICO ===")
        for id_carro, logs in self.historico.items():
            print(f"Carro {id_carro}: {len(logs)} registros.")
"""

# --- CRIAÇÃO DA ESTRUTURA ---

def criar_arquivo(caminho, conteudo):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Arquivo criado: {caminho}")

# Criar pastas
os.makedirs("projeto_trafego/entities", exist_ok=True)
os.makedirs("projeto_trafego/communication", exist_ok=True)

# Criar arquivos vazios (__init__)
criar_arquivo("projeto_trafego/__init__.py", "")
criar_arquivo("projeto_trafego/entities/__init__.py", "")
criar_arquivo("projeto_trafego/communication/__init__.py", "")

# Criar arquivos com código
criar_arquivo("main.py", codigo_main)
criar_arquivo("projeto_trafego/communication/manager.py", codigo_manager)
criar_arquivo("projeto_trafego/entities/car.py", codigo_car)
criar_arquivo("projeto_trafego/entities/central.py", codigo_central)

print("\nSUCESSO! Toda a estrutura foi criada.")
print("👉 Agora digite no terminal: python main.py")