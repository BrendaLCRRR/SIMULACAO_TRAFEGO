# ARQUIVO: config.py

SIMULATION_DURATION = 60 
TIME_STEP = 1             

# --- CENÁRIO: 1 CARRO ÚNICO ---
CARS_CONFIG = [
    # Apenas 1 carro para atender todo mundo
    {"id": "UBER_01", "x": 0, "y": 50, "speed": 10}, 
]

# --- 2 PESSOAS ---
PEOPLE_CONFIG = [
    {"id": "JOAO_PRIMEIRO"}, # Vai pedir primeiro
    {"id": "MARIA_DEPOIS"}   # Vai pedir depois
]

SAFE_DISTANCE = 30