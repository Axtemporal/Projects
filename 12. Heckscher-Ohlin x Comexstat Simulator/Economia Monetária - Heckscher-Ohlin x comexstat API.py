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
import numpy as np
import time


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

    resposta = requests.post(
        API_URL,
        json=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        timeout=180
    )
    resposta.raise_for_status()

    registros = resposta.json().get("data", {}).get("list", [])
    return pd.DataFrame(registros)


# ============================================================
# BUSCA OS DADOS
# ============================================================

print(f"\n  Buscando dados da ComexStat")
print(f"  Produto: {NOME_PRODUTO} | NCM: {NCM_CODES}")
print(f"  Período: {ANO_INICIAL} a {ANO_FINAL}\n")

df_imp      = buscar_dados("import", [],          NCM_CODES, ANO_INICIAL, ANO_FINAL, month_detail=True)
df_exp      = buscar_dados("export", [],          NCM_CODES, ANO_INICIAL, ANO_FINAL, month_detail=True)
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
    df["metricFOB"] = pd.to_numeric(df["metricFOB"], errors="coerce")
    df["metricKG"]  = pd.to_numeric(df["metricKG"],  errors="coerce")
    df["data"] = pd.to_datetime(
        df["year"].astype(str) + "-" +
        df["monthNumber"].astype(str).str.zfill(2) + "-01"
    )
    df = df.groupby("data", as_index=False).agg({"metricFOB": "sum", "metricKG": "sum"})
    df = df.sort_values("data").reset_index(drop=True)
    df["preco_usd_ton"] = (df["metricFOB"] / df["metricKG"]) * 1000
    return df


def processar_por_pais(df):
    """Limpa e encontra a coluna de nome de país."""
    if df.empty:
        return df, None
    df["metricFOB"] = pd.to_numeric(df["metricFOB"], errors="coerce")
    df["metricKG"]  = pd.to_numeric(df["metricKG"],  errors="coerce")
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

    total_fob   = df["metricFOB"].sum()
    total_kg    = df["metricKG"].sum()
    media_fob   = df["metricFOB"].mean()
    preco_medio = (total_fob / total_kg) * 1000
    vol_preco   = df["preco_usd_ton"].std() / df["preco_usd_ton"].mean() * 100

    df["ano"] = df["data"].dt.year
    anos_completos = df.groupby("ano").size()
    anos_validos   = anos_completos[anos_completos == 12].index.tolist()

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

fig, axes = plt.subplots(3, 2, figsize=(16, 14))
fig.suptitle(
    f"Comércio Exterior Brasileiro | {NOME_PRODUTO} | {ANO_INICIAL} a {ANO_FINAL}\n"
    f"NCM: {', '.join(NCM_CODES)}     Fonte: ComexStat / SECEX / MDIC",
    fontsize=13, fontweight="bold"
)

COR_IMP = "#dc2626"
COR_EXP = "#16a34a"

ax = axes[0, 0]
if not df_imp.empty:
    ax.plot(df_imp["data"], df_imp["metricFOB"] / 1e6, label="Importação", color=COR_IMP, lw=1.5)
if not df_exp.empty:
    ax.plot(df_exp["data"], df_exp["metricFOB"] / 1e6, label="Exportação", color=COR_EXP, lw=1.5)
ax.set_title("Valor FOB Mensal", fontweight="bold")
ax.set_ylabel("US$ Milhões")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend()

ax = axes[0, 1]
if not df_imp.empty:
    ax.plot(df_imp["data"], df_imp["metricKG"] / 1e6, label="Importação", color=COR_IMP, lw=1.5)
if not df_exp.empty:
    ax.plot(df_exp["data"], df_exp["metricKG"] / 1e6, label="Exportação", color=COR_EXP, lw=1.5)
ax.set_title("Volume Mensal", fontweight="bold")
ax.set_ylabel("Mil Toneladas")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend()

