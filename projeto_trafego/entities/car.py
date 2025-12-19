# ARQUIVO: entities/car.py
class Carro:
    def __init__(self, id_carro, comm_manager, x_inicial, y_inicial):
        self.id = id_carro
        self.comm_manager = comm_manager
        self.comm_manager.registrar_ouvinte(self.id, self)
        
        # Física e Estado
        self.x = x_inicial
        self.y = y_inicial
        self.velocidade = 0  # m/s (começa parado)
        self.rua_atual = "RUA_H1" # Exemplo: Começa na rua horizontal
        self.destino_x = None

    def receber_mensagem(self, remetente, tipo, dados):
        # A Central manda mudar velocidade para evitar colisão [cite: 26, 43]
        if tipo == "MUDAR_VELOCIDADE":
            nova_vel = dados.get("valor")
            self.velocidade = nova_vel
            print(f"   🚗 [{self.id}] Velocidade alterada para {self.velocidade} m/s")

        elif tipo == "DEFINIR_DESTINO":
            self.destino_x = dados.get("x")
            print(f"   🚗 [{self.id}] Novo destino recebido: X={self.destino_x}")
            # Começa a andar
            self.velocidade = 10 

    def tick(self, delta_tempo):
        """
        Método chamado a cada 'frame' da simulação.
        Atualiza a posição (Física de Tempo Discreto).
        """
        if self.velocidade > 0 and self.destino_x is not None:
            # Move o carro: Espaço = Velocidade * Tempo
            deslocamento = self.velocidade * delta_tempo
            
            # Lógica simples para andar no eixo X (Rua Horizontal)
            if self.x < self.destino_x:
                self.x += deslocamento
            
            # Envia relatório periódico para a central [cite: 45]
            dados_status = {"x": self.x, "y": self.y, "vel": self.velocidade}
            self.comm_manager.enviar_mensagem(self.id, "CENTRAL_MAIN", "STATUS_CARRO", dados_status)