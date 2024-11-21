from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Tabela de taxas
taxas = {
    "VISA": [1.19, 3.46, 4.41, 5.12, 5.84, 6.54, 7.25, 7.94, 8.63, 9.32, 10.01, 10.69, 11.36, 12.04, 12.70, 13.36, 14.01, 14.66, 15.29],
    "MASTER": [1.19, 1.77, 4.63, 5.34, 6.06, 6.76, 7.47, 8.16, 8.84, 9.53, 10.21, 10.89, 11.56, 12.23, 12.89, 13.54, 14.19, 14.83, 15.46],
    "DINERS": [1.19, 1.77, 4.63, 5.34, 6.06, 6.76, 7.47, 8.16, 8.84, 9.53, 10.21, 10.89, 11.56, 12.23, 12.89, 13.54, 14.19, 14.83, 15.46],
    "ELO": [1.88, 2.53, 5.34, 6.05, 6.77, 7.47, 8.17, 8.85, 9.53, 10.20, 10.87, 11.53, 12.18, 12.84, 13.48, 14.13, 14.77, 15.40, 16.02],
    "AMEX": [0.89, 2.57, 5.34, 6.05, 6.77, 7.47, 8.17, 8.85, 9.53, 10.20, 10.87, 11.53, 12.18, 12.84, 13.48, 14.13, 14.77, 15.40, 16.02],
    "HIPER": [0.89, 1.74, 4.80, 5.50, 6.21, 6.91, 7.61, 8.29, 8.96, 9.64, 10.31, 10.97, 11.62, 12.27, 12.91, 13.55, 14.18, 14.81, 15.42],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    valor = float(dados['valor'])
    forma_pagamento = dados['forma_pagamento']
    bandeira = dados['bandeira']
    parcelas = int(dados['parcelas']) if 'parcelas' in dados and dados['parcelas'] else 1

    if forma_pagamento == "DEBITO":
        # Busca a taxa de débito da tabela
        if bandeira in taxas:
            taxa = taxas[bandeira][0]  # A taxa de débito é sempre a primeira
            valor_final = valor + (valor * (taxa / 100))
            return jsonify({"valor_final": round(valor_final, 2)})
        else:
            return jsonify({"erro": "Bandeira inválida."}), 400

    elif forma_pagamento == "CREDITO":
        # Busca a taxa de crédito parcelado
        if bandeira in taxas and 1 <= parcelas <= 18:
            taxa = taxas[bandeira][parcelas]
            valor_final = valor + (valor * (taxa / 100))
            return jsonify({"valor_final": round(valor_final, 2)})
        else:
            return jsonify({"erro": "Bandeira ou parcelas inválidas."}), 400

    return jsonify({"erro": "Forma de pagamento inválida."}), 400


if __name__ == '__main__':
    app.run(debug=True)