ax = axes[1, 0]
if not df_imp.empty:
    ax.plot(df_imp["data"], df_imp["preco_usd_ton"], label="Importação", color=COR_IMP, lw=1.5)
if not df_exp.empty:
    ax.plot(df_exp["data"], df_exp["preco_usd_ton"], label="Exportação", color=COR_EXP, lw=1.5)
ax.set_title("Preço Médio Implícito (FOB / Volume)", fontweight="bold")
ax.set_ylabel("US$ por tonelada")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.legend()

ax = axes[1, 1]
if not df_imp.empty and not df_exp.empty:
    balanca = df_exp[["data", "metricFOB"]].merge(
        df_imp[["data", "metricFOB"]],
        on="data", suffixes=("_exp", "_imp"), how="outer"
    ).fillna(0)
    balanca["saldo"] = balanca["metricFOB_exp"] - balanca["metricFOB_imp"]
    cores = [COR_EXP if v >= 0 else COR_IMP for v in balanca["saldo"]]
    ax.bar(balanca["data"], balanca["saldo"] / 1e6, color=cores, width=25)
    ax.axhline(0, color="black", lw=0.5)
ax.set_title("Saldo Comercial (Exportação menos Importação)", fontweight="bold")
ax.set_ylabel("US$ Milhões")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))

ax = axes[2, 0]
if not df_imp_pais.empty and col_pais_imp is not None:
    top_imp = df_imp_pais.nlargest(10, "metricFOB").iloc[::-1]
    ax.barh(top_imp[col_pais_imp], top_imp["metricFOB"] / 1e6, color=COR_IMP)
ax.set_title("Top 10 Origens das Importações", fontweight="bold")
ax.set_xlabel("US$ Milhões (acumulado no período)")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))

ax = axes[2, 1]
if not df_exp_pais.empty and col_pais_exp is not None:
    top_exp = df_exp_pais.nlargest(10, "metricFOB").iloc[::-1]
    ax.barh(top_exp[col_pais_exp], top_exp["metricFOB"] / 1e6, color=COR_EXP)
ax.set_title("Top 10 Destinos das Exportações", fontweight="bold")
ax.set_xlabel("US$ Milhões (acumulado no período)")
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))

plt.tight_layout()
plt.savefig("comexstat_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n  Dashboard salvo como 'comexstat_dashboard.png'\n")


# ============================================================
# PARTE 2 – ANÁLISE BILATERAL POR INTENSIDADE DE FATOR
# Comparação entre dois parceiros comerciais do Brasil
#
# Base teórica: Heckscher-Ohlin — países exportam o bem que usa
# intensivamente o fator que possuem em abundância relativa.
#
# Classificação dos capítulos NCM:
#   Capital   → química, metais, máquinas, eletroeletrônicos, transporte,
#               instrumentos de precisão  (caps. 28-40, 72-93)
#   Trabalho  → agropecuária, alimentos, têxteis, vestuário, calçados,
#               madeira/papel, móveis, brinquedos  (caps. 1-24, 44-67, 94-96)
#   Outros    → minerais, combustíveis, couro, pedras, arte, etc.
#
# Referências: Lall (2000), UNCTAD TRAINS, Krugman & Obstfeld (2018)
# ============================================================

# ============================================================
# CONFIGURAÇÃO BILATERAL  ← mexa aqui
# ============================================================

# Código numérico do sistema MDIC/SECEX (diferente do ISO 3166)
# Exemplos comuns:
#   China:            160   |  Estados Unidos: 249
#   Alemanha:         158   |  Argentina:       63
#   Japão:            398   |  Países Baixos:  187
#   Coreia do Sul:    410   |  Índia:          699
#   México:           764   |  Chile:          119
# Dica: chame listar_paises_e_codigos() para ver os códigos
#       presentes nos dados de exportação já baixados nesta sessão.
PAIS_A = {"codigo": "160", "nome": "China"}
PAIS_B = {"codigo": "249", "nome": "Estados Unidos"}

