# ============================================================

# SIMULADOR DE APORTES MENSAIS

# Calcula evolução do patrimônio com juros compostos e inflação

# ============================================================

import matplotlib.pyplot as plt  # gera os gráficos
import matplotlib.ticker as mtick  # formata os eixos do gráfico

# –– PARÂMETROS DA SIMULAÇÃO ––

aporte_mensal    = 1000.00   # valor aportado todo mês (R$)
capital_inicial  = 5000.00   # valor já investido no início
taxa_anual       = 12.0      # taxa de juros anual (%)
inflacao_anual   = 4.5       # inflação anual estimada (%)
anos             = 10        # duração da simulação em anos

# –– CONVERSÃO DE TAXAS ––

# Converte a taxa anual para mensal usando a fórmula exata: (1 + i)^(1/12) - 1

taxa_mensal = (1 + taxa_anual / 100) ** (1 / 12) - 1

# Mesmo processo para a inflação mensal

inflacao_mensal = (1 + inflacao_anual / 100) ** (1 / 12) - 1

# Total de meses simulados

meses = anos * 12

# –– SIMULAÇÃO MÊS A MÊS ––

# Listas para guardar os valores a cada mês (usadas no gráfico)

saldo_nominal   = []   # patrimônio bruto, sem descontar inflação
saldo_real      = []   # patrimônio ajustado pela inflação (poder de compra real)
total_aportado  = []   # soma simples de tudo que foi depositado

# Valores iniciais antes de começar o loop

saldo = capital_inicial

for mes in range(1, meses + 1):


# Aplica os juros do mês sobre o saldo atual
saldo = saldo * (1 + taxa_mensal)

# Adiciona o aporte do mês
saldo += aporte_mensal

# Calcula o total depositado até este mês (sem juros)
depositado = capital_inicial + aporte_mensal * mes

# Deflaciona o saldo nominal para encontrar o valor real
# Divide pelo fator acumulado da inflação até este mês
fator_inflacao = (1 + inflacao_mensal) ** mes
saldo_hoje = saldo / fator_inflacao

# Guarda os três valores na lista correspondente
saldo_nominal.append(saldo)
saldo_real.append(saldo_hoje)
total_aportado.append(depositado)


# –– RESULTADOS FINAIS ––

# Pega os valores do último mês de cada lista

patrimonio_final_nominal = saldo_nominal[-1]
patrimonio_final_real    = saldo_real[-1]
total_depositado         = total_aportado[-1]

# Calcula quanto foram os juros (o que veio além do que você depositou)

juros_gerados = patrimonio_final_nominal - total_depositado

print(”\n========== RESULTADO DA SIMULAÇÃO ==========”)
print(f”  Prazo:                   {anos} anos ({meses} meses)”)
print(f”  Capital inicial:         R$ {capital_inicial:,.2f}”)
print(f”  Aporte mensal:           R$ {aporte_mensal:,.2f}”)
print(f”  Taxa de juros anual:     {taxa_anual}%”)
print(f”  Inflação anual estimada: {inflacao_anual}%”)
print(”———————————————”)
print(f”  Total depositado:        R$ {total_depositado:,.2f}”)
print(f”  Juros gerados:           R$ {juros_gerados:,.2f}”)
print(f”  Patrimônio nominal:      R$ {patrimonio_final_nominal:,.2f}”)
print(f”  Patrimônio real:         R$ {patrimonio_final_real:,.2f}”)
print(”=============================================\n”)

# –– GRÁFICO ––

# Cria o eixo de tempo em anos (divide cada mês pelo 12)

eixo_tempo = [m / 12 for m in range(1, meses + 1)]

# Configura a figura com um único gráfico

fig, ax = plt.subplots(figsize=(12, 6))

# Plota as três linhas

ax.plot(eixo_tempo, saldo_nominal,  label=“Patrimônio Nominal”,      color=”#2563eb”, linewidth=2)
ax.plot(eixo_tempo, saldo_real,     label=“Patrimônio Real”,         color=”#16a34a”, linewidth=2, linestyle=”–”)
ax.plot(eixo_tempo, total_aportado, label=“Total Aportado (sem juros)”, color=”#9ca3af”, linewidth=1.5, linestyle=”:”)

# Preenche a área entre o nominal e o aportado para destacar os juros

ax.fill_between(eixo_tempo, total_aportado, saldo_nominal, alpha=0.08, color=”#2563eb”)

# Formata o eixo Y para mostrar valores em R$

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f”R$ {x:,.0f}”))

# Títulos e labels

ax.set_title(“Simulador de Aportes Mensais”, fontsize=15, fontweight=“bold”, pad=15)
ax.set_xlabel(“Anos”, fontsize=11)
ax.set_ylabel(“Valor (R$)”, fontsize=11)

# Legenda e grid

ax.legend(fontsize=10)
ax.grid(True, linestyle=”–”, alpha=0.4)

# Ajusta as margens e exibe

plt.tight_layout()
plt.savefig(”/mnt/user-data/outputs/simulador_aportes.png”, dpi=150)
plt.show()
print(”  Gráfico salvo como ‘simulador_aportes.png’\n”)