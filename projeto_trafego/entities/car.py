# ARQUIVO: entities/car.py
import math

class Carro:
    def __init__(self, id_carro, manager, x_inicial, y_inicial):
        self.id = id_carro
        self.manager = manager
        self.manager.registrar_ouvinte(self.id, self)
        
        # Posição 2D
        self.x = x_inicial
        self.y = y_inicial
        
        self.velocidade = 0 
        
        # Vetor de Direção: (1, 0) = Direita | (0, 1) = Cima
        self.dir_x = 1 
        self.dir_y = 0
        
        self.ja_virou = False # Para garantir que ele só vira uma vez no cruzamento

    def receber_mensagem(self, remetente, tipo, dados):
        if tipo == "MUDAR_VELOCIDADE":
            self.velocidade = dados["valor"]
            print(f"   🚗 [{self.id}] Nova velocidade: {self.velocidade} m/s")
            
        elif tipo == "VIRAR_ESQUERDA":
            if not self.ja_virou:
                print(f"   ↩️ [{self.id}] Recebeu ordem para VIRAR!")
                # Matemática: Para virar 90 graus à esquerda
                # Se estava indo p/ Direita (1,0) -> Vai p/ Cima (0,1)
                self.dir_x = 0
                self.dir_y = 1
                self.ja_virou = True # Marca que a curva foi feita

    def tick(self, delta_tempo):
        if self.velocidade > 0:
            # FÍSICA VETORIAL:
            # Posição = Posição + (Velocidade * Direção * Tempo)
            self.x += self.velocidade * self.dir_x * delta_tempo
            self.y += self.velocidade * self.dir_y * delta_tempo
            
            # Envia posição atualizada para a Central
            self.manager.enviar_mensagem(self.id, "CENTRAL_MAIN", "STATUS_CARRO", 
                                         {"x": self.x, "y": self.y, "vel": self.velocidade})