ANO_INI_BIL = ANO_INICIAL
ANO_FIM_BIL = ANO_FINAL

# True  → restringe a análise aos NCMs definidos em NCM_CODES (topo)
# False → abrange TODA a pauta comercial com cada país (recomendado)
FILTRAR_NCM_BILATERAL = False


# ============================================================
# TABELA DE CLASSIFICAÇÃO NCM → INTENSIDADE DE FATOR
# ============================================================

CAPS_CAPITAL = frozenset({
    28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,  # Química inorgânica / orgânica
    39, 40,                                         # Plásticos e borracha
    72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83,   # Metais e manufaturados metálicos
    84, 85,                                         # Máquinas, caldeiras, eletroeletrônicos
    86, 87, 88, 89,                                 # Veículos, aeronaves, embarcações
    90, 91, 92, 93,                                 # Instrumentos de precisão e armamentos
})

CAPS_TRABALHO = frozenset({
     1,  2,  3,  4,  5,  6,  7,  8,  9, 10,       # Animais vivos e produtos animais
    11, 12, 13, 14,                                  # Produtos vegetais
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24,         # Gorduras, alimentos processados, fumo
    44, 45, 46, 47, 48, 49,                          # Madeira, cortiça, pasta de papel
    50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,     # Fibras têxteis e tecidos
    61, 62, 63,                                      # Vestuário e confecções
    64, 65, 66, 67,                                  # Calçados, chapéus, guarda-chuvas
    94, 95, 96,                                      # Móveis, brinquedos, manufaturas diversas
})

COR_A       = "#1d4ed8"
COR_B       = "#f59e0b"
COR_CAPITAL = "#7c3aed"
COR_TRAB    = "#059669"
COR_OUTROS  = "#9ca3af"


# ============================================================
# UTILITÁRIOS
# ============================================================

def listar_paises_e_codigos():
    """Mostra países e códigos nos dados de exportação já baixados."""
    for df, rotulo in [(df_exp_pais, "exportação"), (df_imp_pais, "importação")]:
        if df.empty:
            continue
        col_nome = next((c for c in ["noPaisPor", "country", "noPais", "Country"] if c in df.columns), None)
        col_cod  = next((c for c in ["coCountry", "coIso", "codPais", "coPais", "coId"] if c in df.columns), None)
        if col_nome is None:
            continue
        cols = [col_nome] + ([col_cod] if col_cod else [])
        print(f"\n  Países nos dados de {rotulo} ({NOME_PRODUTO}):")
        print(df[cols].drop_duplicates().sort_values(col_nome).to_string(index=False))
        break


# ============================================================
# FUNÇÕES DE ACESSO À API (bilateral)
# ============================================================

def _post_api_bilateral(body, _pausa=3):
    """POST à API com retry automático em caso de 429 (rate limit)."""
    espera = 10
    for tentativa in range(5):
        time.sleep(_pausa)
        r = requests.post(
            API_URL, json=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=180,
        )
        if r.status_code == 429:
            print(f"\n    [rate limit] aguardando {espera}s antes de tentar novamente…", end="", flush=True)
            time.sleep(espera)
            espera *= 2   # backoff exponencial: 10 → 20 → 40 → 80s
            continue
        r.raise_for_status()
        return pd.DataFrame(r.json().get("data", {}).get("list", []))
    r.raise_for_status()


def buscar_bilateral_ncm(flow, pais_cod, ano_ini, ano_fim):
    """Composição por NCM com um país, sem detalhe mensal."""
    filtros = [{"filter": "country", "values": [pais_cod]}]
    if FILTRAR_NCM_BILATERAL:
        filtros.insert(0, {"filter": "ncm", "values": NCM_CODES})
    return _post_api_bilateral({
        "flow": flow,
        "monthDetail": False,
        "period": {"from": f"{ano_ini}-01", "to": f"{ano_fim}-12"},
        "filters": filtros,
        "details": ["ncm"],
        "metrics": ["metricFOB", "metricKG"],
    })


