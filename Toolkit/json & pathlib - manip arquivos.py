"""
ler_escrever.py
Leitura e escrita de arquivos de texto, JSON
Sempre use 'with' para garantir fechamento do arquivo.
"""

import json
from pathlib import Path


# ============================================================
# Texto puro
# ============================================================

def ler_texto(caminho, encoding='utf-8'):
    """
    Lê arquivo inteiro como string única.

    Exemplo:
        texto = ler_texto('relatorio.txt')
    """
    with open(caminho, 'r', encoding=encoding) as f:
        return f.read()


def ler_linhas(caminho, encoding='utf-8', remover_quebra=True):
    """
    Lê arquivo como lista de linhas.

    Exemplo:
        linhas = ler_linhas('dados.txt')
    """
    with open(caminho, 'r', encoding=encoding) as f:
        linhas = f.readlines()
    if remover_quebra:
        linhas = [l.rstrip('\n\r') for l in linhas]
    return linhas


def ler_linhas_lazy(caminho, encoding='utf-8'):
    """
    Gerador que lê uma linha por vez. Use para arquivos grandes
    que não cabem na memória.

    Exemplo:
        for linha in ler_linhas_lazy('arquivo_gigante.txt'):
            processar(linha)
    """
    with open(caminho, 'r', encoding=encoding) as f:
        for linha in f:
            yield linha.rstrip('\n\r')


def escrever_texto(caminho, conteudo, encoding='utf-8'):
    """
    Escreve string em arquivo. Sobrescreve se existir.
    """
    with open(caminho, 'w', encoding=encoding) as f:
        f.write(conteudo)


def escrever_linhas(caminho, linhas, encoding='utf-8'):
    """
    Escreve lista de strings, uma por linha.

    Exemplo:
        escrever_linhas('saida.txt', ['linha1', 'linha2', 'linha3'])
    """
    with open(caminho, 'w', encoding=encoding) as f:
        f.write('\n'.join(str(l) for l in linhas))


def anexar_texto(caminho, conteudo, encoding='utf-8'):
    """
    Adiciona conteúdo ao final do arquivo sem apagar o que já tem.
    Modo 'a' (append).
    """
    with open(caminho, 'a', encoding=encoding) as f:
        f.write(conteudo)


# ============================================================
# JSON
# ============================================================

def ler_json(caminho, encoding='utf-8'):
    """
    Lê arquivo JSON e retorna dict ou list.

    Exemplo:
        dados = ler_json('config.json')
    """
    with open(caminho, 'r', encoding=encoding) as f:
        return json.load(f)


def escrever_json(caminho, dados, indent=2, encoding='utf-8'):
    """
    Escreve dict ou list em JSON. indent=2 deixa bonito.
    ensure_ascii=False preserva acentos.

    Exemplo:
        escrever_json('config.json', {'nome': 'São Paulo', 'ano': 2025})
    """
    with open(caminho, 'w', encoding=encoding) as f:
        json.dump(dados, f, indent=indent, ensure_ascii=False, default=str)


def escrever_jsonlines(caminho, registros, encoding='utf-8'):
    """
    Escreve formato JSON Lines (um JSON por linha).
    Útil para streaming de dados.

    Exemplo:
        escrever_jsonlines('logs.jsonl', [{'a': 1}, {'a': 2}])
    """
    with open(caminho, 'w', encoding=encoding) as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + '\n')


def ler_jsonlines(caminho, encoding='utf-8'):
    """
    Lê arquivo JSON Lines.
    """
    with open(caminho, 'r', encoding=encoding) as f:
        return [json.loads(linha) for linha in f if linha.strip()]



