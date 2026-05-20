# ============================================================
# ANÁLISE DE COMÉRCIO EXTERIOR BRASILEIRO
# Fonte dos dados: ComexStat / SECEX / MDIC
# Endpoint:        https://api-comexstat.mdic.gov.br/general
# Documentação:    https://api-comexstat.mdic.gov.br/docs
# ============================================================

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# ============================================================
# CONFIGURAÇÕES DA ANÁLISE (mexa aqui)
# ============================================================

# Códigos NCM (Nomenclatura Comum do Mercosul) dos produtos
# Aceita um ou vários. Consulte a tabela completa no site do ComexStat
# Exemplos prontos:
#   Soja em grãos:            "12019000"
#   Minério de ferro:         "26011100"
#   Óleo bruto de petróleo:   "27090010"
#   Café não torrado:         "09011110"
#   Açúcar de cana:           "17011400"
NCM_CODES = ["12019000"]

# Nome apenas para rotular os gráficos (livre)
NOME_PRODUTO = "Soja em grãos"

# Janela temporal (anos completos)
ANO_INICIAL = 2019
ANO_FINAL   = 2025


# ============================================================
# FUNÇÃO QUE CONSULTA A API
# ============================================================

API_URL = "https://api-comexstat.mdic.gov.br/general"


def buscar_dados(flow, details, ncm_codes, ano_ini, ano_fim, month_detail=True):
    """
    Faz requisição POST à API do ComexStat.

    flow         : 'import' ou 'export'
    details      : lista de agrupamentos, ex. ['country'] ou []
    ncm_codes    : lista de NCMs (strings)
    ano_ini/fim  : anos de início e fim
    month_detail : True retorna série mensal, False agrega por período
    """
    # Monta o corpo da requisição no formato exigido pela API
    body = {
        "flow": flow,
        "monthDetail": month_detail,
        "period": {
            "from": f"{ano_ini}-01",
            "to":   f"{ano_fim}-12"
        },
        "filters": [
            {"filter": "ncm", "values": ncm_codes}
        ],
        "details": details,
        "metrics": ["metricFOB", "metricKG"]
    }

    # Chamada POST à API (pode demorar, daí o timeout generoso)
    resposta = requests.post(
        API_URL,
        json=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        timeout=180
    )
    resposta.raise_for_status()

    # Extrai a lista de registros (resposta sempre no formato {data: {list: [...]}})
    registros = resposta.json().get("data", {}).get("list", [])
    return pd.DataFrame(registros)


# ============================================================
# BUSCA OS DADOS
# ============================================================

print(f"\n  Buscando dados da ComexStat")
print(f"  Produto: {NOME_PRODUTO} | NCM: {NCM_CODES}")
print(f"  Período: {ANO_INICIAL} a {ANO_FINAL}\n")

# Série mensal de importação (sem quebra por país, só o total mensal)
df_imp = buscar_dados("import", [], NCM_CODES, ANO_INICIAL, ANO_FINAL, month_detail=True)

# Série mensal de exportação
df_exp = buscar_dados("export", [], NCM_CODES, ANO_INICIAL, ANO_FINAL, month_detail=True)

# Acumulado por país do período inteiro (sem mês)
df_imp_pais = buscar_dados("import", ["country"], NCM_CODES, ANO_INICIAL, ANO_FINAL, month_detail=False)
df_exp_pais = buscar_dados("export", ["country"], NCM_CODES, ANO_INICIAL, ANO_FINAL, month_detail=False)

print(f"  Importação mensal: {len(df_imp)} linhas")
print(f"  Exportação mensal: {len(df_exp)} linhas")


# ============================================================
# PROCESSA E LIMPA OS DADOS
# ============================================================

