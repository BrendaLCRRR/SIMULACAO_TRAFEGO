import json
import time
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

class CommunicationManager:
    def __init__(self, mode="MQTT"):
        self.mode = mode
        self.listeners = {} 
        # Prefixo único para evitar conflito no servidor público
        self.topic_prefix = "projeto_trafego_aluno_xyz/v1/"
        
        if self.mode == "MQTT":
            # Configuração atualizada para Paho MQTT v2.0
            self.client = mqtt.Client(
                callback_api_version=CallbackAPIVersion.VERSION2,
                client_id="" # ID vazio = gera aleatório
            )
            
            # Vincula os callbacks
            self.client.on_message = self._on_message
            self.client.on_connect = self._on_connect
            
            try:
                # Conecta ao broker público (para testes)
                print("[SISTEMA] Conectando ao Broker MQTT...")
                self.client.connect("test.mosquitto.org", 1883, 60)
                self.client.loop_start() # Inicia a thread de escuta em background
            except Exception as e:
                print(f"[ERRO FATAL] Não foi possível conectar: {e}")

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print(f"[MQTT] Conexão estabelecida com sucesso!")
        else:
            print(f"[MQTT] Falha na conexão. Código: {reason_code}")

    def registrar_ouvinte(self, id_entidade, entidade):
        """Associa um ID (ex: 'CAR_01') ao objeto Python correspondente"""
        self.listeners[id_entidade] = entidade
        
        if self.mode == "MQTT":
            topic = f"{self.topic_prefix}{id_entidade}"
            self.client.subscribe(topic)
            print(f"[REDE] Objeto '{id_entidade}' registrado no tópico: .../{id_entidade}")

    def enviar_mensagem(self, remetente_id, destinatario_id, tipo, dados):
        payload_dict = {
            "remetente": remetente_id,
            "tipo": tipo,
            "dados": dados
        }
        payload_str = json.dumps(payload_dict)
        
        if self.mode == "MQTT":
            topic = f"{self.topic_prefix}{destinatario_id}"
            self.client.publish(topic, payload_str, qos=1)
            print(f"--> [ENVIADO] De {remetente_id} para {destinatario_id}: {tipo}")

    def _on_message(self, client, userdata, msg):
        """Recebe do Broker e entrega para o objeto Python correto"""
        try:
            payload = json.loads(msg.payload.decode())
            # Pega quem é o destinatário baseado no final do tópico
            destinatario_real = msg.topic.split("/")[-1]
            
            if destinatario_real in self.listeners:
                entidade = self.listeners[destinatario_real]
                
                #Chama o método receber_mensagem da classe específica
                if hasattr(entidade, 'receber_mensagem'):
                    entidade.receber_mensagem(payload["remetente"], payload["tipo"], payload["dados"])
            
        except Exception as e:
            print(f"[ERRO REDE] {e}")