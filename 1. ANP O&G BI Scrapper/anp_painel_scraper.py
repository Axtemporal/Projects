import os
import json
from playwright.sync_api import sync_playwright
import pandas as pd

PAINEL_URL = (
    "https://app.powerbi.com/view?r="
    "eyJrIjoiNzVmNzI1MzQtNTY1NC00ZGVhLTk5N2ItNzBkMDNhY2IxZTIxIiwid"
    "CI6IjQ0OTlmNGZmLTI0YTYtNGI0Mi1iN2VmLTEyNGFmY2FkYzkxMyJ9"
)
HEADLESS = False
TIMEOUT = 60000
OUTPUT_DIR = "anp_dados"


# ============================================================
# PAGINAS DE INTERESSE (textos dos links na pagina inicial)
# Mude essa lista pra escolher quais paginas visitar
# ============================================================
PAGINAS_ALVO = [
    "Total",              # Producao total (graficos e KPIs)
    "Agregada",           # Producao agregada por campo/bacia
    "Tabela Produção",    # Dados em tabela (melhor pra extrair)
]


def esperar(page):
    """Espera Power BI carregar."""
    print("  Aguardando carregar...")
    try:
        page.wait_for_selector(
            ".visualContainerHost, .landingPage, exploration-container",
            timeout=TIMEOUT,
            state="attached",
        )
    except Exception:
        pass
    # Espera spinners
    for _ in range(30):
        s = page.query_selector_all(
            ".displaySpinner, .progressBar, [aria-busy=true]"
        )
        if not s:
            break
        page.wait_for_timeout(1000)
    page.wait_for_timeout(5000)
    print("  Carregado!")


def voltar_inicio(page):
    """Clica no icone de casa pra voltar a pagina inicial."""
    # O icone de casa fica no canto superior direito
    casa = page.query_selector(
        "button[aria-label*='home'], "
        "button[aria-label*='Home'], "
        "button[aria-label*='Início'], "
        "div[title*='Início'], "
        "img[alt*='home']"
    )
    if casa:
        casa.click()
        page.wait_for_timeout(2000)
        esperar(page)
        return True

    # Alternativa: navega pra pagina 1 usando setas
    # Procura o indicador "X de 27" e clica na seta esquerda varias vezes
    seta_esq = page.query_selector(
        "button[aria-label*='Previous'], "
        "button[aria-label*='Anterior'], "
        "button[aria-label*='previous']"
    )
    if seta_esq:
        for _ in range(30):
            seta_esq.click()
            page.wait_for_timeout(300)
        esperar(page)
        return True

    # Ultimo recurso: recarrega a URL
    page.goto(PAINEL_URL, wait_until="networkidle")
    esperar(page)
    return True


def clicar_link(page, texto):
    """
    Clica num link/botao pelo texto visivel.
    Na pagina inicial do painel, os links sao textos clicaveis
    como 'Total', 'Agregada', 'Tabela Producao', etc.
    """
    # Tenta varios seletores pra encontrar o elemento com esse texto
    seletores = [
        f"text='{texto}'",
        f"a:has-text('{texto}')",
        f"span:has-text('{texto}')",
        f"div:has-text('{texto}')",
        f"button:has-text('{texto}')",
        f"p:has-text('{texto}')",
    ]

    for sel in seletores:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click()
                page.wait_for_timeout(3000)
                esperar(page)
                return True
        except Exception:
            continue

    # Fallback: procura por texto parcial em todos os elementos visiveis
    try:
        page.click(f"text={texto}", timeout=5000)
        page.wait_for_timeout(3000)
        esperar(page)
        return True
    except Exception:
        pass

    print(f"  AVISO: nao encontrou link '{texto}'")
    return False


def capturar_tudo(page):
    """
    Captura TODOS os textos visiveis na pagina.
    Mais robusto que procurar seletores especificos do Power BI.
    """
    # Pega todos os elementos de texto visiveis
    seletores_tentar = [
        # Tabelas do Power BI
        "div.cell-interactive",
        "div.pivotTableCellWrap",
        # Cards/KPIs
        "div.card .value, div[class*=kpiValue], div[class*=cardValue]",
        # Titulos
        "div.visual-title span, div.visual-title p",
        # Texto generico dentro de visuais
        ".visualContainerHost text",
        ".visualContainerHost span",
        ".visualContainerHost div[class*='label']",
    ]

    resultados = {}

    for sel in seletores_tentar:
        try:
            els = page.query_selector_all(sel)
            if els and len(els) > 0:
                textos = []
                for el in els:
                    t = el.inner_text().strip()
                    if t and len(t) < 500:
                        textos.append(t)
                if textos:
                    resultados[sel] = textos
        except Exception:
            continue

    return resultados


