
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
