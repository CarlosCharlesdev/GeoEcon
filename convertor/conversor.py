import pandas as pd
from geopy.geocoders import Nominatim
import time
import json
import re
import unicodedata

geolocator = Nominatim(user_agent="geoecon")

df = pd.read_excel("planilha_limpa.xlsx", header=None)

pontos = []
erros = []  # ← LISTA DE ERROS

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


for index, row in df.iterrows():
    linha_excel = index + 1  # mesma linha do Excel

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
    endereco_usado = ""

    for endereco in tentativas:
        try:
            location = geolocator.geocode(endereco, timeout=10)
            if location:
                print(f"✅ OK (linha {linha_excel}):", endereco)
                endereco_usado = endereco
                break
        except Exception as e:
            print("Erro:", e)
            time.sleep(5)

    if location:
        pontos.append({
            "linha": linha_excel,
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cep": cep,
            "lat": location.latitude,
            "lng": location.longitude
        })
    else:
        print(f"❌ ERRO (linha {linha_excel}):", rua, numero)

        erros.append({
            "linha_excel": linha_excel,
            "rua": row[0],
            "numero": numero,
            "bairro": row[2],
            "cep": cep
        })

    time.sleep(1)  # respeita o Nominatim


# =========================
# SALVA OS ARQUIVOS
# =========================

with open("pontos.json", "w", encoding="utf-8") as f:
    json.dump(pontos, f, ensure_ascii=False, indent=2)

if erros:
    df_erros = pd.DataFrame(erros)
    df_erros.to_excel("enderecos_com_erro.xlsx", index=False)

print("\n✅ pontos.json gerado com sucesso")
print(f"📍 Total de pontos válidos: {len(pontos)}")
print(f"⚠️ Total de erros: {len(erros)}")

if erros:
    print("🧾 Planilha 'enderecos_com_erro.xlsx' criada para correção manual")
