
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