def buscar_bilateral_mensal(flow, pais_cod, ano_ini, ano_fim):
    """Série mensal total com um país, sem detalhe por NCM."""
    filtros = [{"filter": "country", "values": [pais_cod]}]
    if FILTRAR_NCM_BILATERAL:
        filtros.insert(0, {"filter": "ncm", "values": NCM_CODES})
    return _post_api_bilateral({
        "flow": flow,
        "monthDetail": True,
        "period": {"from": f"{ano_ini}-01", "to": f"{ano_fim}-12"},
        "filters": filtros,
        "details": [],
        "metrics": ["metricFOB", "metricKG"],
    })


def classificar_fator(df):
    """Adiciona coluna 'fator' (Capital / Trabalho / Outros) com base no capítulo NCM."""
    df = df.copy()
    df["metricFOB"] = pd.to_numeric(df["metricFOB"], errors="coerce").fillna(0)
    df["metricKG"]  = pd.to_numeric(df["metricKG"],  errors="coerce").fillna(0)
    if df.empty:
        return df.assign(fator="Outros")
    col_ncm = next(
        (c for c in ["coNcm", "ncm", "coCodigo", "noNcm", "coSh6"] if c in df.columns),
        None,
    )
    if col_ncm is None:
        return df.assign(fator="Outros")

    def _mapa(code):
        try:
            cap = int(str(code).zfill(8)[:2])
        except (ValueError, TypeError):
            return "Outros"
        if cap in CAPS_CAPITAL:
            return "Capital"
        if cap in CAPS_TRABALHO:
            return "Trabalho"
        return "Outros"

    df["fator"] = df[col_ncm].apply(_mapa)
    return df


def agregar_fator(df):
    """Retorna Series indexada por ['Capital','Trabalho','Outros'] com FOB total."""
    cats = ["Capital", "Trabalho", "Outros"]
    if df.empty or "fator" not in df.columns:
        return pd.Series({c: 0.0 for c in cats})
    return df.groupby("fator")["metricFOB"].sum().reindex(cats, fill_value=0)


# ============================================================
# COLETA DOS DADOS BILATERAIS  (8 requisições)
# ============================================================

print(f"\n  {'='*56}")
print(f"  ANÁLISE BILATERAL  |  {PAIS_A['nome']} × {PAIS_B['nome']}")
print(f"  Período: {ANO_INI_BIL}–{ANO_FIM_BIL}  |  "
      f"{'NCMs selecionados' if FILTRAR_NCM_BILATERAL else 'Toda a pauta comercial'}")
print(f"  {'='*56}\n")

PAISES_BIL = [PAIS_A, PAIS_B]
FLOWS_BIL  = [("import", "imp"), ("export", "exp")]

ncm_bil   = {}
serie_bil = {}

for pais in PAISES_BIL:
    for flow, fk in FLOWS_BIL:
        print(f"  {flow.upper():6s} ← {pais['nome']} … ", end="", flush=True)
        df_n = buscar_bilateral_ncm(flow, pais["codigo"], ANO_INI_BIL, ANO_FIM_BIL)
        df_n = classificar_fator(df_n)
        ncm_bil[(fk, pais["nome"])] = df_n

        df_s = buscar_bilateral_mensal(flow, pais["codigo"], ANO_INI_BIL, ANO_FIM_BIL)
        df_s = processar_serie_mensal(df_s)
        serie_bil[(fk, pais["nome"])] = df_s

        total = df_n["metricFOB"].sum() if not df_n.empty else 0
        print(f"US$ {total/1e9:.2f} bi  ({len(df_n)} NCMs)")


# ============================================================
# ESTATÍSTICAS BILATERAIS + LEITURA HECKSCHER-OHLIN
# ============================================================

