# Modelagem de Volatilidade com Modelos ARCH e GARCH: Uma Aplicação ao Índice S&P 500

Trabalho da disciplina de Econometria II (IBMEC Rio). O projeto simula um processo ARCH(1) para ilustrar a clusterização de volatilidade e estima um modelo GARCH(1,1) sobre os retornos diários do índice S&P 500, com testes de diagnóstico e previsão.

## Visão geral

A análise está organizada em duas partes. A primeira simula um processo ARCH(1) com parâmetros conhecidos para mostrar, em ambiente controlado, como choques afetam a variância condicional ao longo do tempo. A segunda aplica o modelo GARCH(1,1) a uma série real de retornos do S&P 500 no período de 2015 a 2024, estimando os parâmetros por máxima verossimilhança e avaliando a qualidade do ajuste.

## Dados

Preços diários de fechamento do índice S&P 500 entre 2015 e 2024, obtidos via Yahoo Finance (biblioteca `yfinance`), com Stooq e FRED como fontes alternativas caso a principal falhe. São aproximadamente 2.514 observações.

## Métodos aplicados

A análise cobre estatísticas descritivas dos retornos, teste de raiz unitária de Dickey-Fuller Aumentado (ADF) no preço e nos retornos, seleção de especificação por AIC e BIC, estimação do GARCH(1,1) por máxima verossimilhança, diagnóstico por ACF dos resíduos e dos resíduos ao quadrado, gráfico Q-Q, teste de Ljung-Box e previsão da volatilidade condicional.

## Principais resultados

O retorno é estacionário (ADF com p-valor inferior a 0,001) enquanto o preço possui raiz unitária. O GARCH(1,1) foi a especificação de menor BIC. Os parâmetros estimados foram ômega = 0,0397, alfa = 0,1837 e beta = 0,7853, com persistência (alfa mais beta) de 0,969, indicando alta persistência da volatilidade. O teste de Ljung-Box nos resíduos ao quadrado (p-valor 0,7478) não rejeita a ausência de autocorrelação, indicando bom ajuste.

## Como executar

Opção recomendada, no Google Colab: abra o notebook `Econometria_II_SP500_GARCH_Colab.ipynb` e execute todas as células (a internet do Colab já vem liberada).

Localmente, com Python 3.10 ou superior:

```bash
pip install -r requirements.txt
python "Econometria_II_SP500_GARCH.py"
```

## Estrutura do repositório

```
.
├── README.md
├── requirements.txt
├── Econometria_II_SP500_GARCH.py          # script principal
├── Econometria_II_SP500_GARCH_Colab.ipynb # notebook comentado por seção
├── relatorio/                             # relatório final em PDF
└── figuras/                               # gráficos gerados
```

## Autor

Alex Temporal. Econometria II, IBMEC Rio.