def processar_serie_mensal(df):
    """Converte valores numéricos, cria coluna data e agrega por mês."""
    if df.empty:
        return df
    # A API devolve valores como string, então converte para número
    df["metricFOB"] = pd.to_numeric(df["metricFOB"], errors="coerce")
    df["metricKG"]  = pd.to_numeric(df["metricKG"],  errors="coerce")
    # Monta coluna de data no primeiro dia do mês
    df["data"] = pd.to_datetime(
        df["year"].astype(str) + "-" +
        df["monthNumber"].astype(str).str.zfill(2) + "-01"
    )
    # Agrega caso existam múltiplos NCMs em um mesmo mês
    df = df.groupby("data", as_index=False).agg({"metricFOB": "sum", "metricKG": "sum"})
    df = df.sort_values("data").reset_index(drop=True)
    # Calcula preço implícito em US$ por tonelada (FOB / peso em kg * 1000)
    df["preco_usd_ton"] = (df["metricFOB"] / df["metricKG"]) * 1000
    return df


def processar_por_pais(df):
    """Limpa e encontra a coluna de nome de país."""
    if df.empty:
        return df, None
    df["metricFOB"] = pd.to_numeric(df["metricFOB"], errors="coerce")
    df["metricKG"]  = pd.to_numeric(df["metricKG"],  errors="coerce")
    # A API pode retornar a coluna de país com nomes diferentes dependendo do idioma
    # Testa os candidatos mais comuns
    col_pais = None
    for candidato in ["noPaisPor", "country", "noPais", "pais", "Country"]:
        if candidato in df.columns:
            col_pais = candidato
            break
    return df, col_pais


df_imp = processar_serie_mensal(df_imp)
df_exp = processar_serie_mensal(df_exp)
df_imp_pais, col_pais_imp = processar_por_pais(df_imp_pais)
df_exp_pais, col_pais_exp = processar_por_pais(df_exp_pais)


# ============================================================
# ESTATÍSTICAS
# ============================================================

def resumir(df, rotulo):
    """Imprime um bloco de estatísticas para uma das séries."""
    if df.empty:
        print(f"\n  {rotulo}: sem dados no período")
        return

    # Totais
    total_fob = df["metricFOB"].sum()
    total_kg  = df["metricKG"].sum()
    media_fob = df["metricFOB"].mean()

    # Preço médio ponderado pelo volume (não é a média simples dos preços mensais)
    preco_medio = (total_fob / total_kg) * 1000

    # Volatilidade do preço: desvio padrão dividido pela média (coef. de variação)
    vol_preco = df["preco_usd_ton"].std() / df["preco_usd_ton"].mean() * 100

    # Variação ano sobre ano usando os dois últimos anos completos
    df["ano"] = df["data"].dt.year
    anos_completos = df.groupby("ano").size()
    anos_validos = anos_completos[anos_completos == 12].index.tolist()

    if len(anos_validos) >= 2:
        a1, a0 = anos_validos[-1], anos_validos[-2]
        fob_a1 = df.loc[df["ano"] == a1, "metricFOB"].sum()
        fob_a0 = df.loc[df["ano"] == a0, "metricFOB"].sum()
        yoy = (fob_a1 / fob_a0 - 1) * 100
        rotulo_yoy = f"{a1} vs {a0}"
    else:
        yoy = None
        rotulo_yoy = ""

    print(f"\n  ===== {rotulo} =====")
    print(f"  Total FOB:              US$ {total_fob:>18,.0f}")
    print(f"  Volume total:           {total_kg/1_000_000:>18,.1f} mil ton")
    print(f"  Média mensal FOB:       US$ {media_fob:>18,.0f}")
    print(f"  Preço médio implícito:  US$ {preco_medio:>18,.2f} / ton")
    print(f"  Volatilidade do preço:  {vol_preco:>22,.1f} %")
    if yoy is not None:
        print(f"  YoY ({rotulo_yoy}):     {yoy:>+18,.1f} %")


resumir(df_imp, "IMPORTAÇÃO")
resumir(df_exp, "EXPORTAÇÃO")


# ============================================================
# GERAÇÃO DOS GRÁFICOS (dashboard com 6 painéis)
# ============================================================

plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
})

# Cria a figura com grade 3x2
fig, axes = plt.subplots(3, 2, figsize=(16, 14))

# Título geral do dashboard
fig.suptitle(
    f"Comércio Exterior Brasileiro | {NOME_PRODUTO} | {ANO_INICIAL} a {ANO_FINAL}\n"
    f"NCM: {', '.join(NCM_CODES)}     Fonte: ComexStat / SECEX / MDIC",
    fontsize=13, fontweight="bold"
)

