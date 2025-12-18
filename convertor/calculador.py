import json

# Carrega os pontos
with open("../pontos.json", "r", encoding="utf-8") as f:
    pontos = json.load(f)

if not pontos:
    print("Nenhum ponto encontrado")
    exit()

soma_lat = 0
soma_lng = 0
peso_total = 0

for p in pontos:
    # peso = quantidade de pedidos
    peso = p.get("pedidos", 1)  # se não existir, assume 1

    soma_lat += p["lat"] * peso
    soma_lng += p["lng"] * peso
    peso_total += peso

melhor_lat = soma_lat / peso_total
melhor_lng = soma_lng / peso_total

melhor_ponto = {
    "lat": melhor_lat,
    "lng": melhor_lng
}

# Salva resultado
with open("../melhor_ponto.json", "w", encoding="utf-8") as f:
    json.dump(melhor_ponto, f, indent=2)

print("📍 Melhor ponto calculado:")
print(melhor_ponto)
