from flask import Flask, request, jsonify

#para rodar flask --app api run

app = Flask(__name__)

# Rota para obter todos os dados
@app.route('/api/produtos', methods=['GET'])

def obter_produtos():
    produto = request.args.get('produto')

# COMEÇA AQUI

    
    # aqui vamos rodar a rede
    classificacao = "PAPELARIA"






# TERMINA AQUI

    dados = {"produto": produto, "classificacao": classificacao}

    return jsonify({"dados": dados})

if __name__ == '__main__':
    app.run(debug=True)