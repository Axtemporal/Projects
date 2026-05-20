"""
zip_tar.py
Compactação e extração de arquivos ZIP e TAR.
"""

import zipfile
import tarfile
from pathlib import Path


# ============================================================
# ZIP
# ============================================================

def listar_conteudo_zip(caminho):
    """
    Lista nomes dos arquivos dentro de um ZIP sem extrair.

    Exemplo:
        nomes = listar_conteudo_zip('dados.zip')
    """
    with zipfile.ZipFile(caminho, 'r') as z:
        return z.namelist()


def extrair_zip(caminho_zip, pasta_destino='.'):
    """
    Extrai todos os arquivos de um ZIP.

    Exemplo:
        extrair_zip('dados.zip', './extraido/')
    """
    Path(pasta_destino).mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        z.extractall(pasta_destino)


def extrair_um_arquivo_do_zip(caminho_zip, nome_arquivo, pasta_destino='.'):
    """
    Extrai apenas um arquivo específico de dentro do ZIP.

    Exemplo:
        extrair_um_arquivo_do_zip('pacote.zip', 'dados/x.csv', './tmp/')
    """
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        z.extract(nome_arquivo, pasta_destino)


def ler_arquivo_do_zip(caminho_zip, nome_arquivo, encoding='utf-8'):
    """
    Lê conteúdo de texto de um arquivo dentro do ZIP sem extrair.

    Exemplo:
        texto = ler_arquivo_do_zip('dados.zip', 'relatorio.txt')
    """
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        with z.open(nome_arquivo) as f:
            return f.read().decode(encoding)


def criar_zip(caminho_zip, arquivos, pasta_base=None):
    """
    Cria ZIP a partir de lista de arquivos.
    Se pasta_base for dada, os caminhos no ZIP ficam relativos a ela.

    Exemplo:
        criar_zip('saida.zip', ['a.csv', 'b.csv', 'relatorio.pdf'])
    """
    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for arq in arquivos:
            p = Path(arq)
            nome_no_zip = p.relative_to(pasta_base) if pasta_base else p.name
            z.write(p, nome_no_zip)


def zipar_pasta(pasta, caminho_zip):
    """
    Compacta pasta inteira preservando estrutura.

    Exemplo:
        zipar_pasta('./resultados/', 'resultados.zip')
    """
    pasta = Path(pasta)
    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for arq in pasta.rglob('*'):
            if arq.is_file():
                z.write(arq, arq.relative_to(pasta.parent))


def tamanho_antes_depois(caminho_zip):
    """
    Compara tamanho original vs comprimido dentro do ZIP.
    Útil para ver taxa de compressão.
    """
    with zipfile.ZipFile(caminho_zip, 'r') as z:
        originais = sum(i.file_size for i in z.infolist())
        comprimidos = sum(i.compress_size for i in z.infolist())
    return {
        'tamanho_original_mb': originais / 1024 / 1024,
        'tamanho_comprimido_mb': comprimidos / 1024 / 1024,
        'taxa_compressao': 1 - (comprimidos / originais) if originais else 0
    }


if __name__ == '__main__':
    # Teste rápido
    from pathlib import Path
    Path('/tmp/teste_zip').mkdir(exist_ok=True)
    Path('/tmp/teste_zip/a.txt').write_text('hello')
    Path('/tmp/teste_zip/b.txt').write_text('world')
    zipar_pasta('/tmp/teste_zip', '/tmp/teste.zip')
    print(listar_conteudo_zip('/tmp/teste.zip'))