def scroll_tabela(page, max_scrolls=15):
    """Faz scroll em tabelas virtualizadas."""
    todos = []
    anteriores = set()

    # Procura container de scroll
    container = page.query_selector(
        ".bodyCells, .scrollRegion, .tableEx, "
        "div[class*='scroll'], div[class*='tableBody']"
    )
    if not container:
        return todos

    for n in range(max_scrolls):
        # Captura celulas visiveis
        cells = page.query_selector_all(
            "div.cell-interactive, div.pivotTableCellWrap"
        )
        novos = []
        for c in cells:
            t = c.inner_text().strip()
            if t and t not in anteriores:
                novos.append(t)
                anteriores.add(t)

        if not novos and n > 0:
            print(f"  Scroll {n}: sem novos, parando")
            break

        todos.extend(novos)
        print(f"  Scroll {n}: +{len(novos)} (total: {len(todos)})")

        container.evaluate(
            "el => el.scrollBy({top: 400, behavior: 'smooth'})"
        )
        page.wait_for_timeout(1500)

    return todos


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("")
    print("=" * 60)
    print("  EXTRATOR DO PAINEL DINAMICO ANP")
    print("  Producao de Petroleo e Gas Natural")
    print("=" * 60)

    with sync_playwright() as p:
        # Abre navegador
        print("\n[1/4] Abrindo navegador...")
        browser = p.chromium.launch(headless=HEADLESS)
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="pt-BR",
        )
        page = ctx.new_page()
        page.set_default_timeout(TIMEOUT)

        # Acessa painel
        print("[2/4] Acessando painel da ANP...")
        page.goto(PAINEL_URL, wait_until="networkidle")
        esperar(page)
        page.screenshot(path=os.path.join(OUTPUT_DIR, "00_indice.png"))
        print("  Screenshot: 00_indice.png")

        # Lista links visiveis na pagina inicial
        print("\n  Links encontrados na pagina inicial:")
        links = page.query_selector_all("a, span, div, p, button")
        textos_links = set()
        for lk in links:
            try:
                t = lk.inner_text().strip()
                if t and len(t) < 50 and len(t) > 2:
                    textos_links.add(t)
            except Exception:
                continue
        for t in sorted(textos_links):
            print(f"    - {t}")

        # Navega pelas paginas de interesse
        print(f"\n[3/4] Visitando paginas: {PAGINAS_ALVO}")
        todos_resultados = {}

        for idx, pagina in enumerate(PAGINAS_ALVO):
            print(f"\n{'='*40}")
            print(f"  Navegando para: {pagina}")
            print(f"{'='*40}")

            # Volta pro indice antes de cada navegacao
            if idx > 0:
                voltar_inicio(page)
                page.wait_for_timeout(2000)

            # Clica no link
            ok = clicar_link(page, pagina)
            if not ok:
                print(f"  Pulando '{pagina}'")
                continue

            # Screenshot
            fname = f"{idx+1:02d}_{pagina.replace(' ','_')[:20]}.png"
            page.screenshot(path=os.path.join(OUTPUT_DIR, fname))
            print(f"  Screenshot: {fname}")

            # Captura dados genericos
            dados = capturar_tudo(page)
            if dados:
                for sel, textos in dados.items():
                    chave = f"{pagina}_{sel[:30]}"
                    todos_resultados[chave] = textos
                    print(f"  {sel[:40]}: {len(textos)} itens")

            # Se for pagina de tabela, tenta scroll
            if "Tabela" in pagina or "tabela" in pagina:
                print("  Tentando scroll na tabela...")
                tab_dados = scroll_tabela(page, max_scrolls=15)
                if tab_dados:
                    todos_resultados[f"tabela_scroll_{pagina}"] = tab_dados
                    print(f"  Total com scroll: {len(tab_dados)} itens")

        # Salva resultados
        print(f"\n[4/4] Salvando resultados...")

        # JSON completo
        json_path = os.path.join(OUTPUT_DIR, "dados.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(todos_resultados, f, ensure_ascii=False, indent=2)
        print(f"  {json_path}")

        # CSVs
        for k, v in todos_resultados.items():
            if isinstance(v, list) and v:
                safe_name = (
                    k.replace(" ", "_")
                    .replace("/", "_")
                    .replace(":", "_")
                    .replace(".", "_")[:50]
                )
                csv_path = os.path.join(OUTPUT_DIR, f"{safe_name}.csv")
                df = pd.DataFrame({"valor": v})
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                print(f"  {csv_path}: {len(v)} linhas")

        browser.close()

    print("")
    print("=" * 60)
    print("  CONCLUIDO!")
    print(f"  Resultados em: ./{OUTPUT_DIR}/")
    print("=" * 60)
    print("")


if __name__ == "__main__":
    main()