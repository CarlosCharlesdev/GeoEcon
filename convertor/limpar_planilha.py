import pandas as pd

# Lê o Excel SEM cabeçalho
df = pd.read_excel("planilha-teste.xlsx", header=None)

# Renomeia colunas por posição
df.columns = ["Rua", "Numero", "Bairro", "CEP"]

# Remove linhas vaziasdf = df.dropna(subset=["Rua", "Numero", "Bairro", "CEP"])

# Padroniza textos
df["Rua"] = df["Rua"].astype(str).str.strip().str.upper()
df["Bairro"] = df["Bairro"].astype(str).str.strip().str.upper()

# Agrupa endereços iguais e conta pedidos
df_limpo = (
    df
    .groupby(["Rua", "Numero", "Bairro", "CEP"])
    .size()
    .reset_index(name="Pedidos")
)

# Salva planilha limpa
df_limpo.to_excel("planilha_limpa.xlsx", index=False)

print("✅ Planilha limpa criada com sucesso")
print(df_limpo.head())
