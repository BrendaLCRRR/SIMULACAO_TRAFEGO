# ARQUIVO: entities/central.py
import matplotlib.pyplot as plt
import math

class Central:
    def __init__(self, comm_manager):
        self.id = "CENTRAL_MAIN"
        self.comm_manager = comm_manager
        self.comm_manager.registrar_ouvinte(self.id, self)
        
        # Histórico guarda (X, Y) para desenhar o trajeto
        self.historico = {} 
        self.posicoes_atuais = {} 

    def receber_mensagem(self, remetente, tipo, dados):
        if tipo == "STATUS_CARRO":
            x = dados["x"]
            y = dados["y"]
            
            # 1. Guarda Histórico (Trajetória)
            if remetente not in self.historico:
                self.historico[remetente] = {"x": [], "y": []}
            self.historico[remetente]["x"].append(x)
            self.historico[remetente]["y"].append(y)
            
            self.posicoes_atuais[remetente] = {"x": x, "y": y}
            
            # 2. Lógica de Tráfego e Curvas
            self.controlar_trafego(remetente, x, y)

    def controlar_trafego(self, id_carro, x, y):
        # A) VERIFICAR CRUZAMENTO (Exemplo: Rua Vertical no X=500)
        # Se o carro estiver perto de 500 (entre 495 e 505) e ainda estiver na rua de baixo (y < 60)
        if (490 < x < 510) and (y < 60):
            # Manda virar para a rua vertical
            self.comm_manager.enviar_mensagem(self.id, id_carro, "VIRAR_ESQUERDA", {})

        # B) EVITAR COLISÃO (Simplificado para Distância Euclidiana)
        for outro_id, pos in self.posicoes_atuais.items():
            if id_carro == outro_id: continue
            
            # Distância Pitágoras: Raiz((x2-x1)² + (y2-y1)²)
            dist = math.sqrt((x - pos["x"])**2 + (y - pos["y"])**2)
            
            # Se tiver alguém MUITO perto na frente (< 20m)
            if 0 < dist < 20:
                print(f"   ⚠️ PERIGO: {id_carro} quase batendo em {outro_id}!")
                self.comm_manager.enviar_mensagem(self.id, id_carro, "MUDAR_VELOCIDADE", {"valor": 0})

    def tick(self, delta_tempo):
        pass # O relógio avança, mas a lógica está no recebimento de msg

    def gerar_grafico(self):
        print("Gerando Mapa da Cidade...")
        plt.figure(figsize=(8, 8))
        
        # Desenhar as Ruas (Só para visualização)
        plt.axhline(y=50, color='gray', linestyle='--', linewidth=20, alpha=0.3, label="Rua Horizontal")
        plt.axvline(x=500, color='gray', linestyle='--', linewidth=20, alpha=0.3, label="Rua Vertical")
        
        # Desenhar Trajetórias dos Carros
        for carro_id, dados in self.historico.items():
            plt.plot(dados["x"], dados["y"], linewidth=3, label=f"Trajeto {carro_id}")
            # Marca o ponto final
            plt.scatter(dados["x"][-1], dados["y"][-1], s=100)

        plt.title("Mapa de Tráfego: Visão Superior (2D)")
        plt.xlabel("Posição X (metros)")
        plt.ylabel("Posição Y (metros)")
        plt.legend()
        plt.grid(True)
        plt.axis('equal') # Para o gráfico não ficar esticado
        plt.show()