# ARQUIVO: config.py

# Configurações da Simulação
SIMULATION_DURATION = 40  # Segundos de simulação
TIME_STEP = 1             # Quanto tempo passa por "tick"

# Configuração dos Carros (ID, Posição X, Posição Y, Velocidade Inicial)
CARS_CONFIG = [
    {"id": "CAR_01", "x": 0,   "y": 50, "speed": 20}, # Carro rápido atrás
    {"id": "CAR_02", "x": 300, "y": 50, "speed": 10}, # Carro lento à frente
    # Podes adicionar mais carros aqui facilmente
    # {"id": "CAR_03", "x": 600, "y": 50, "speed": 15},
]

# Configuração das Pessoas
PEOPLE_CONFIG = [
    {"id": "JOAO"},
    {"id": "MARIA"}
]

# Parâmetros de Segurança
SAFE_DISTANCE = 30 # Metros