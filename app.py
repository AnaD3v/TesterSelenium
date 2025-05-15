from flask import Flask, render_template, request
from selenium_login import testar_login

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    resultados = []
    if request.method == "POST":
        urls = request.form.getlist("urls")
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return render_template(
                "index.html", resultados=[], erro="Por favor, preencha todos os campos."
            )

        for url in urls:
            if url.strip():
                resultado = testar_login(
                    url.strip(), username.strip(), password.strip()
                )
                resultados.append({"url": url, "resultado": resultado})

    return render_template("index.html", resultados=resultados)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

