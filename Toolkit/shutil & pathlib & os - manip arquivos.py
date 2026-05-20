"""
pathlib_basico.py
Navegação, criação, movimentação e remoção de arquivos e pastas.
Prefira pathlib ao módulo os, é mais limpo e portável.
"""

from pathlib import Path
import shutil
import os


# ============================================================
# Criar Path e inspecionar
# ============================================================

def exemplos_path():
    """
    Operações básicas com Path.
    """
    p = Path('dados/relatorio.pdf')

    # Inspecionar
    p.exists()           # True se existe no disco
    p.is_file()          # True se é arquivo
    p.is_dir()           # True se é pasta
    p.name               # 'relatorio.pdf'
    p.stem               # 'relatorio' (nome sem extensão)
    p.suffix             # '.pdf'
    p.suffixes           # ['.pdf'] (lista, útil para .tar.gz)
    p.parent             # Path('dados')
    p.parents[0]         # pasta pai imediata
    p.parts              # ('dados', 'relatorio.pdf')

    # Caminhos
    p.absolute()         # caminho completo a partir da raiz
    p.resolve()          # caminho absoluto resolvendo links simbólicos

    # Combinar caminhos (operador /)
    base = Path('C:/projetos') if os.name == 'nt' else Path('/projetos')
    arquivo = base / 'dados' / 'arquivo.csv'

    return arquivo


# ============================================================
# Criar pastas e arquivos
# ============================================================

def criar_pasta(caminho, com_pais=True):
    """
    Cria pasta. com_pais=True cria todas as pastas intermediárias.
    exist_ok=True não reclama se já existir.

    Exemplo:
        criar_pasta('dados/brutos/2025')
    """
    Path(caminho).mkdir(parents=com_pais, exist_ok=True)


def criar_arquivo_vazio(caminho):
    """
    Cria arquivo vazio (equivale ao 'touch' no Linux).
    """
    Path(caminho).touch()


def garantir_diretorio_existe(caminho_arquivo):
    """
    Garante que a pasta onde o arquivo vai ser salvo existe.
    Use antes de escrever arquivos em pastas que podem não existir.

    Exemplo:
        garantir_diretorio_existe('output/2025/resumo.csv')
    """
    Path(caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)


# ============================================================
# Listar conteudo
# ============================================================

def listar_arquivos(pasta, padrao='*'):
    """
    Lista arquivos diretamente dentro da pasta (não entra em subpastas).

    Exemplo:
        listar_arquivos('dados/', '*.csv')
    """
    return sorted([p for p in Path(pasta).glob(padrao) if p.is_file()])


def listar_arquivos_recursivo(pasta, padrao='*'):
    """
    Lista arquivos em pasta e subpastas. Use rglob.

    Exemplo:
        listar_arquivos_recursivo('projeto/', '*.py')
    """
    return sorted([p for p in Path(pasta).rglob(padrao) if p.is_file()])


def listar_pastas(pasta):
    """Lista apenas subpastas, ignorando arquivos."""
    return sorted([p for p in Path(pasta).iterdir() if p.is_dir()])


def percorrer_arvore(pasta):
    """
    Gera tupla (pasta, subpastas, arquivos) para cada nível.
    Equivale ao os.walk mas com Path.

    Exemplo:
        for pasta_atual, subs, arqs in percorrer_arvore('./projeto'):
            print(pasta_atual, len(arqs))
    """
    for raiz, dirs, arqs in os.walk(pasta):
        yield Path(raiz), [Path(raiz) / d for d in dirs], [Path(raiz) / a for a in arqs]


# ============================================================
# Copiar, mover, deletar
# ============================================================

def copiar_arquivo(origem, destino):
    """
    Copia arquivo preservando metadados.
    Se destino for pasta, copia mantendo nome original.
    """
    return shutil.copy2(origem, destino)


def copiar_pasta(origem, destino):
    """Copia pasta inteira com todo o conteúdo."""
    return shutil.copytree(origem, destino, dirs_exist_ok=True)


def mover(origem, destino):
    """Move ou renomeia arquivo ou pasta."""
    return shutil.move(str(origem), str(destino))


def renomear(caminho, novo_nome):
    """
    Renomeia mantendo na mesma pasta.

    Exemplo:
        renomear('dados.csv', 'dados_2025.csv')
    """
    p = Path(caminho)
    return p.rename(p.parent / novo_nome)


def deletar_arquivo(caminho, silencioso=True):
    """
    Remove arquivo. silencioso=True não reclama se não existir.
    """
    p = Path(caminho)
    if p.exists():
        p.unlink()
    elif not silencioso:
        raise FileNotFoundError(caminho)


def deletar_pasta(caminho):
    """
    Remove pasta e TODO o conteúdo. Cuidado, não tem volta.
    """
    shutil.rmtree(caminho)


# ============================================================
# Metadados de arquivo
# ============================================================

def info_arquivo(caminho):
    """
    Retorna dict com tamanho, datas de modificação e criação.
    """
    p = Path(caminho)
    stat = p.stat()
    from datetime import datetime
    return {
        'tamanho_bytes': stat.st_size,
        'tamanho_kb': stat.st_size / 1024,
        'tamanho_mb': stat.st_size / 1024 / 1024,
        'modificado_em': datetime.fromtimestamp(stat.st_mtime),
        'criado_em': datetime.fromtimestamp(stat.st_ctime),
        'acessado_em': datetime.fromtimestamp(stat.st_atime)
    }


def tamanho_pasta(caminho):
    """Soma o tamanho de todos os arquivos dentro de uma pasta."""
    return sum(f.stat().st_size for f in Path(caminho).rglob('*') if f.is_file())


# ============================================================
# Caminhos relativos e absolutos
# ============================================================

def caminho_relativo(caminho, base):
    """
    Retorna caminho relativo a uma pasta base.

    Exemplo:
        caminho_relativo('/projeto/dados/x.csv', '/projeto')  # 'dados/x.csv'
    """
    return Path(caminho).relative_to(base)


def pasta_atual():
    """Pasta de onde o script está rodando."""
    return Path.cwd()


def pasta_do_script():
    """
    Pasta onde o script está salvo. Use __file__.

    Uso dentro de um script:
        PASTA = Path(__file__).parent
    """
    return Path(__file__).parent


def pasta_home():
    """Pasta home do usuário."""
    return Path.home()


if __name__ == '__main__':
    # Teste rápido
    print('Pasta atual:', pasta_atual())
    print('Arquivos Python aqui:', listar_arquivos('.', '*.py'))
