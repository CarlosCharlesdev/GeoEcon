import pandas as pd
from geopy.geocoders import Nominatim
import time
import json
import re
import unicodedata

geolocator = Nominatim(user_agent="geoecon")

df = pd.read_excel("planilha_limpa.xlsx", header=None)

pontos = []

def normalizar(texto):
    if not isinstance(texto, str):
        return ""

    texto = texto.strip().upper()

    texto = texto.replace("AV. ", "AVENIDA ")
    texto = texto.replace("AV ", "AVENIDA ")
    texto = texto.replace("R. ", "RUA ")
    texto = texto.replace("R ", "RUA ")
    texto = texto.replace("AL. ", "ALAMEDA ")
    texto = texto.replace("TRAV. ", "TRAVESSA ")

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))

    texto = re.sub(r"\s+", " ", texto)
    return texto

for _, row in df.iterrows():
    rua = normalizar(row[0])
    numero = row[1]
    bairro = normalizar(row[2])
    cep = row[3]

    tentativas = [
        f"{rua}, {numero}, {bairro}, Porto Velho - RO, {cep}",
        f"{rua}, {numero}, Porto Velho - RO, {cep}",
        f"{rua}, {numero}, Porto Velho - RO",
        f"{rua}, Porto Velho - RO"
    ]

    location = None

    for endereco in tentativas:
        try:
            location = geolocator.geocode(endereco, timeout=10)
            if location:
                print("✅ OK:", endereco)
                break
        except Exception as e:
            print("Erro:", e)
            time.sleep(5)

    if location:
        pontos.append({
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cep": cep,
            "lat": location.latitude,
            "lng": location.longitude
        })
    else:
        print("❌ Não encontrado:", rua, numero)

    time.sleep(1)  # RESPEITA o Nominatim

with open("pontos.json", "w", encoding="utf-8") as f:
    json.dump(pontos, f, ensure_ascii=False, indent=2)

print("✅ pontos.json gerado com sucesso")