print(f"\n  {'─'*56}")
print("   COMPOSIÇÃO POR INTENSIDADE DE FATOR")
print(f"  {'─'*56}")

for pais in PAISES_BIL:
    print(f"\n  ── {pais['nome'].upper()} ──")
    for flow, fk in FLOWS_BIL:
        label = (f"  Importações DO Brasil (origem: {pais['nome']})"
                 if fk == "imp" else
                 f"  Exportações DO Brasil (destino: {pais['nome']})")
        s = agregar_fator(ncm_bil.get((fk, pais["nome"]), pd.DataFrame()))
        total = s.sum()
        print(f"{label}:")
        for cat in ["Capital", "Trabalho", "Outros"]:
            pct = s[cat] / total * 100 if total > 0 else 0
            print(f"    {cat:10s}  US$ {s[cat]/1e9:7.2f} bi  ({pct:5.1f}%)")

print(f"\n  {'─'*56}")
print("   LEITURA HECKSCHER-OHLIN")
print(f"  {'─'*56}")
for pais in PAISES_BIL:
    s_imp = agregar_fator(ncm_bil.get(("imp", pais["nome"]), pd.DataFrame()))
    s_exp = agregar_fator(ncm_bil.get(("exp", pais["nome"]), pd.DataFrame()))
    ti, te = s_imp.sum(), s_exp.sum()
    pci = s_imp["Capital"]  / ti * 100 if ti > 0 else 0
    pti = s_imp["Trabalho"] / ti * 100 if ti > 0 else 0
    pce = s_exp["Capital"]  / te * 100 if te > 0 else 0
    pte = s_exp["Trabalho"] / te * 100 if te > 0 else 0
    dom_imp = "capital" if pci > pti else "trabalho"
    dom_exp = "capital" if pce > pte else "trabalho"
    print(f"\n  {pais['nome']}:")
    print(f"    Brasil IMPORTA bens de {dom_imp} deste parceiro  "
          f"(cap {pci:.0f}% | trab {pti:.0f}%)")
    print(f"    Brasil EXPORTA bens de {dom_exp} para este parceiro  "
          f"(cap {pce:.0f}% | trab {pte:.0f}%)")


# ============================================================
# DASHBOARD BILATERAL  (6 painéis)
# ============================================================

CATS      = ["Capital", "Trabalho", "Outros"]
CORES_CAT = [COR_CAPITAL, COR_TRAB, COR_OUTROS]
x3 = np.arange(3)
x2 = np.arange(2)
W  = 0.38

fig2, axes2 = plt.subplots(3, 2, figsize=(16, 14))
fig2.suptitle(
    f"Comércio Exterior Brasileiro | Análise Bilateral por Intensidade de Fator\n"
    f"{PAIS_A['nome']}  vs  {PAIS_B['nome']}   ·   {ANO_INI_BIL}–{ANO_FIM_BIL}"
    + (f"   ·   NCM: {', '.join(NCM_CODES)}" if FILTRAR_NCM_BILATERAL else "   ·   Toda a pauta"),
    fontsize=12, fontweight="bold",
)

ax = axes2[0, 0]
for i, (pais, cor) in enumerate([(PAIS_A, COR_A), (PAIS_B, COR_B)]):
    s = agregar_fator(ncm_bil.get(("imp", pais["nome"]), pd.DataFrame()))
    ax.bar(x3 + (i - 0.5) * W, s[CATS].values / 1e9, W,
           label=pais["nome"], color=cor, alpha=0.85, edgecolor="white")
ax.set_xticks(x3); ax.set_xticklabels(CATS)
ax.set_title("Importações brasileiras por intensidade de fator", fontweight="bold")
ax.set_ylabel("US$ Bilhões (acumulado no período)")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:.1f}"))
ax.legend()

