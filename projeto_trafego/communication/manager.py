
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
