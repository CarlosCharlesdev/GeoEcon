import pandas as pd
import requests
import json
import time
import os

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImUwZmVlZjNhNjBhMDQwOWI5MWJlNDdiN2U2MDVlNTgwIiwiaCI6Im11cm11cjY0In0="

df = pd.read_excel("planilha_limpa.xlsx")

OUTPUT_FILE = "../pontos.json"

# Se já existir, carrega pra continuar
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        try:
            pontos = json.load(f)
        except json.JSONDecodeError:
            pontos = []
else:
    pontos = []

enderecos_processados = {
    f"{p['rua']}-{p['numero']}" for p in pontos
}

print(f"🔁 Retomando. Já existem {len(pontos)} pontos salvos.")

for _, row in df.iterrows():
    chave = f"{row['Rua']}-{row['Numero']}"

    # Pula se já foi convertido
    if chave in enderecos_processados:
        continue

    endereco = f"{row['Rua']}, {row['Numero']}, Porto Velho - RO"

    try:
        url = "https://api.openrouteservice.org/geocode/search"
        params = {
            "api_key": API_KEY,
            "text": endereco,
            "size": 1
        }

        r = requests.get(url, params=params, timeout=10)

        # RATE LIMIT / BLOQUEIO
        if r.status_code in [401, 403, 429]:
            print("🚨 LIMITE DA API ATINGIDO. Salvando e pausando...")
            break

        if r.status_code == 200:
            data = r.json()
            if data.get("features"):
                coords = data["features"][0]["geometry"]["coordinates"]

                ponto = {
                    "rua": row["Rua"],
                    "numero": int(row["Numero"]),
                    "bairro": row["Bairro"],
                    "cep": int(row["CEP"]),
                    "pedidos": int(row["Pedidos"]),
                    "lat": coords[1],
                    "lng": coords[0]
                }

                pontos.append(ponto)
                enderecos_processados.add(chave)

                # 🔥 SALVA IMEDIATAMENTE
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(pontos, f, indent=2, ensure_ascii=False)

                print("✅ OK:", endereco)

            else:
                print("❌ Não encontrado:", endereco)

        else:
            print("⚠️ Erro API:", r.status_code)

    except Exception as e:
        print("❌ Erro inesperado:", e)
        time.sleep(5)

    time.sleep(0.15)  # seguro pro ORS

print("🏁 Conversão finalizada (ou pausada com segurança).")
