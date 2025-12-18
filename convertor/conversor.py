import pandas as pd
from geopy.geocoders import Nominatim
import time
import json

geolocator = Nominatim(user_agent="geoecon")

# Lê sem cabeçalho
df = pd.read_excel("planilha_limpa.xlsx", header=None)

pontos = []

for _, row in df.iterrows():
    rua = row[0]
    numero = row[1]
    bairro = row[2]
    cep = row[3]

    endereco = f"{rua}, {numero}, {bairro}, Porto Velho - RO, {cep}"

    location = geolocator.geocode(endereco)

    if location:
        pontos.append({
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cep": cep,
            "lat": location.latitude,
            "lng": location.longitude
        })
        print("OK:", endereco)
    else:
        print("Não encontrado:", endereco)

    time.sleep(1)

with open("pontos.json", "w", encoding="utf-8") as f:
    json.dump(pontos, f, ensure_ascii=False, indent=2)

print("pontos.json gerado")
