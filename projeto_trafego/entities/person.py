# ARQUIVO: entities/person.py

class Person:
    def __init__(self, id_pessoa, comm_manager):
        self.id = id_pessoa
        self.comm_manager = comm_manager
        self.comm_manager.registrar_ouvinte(self.id, self)

    def receber_mensagem(self, remetente, tipo, dados):
        # Por enquanto a pessoa apenas recebe confirmações passivamente
        pass 

    def solicitar_uber(self):
        print(f"   🧍 [{self.id}] A solicitar Uber...")
        # Envia pedido para a Central
        self.comm_manager.enviar_mensagem(self.id, "CENTRAL_MAIN", "QUERO_CARRO", {})