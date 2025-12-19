# ARQUIVO: entities/central.py
import matplotlib.pyplot as plt

class Central:
    def __init__(self, comm_manager):
        self.id = "CENTRAL_MAIN"
        self.comm_manager = comm_manager
        self.comm_manager.registrar_ouvinte(self.id, self)
        
        self.historico = {}
        # Novo dicionário para saber onde cada carro está AGORA (última posição recebida)
        self.posicoes_atuais = {} 
        self.tempo_simulacao = 0

    def receber_mensagem(self, remetente, tipo, dados):
        if tipo == "STATUS_CARRO":
            x_atual = dados.get("x")
            
            # 1. Guarda Histórico para o Gráfico
            if remetente not in self.historico:
                self.historico[remetente] = []
            self.historico[remetente].append((self.tempo_simulacao, x_atual))
            
            # 2. Atualiza Posição Atual para Cálculos de Colisão
            self.posicoes_atuais[remetente] = x_atual
            
            # 3. Verifica Colisão (A Lógica Inteligente)
            self.verificar_distancia_seguranca(remetente, x_atual)

        elif tipo == "QUERO_CARRO":
             print(f"   🏢 [CENTRAL] Pedido de {remetente}.")
             # Aqui normalmente haveria lógica de escolha de carro, 
             # mas no main.py forçamos manualmente para o teste.

    def verificar_distancia_seguranca(self, carro_id, x_atual):
        # Compara este carro com todos os outros
        for outro_carro, x_outro in self.posicoes_atuais.items():
            if carro_id == outro_carro:
                continue # Não comparar com ele mesmo
            
            distancia = x_outro - x_atual
            
            # Se o outro carro estiver à frente (distancia positiva) e muito perto (< 30 metros)
            if 0 < distancia < 30:
                print(f"   ⚠️ PERIGO: {carro_id} está muito perto de {outro_carro} ({distancia:.1f}m)!")
                print(f"   🛑 ENVIANDO COMANDO DE FREAR PARA {carro_id}")
                self.comm_manager.enviar_mensagem(self.id, carro_id, "MUDAR_VELOCIDADE", {"valor": 0}) # Para o carro
            
            # (Opcional) Se a distância voltar a ser segura, poderia mandar andar de novo, 
            # mas vamos manter simples por enquanto.

    def tick(self, delta_tempo):
        self.tempo_simulacao += delta_tempo

    def gerar_grafico(self):
        print("Gerando gráfico...")
        plt.figure(figsize=(10, 6))
        for carro_id, dados in self.historico.items():
            tempos = [d[0] for d in dados]
            posicoes = [d[1] for d in dados]
            plt.plot(tempos, posicoes, label=carro_id, linewidth=2)
        
        plt.xlabel("Tempo (s)")
        plt.ylabel("Posição X (m)")
        plt.title("Simulação de Tráfego: Teste de Colisão")
        plt.legend()
        plt.grid(True)
        plt.show()