ax = axes2[0, 1]
for i, (pais, cor) in enumerate([(PAIS_A, COR_A), (PAIS_B, COR_B)]):
    s = agregar_fator(ncm_bil.get(("exp", pais["nome"]), pd.DataFrame()))
    ax.bar(x3 + (i - 0.5) * W, s[CATS].values / 1e9, W,
           label=pais["nome"], color=cor, alpha=0.85, edgecolor="white")
ax.set_xticks(x3); ax.set_xticklabels(CATS)
ax.set_title("Exportações brasileiras por intensidade de fator", fontweight="bold")
ax.set_ylabel("US$ Bilhões (acumulado no período)")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:.1f}"))
ax.legend()

ax = axes2[1, 0]
for pais, cor in [(PAIS_A, COR_A), (PAIS_B, COR_B)]:
    df_s = serie_bil.get(("imp", pais["nome"]), pd.DataFrame())
    if not df_s.empty:
        ax.plot(df_s["data"], df_s["metricFOB"] / 1e6, label=pais["nome"], color=cor, lw=1.5)
ax.set_title("Evolução mensal das Importações bilaterais", fontweight="bold")
ax.set_ylabel("US$ Milhões / mês")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.legend()

ax = axes2[1, 1]
for pais, cor in [(PAIS_A, COR_A), (PAIS_B, COR_B)]:
    df_s = serie_bil.get(("exp", pais["nome"]), pd.DataFrame())
    if not df_s.empty:
        ax.plot(df_s["data"], df_s["metricFOB"] / 1e6, label=pais["nome"], color=cor, lw=1.5)
ax.set_title("Evolução mensal das Exportações bilaterais", fontweight="bold")
ax.set_ylabel("US$ Milhões / mês")
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.legend()

ax = axes2[2, 0]
bottoms = np.zeros(2)
for cat, cor in zip(CATS, CORES_CAT):
    vals = []
    for pais in PAISES_BIL:
        s = agregar_fator(ncm_bil.get(("imp", pais["nome"]), pd.DataFrame()))
        tot = s.sum()
        vals.append(s[cat] / tot * 100 if tot > 0 else 0)
    ax.bar(x2, vals, bottom=bottoms, color=cor, alpha=0.85, edgecolor="white", label=cat)
    for xi, (v, bot) in enumerate(zip(vals, bottoms)):
        if v > 5:
            ax.text(xi, bot + v / 2, f"{v:.0f}%", ha="center", va="center",
                    fontsize=9, color="white", fontweight="bold")
    bottoms += np.array(vals)
ax.set_xticks(x2); ax.set_xticklabels([p["nome"] for p in PAISES_BIL])
ax.set_ylim(0, 100); ax.set_ylabel("%")
ax.set_title("Composição % das Importações por intensidade de fator", fontweight="bold")
ax.legend(loc="upper right", fontsize=8)

ax = axes2[2, 1]
bottoms = np.zeros(2)
for cat, cor in zip(CATS, CORES_CAT):
    vals = []
    for pais in PAISES_BIL:
        s = agregar_fator(ncm_bil.get(("exp", pais["nome"]), pd.DataFrame()))
        tot = s.sum()
        vals.append(s[cat] / tot * 100 if tot > 0 else 0)
    ax.bar(x2, vals, bottom=bottoms, color=cor, alpha=0.85, edgecolor="white", label=cat)
    for xi, (v, bot) in enumerate(zip(vals, bottoms)):
        if v > 5:
            ax.text(xi, bot + v / 2, f"{v:.0f}%", ha="center", va="center",
                    fontsize=9, color="white", fontweight="bold")
    bottoms += np.array(vals)
ax.set_xticks(x2); ax.set_xticklabels([p["nome"] for p in PAISES_BIL])
ax.set_ylim(0, 100); ax.set_ylabel("%")
ax.set_title("Composição % das Exportações por intensidade de fator", fontweight="bold")
ax.legend(loc="upper right", fontsize=8)

plt.tight_layout()
plt.savefig("comexstat_bilateral.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n  Dashboard bilateral salvo como 'comexstat_bilateral.png'\n")