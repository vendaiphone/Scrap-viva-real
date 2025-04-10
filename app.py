from flask import Flask, render_template, request, jsonify
from scraper import buscar_imoveis

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    dados = request.json
    try:
        resultado = buscar_imoveis(
            cidade=dados["cidade"],
            estado=dados["estado"],
            bairro=dados["bairro"],
            metragem=dados["metragem"],
            tipo=dados["tipo"]
        )
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