COR_IMP = "#dc2626"  # vermelho para importação
COR_EXP = "#16a34a"  # verde para exportação


# ---- Gráfico 1: Valor FOB mensal ----
ax = axes[0, 0]
if not df_imp.empty:
    ax.plot(df_imp["data"], df_imp["metricFOB"] / 1e6, label="Importação", color=COR_IMP, lw=1.5)
if not df_exp.empty:
    ax.plot(df_exp["data"], df_exp["metricFOB"] / 1e6, label="Exportação", color=COR_EXP, lw=1.5)
ax.set_title("Valor FOB Mensal", fontweight="bold")
ax.set_ylabel("US$ Milhões")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend()


# ---- Gráfico 2: Volume mensal ----
ax = axes[0, 1]
if not df_imp.empty:
    ax.plot(df_imp["data"], df_imp["metricKG"] / 1e6, label="Importação", color=COR_IMP, lw=1.5)
if not df_exp.empty:
    ax.plot(df_exp["data"], df_exp["metricKG"] / 1e6, label="Exportação", color=COR_EXP, lw=1.5)
ax.set_title("Volume Mensal", fontweight="bold")
ax.set_ylabel("Mil Toneladas")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend()


# ---- Gráfico 3: Preço implícito (FOB por tonelada) ----
ax = axes[1, 0]
if not df_imp.empty:
    ax.plot(df_imp["data"], df_imp["preco_usd_ton"], label="Importação", color=COR_IMP, lw=1.5)
if not df_exp.empty:
    ax.plot(df_exp["data"], df_exp["preco_usd_ton"], label="Exportação", color=COR_EXP, lw=1.5)
ax.set_title("Preço Médio Implícito (FOB / Volume)", fontweight="bold")
ax.set_ylabel("US$ por tonelada")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend()


# ---- Gráfico 4: Balança comercial (exportação menos importação) ----
ax = axes[1, 1]
if not df_imp.empty and not df_exp.empty:
    # Faz merge das duas séries pelo mês
    balanca = df_exp[["data", "metricFOB"]].merge(
        df_imp[["data", "metricFOB"]],
        on="data", suffixes=("_exp", "_imp"), how="outer"
    ).fillna(0)
    balanca["saldo"] = balanca["metricFOB_exp"] - balanca["metricFOB_imp"]
    # Colore positivo de verde e negativo de vermelho
    cores = [COR_EXP if v >= 0 else COR_IMP for v in balanca["saldo"]]
    ax.bar(balanca["data"], balanca["saldo"] / 1e6, color=cores, width=25)
    ax.axhline(0, color="black", lw=0.5)
ax.set_title("Saldo Comercial (Exportação menos Importação)", fontweight="bold")
ax.set_ylabel("US$ Milhões")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))


# ---- Gráfico 5: Top 10 origens das importações ----
ax = axes[2, 0]
if not df_imp_pais.empty and col_pais_imp is not None:
    top_imp = df_imp_pais.nlargest(10, "metricFOB").iloc[::-1]
    ax.barh(top_imp[col_pais_imp], top_imp["metricFOB"] / 1e6, color=COR_IMP)
ax.set_title("Top 10 Origens das Importações", fontweight="bold")
ax.set_xlabel("US$ Milhões (acumulado no período)")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))


# ---- Gráfico 6: Top 10 destinos das exportações ----
ax = axes[2, 1]
if not df_exp_pais.empty and col_pais_exp is not None:
    top_exp = df_exp_pais.nlargest(10, "metricFOB").iloc[::-1]
    ax.barh(top_exp[col_pais_exp], top_exp["metricFOB"] / 1e6, color=COR_EXP)
ax.set_title("Top 10 Destinos das Exportações", fontweight="bold")
ax.set_xlabel("US$ Milhões (acumulado no período)")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))


# Ajusta margens e salva
plt.tight_layout()
plt.savefig("comexstat_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n  Dashboard salvo como 'comexstat_dashboard.png'\n")
