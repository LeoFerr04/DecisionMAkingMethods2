from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Rota inicial: Renderiza a página HTML principal.
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cálculo de pontuações (API endpoint)
@app.route('/calculate', methods=['POST'])
def calculate():
   
    # Carrega os dados JSON enviados pelo cliente
    data = request.json
    
    # Cria um DataFrame Pandas a partir dos dados
    df = pd.DataFrame(data)

    # Dicionário para armazenar as pontuações das alternativas
    alternative_scores = {}
    num_alternatives = len(df['alternatives'][0])  # Número de alternativas fornecidas

    # Calcula as pontuações ponderadas para cada alternativa
    for alt_index in range(num_alternatives):
        
        # Valida se os pesos são todos iguais a zero, o que inviabilizaria o cálculo
        if df['weight'].sum() == 0:
            return jsonify({"error": "Weight values cannot all be zero."}), 400
        
        # Cálculo da pontuação ponderada
        alternative_scores[f'Alternative_{alt_index + 1}'] = int(
            (df['weight'] * df['alternatives'].apply(lambda alts: alts[alt_index])).sum()
        )

    # Prepara os valores para o gráfico de barras
    x_bar = list(alternative_scores.keys())  # Nomes das alternativas
    y_bar = list(alternative_scores.values())  # Pontuações das alternativas

    # Configuração do gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(x_bar, y_bar, width=0.5, edgecolor="white", linewidth=0.7)

    # Ajuste dinâmico dos limites com base nas pontuações
    ax.set_ylim(0, max(y_bar) * 1.1)
    ax.set_xlabel("Alternatives")  # Rótulo do eixo X
    ax.set_ylabel("Scores")  # Rótulo do eixo Y
    ax.set_title("Alternative Scores")  # Título do gráfico

    # Prepara os dados para o gráfico redondo
    weights = df['weight'].tolist()  # Pesos dos parâmetros
    parameter_names = df['parameter'].tolist()  # Nomes dos parâmetros

    # Criação do gráfico redondo
    fig, ax_pie = plt.subplots()
    ax_pie.pie(weights, labels=parameter_names, 
           autopct='%1.1f%%', startangle=90,
           wedgeprops={"linewidth": 1, "edgecolor": "white"})

    # Retorna o dicionário de pontuações como resposta JSON
    return jsonify(alternative_scores)

# Inicialização do servidor
if __name__ == '__main__':
    app.run(debug=True)
