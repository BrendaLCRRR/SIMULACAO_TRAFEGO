# ARQUIVO: entities/city.py
# Este arquivo define o mapa da cidade.

class CityMap:
    def __init__(self):
        # Exemplo simples: 1 Rua Horizontal e 1 Vertical que se cruzam
        # Horizontal: Vai do X=0 ao X=1000, na altura Y=50
        self.ruas = [
            {"id": "RUA_H1", "tipo": "H", "y": 50, "inicio": 0, "fim": 1000},
            {"id": "RUA_V1", "tipo": "V", "x": 500, "inicio": 0, "fim": 1000}
        ]
    
    def get_rua(self, id_rua):
        for rua in self.ruas:
            if rua["id"] == id_rua:
                return rua
        return None
