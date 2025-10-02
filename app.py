import os
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "troque_esta_chave_para_producao")

# Configuração do banco MySQL - ajuste conforme seu usuário/senha/host
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "mercado_db")
DB_PORT = os.getenv("DB_PORT", "3306")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    peso = db.Column(db.Numeric(10, 3))

    def __repr__(self):
        return f"<Produto {self.id} {self.tipo} {self.valor}>"

@app.route("/")
def index():
    produtos = Produto.query.order_by(Produto.criado_em.desc() if hasattr(Produto,'criado_em') else Produto.id.desc()).all()
    return render_template("index.html", produtos=produtos)

@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        valor_raw = request.form.get("valor", "0").replace(",", ".").strip()
        peso_raw = request.form.get("peso", "").replace(",", ".").strip()

        # Validações simples
        if not tipo:
            flash("O campo tipo é obrigatório.", "danger")
            return redirect(url_for("novo"))
        try:
            valor = Decimal(valor_raw)
        except Exception:
            flash("Valor inválido.", "danger")
            return redirect(url_for("novo"))

        peso = None
        if peso_raw:
            try:
                peso = Decimal(peso_raw)
            except Exception:
                flash("Peso inválido.", "danger")
                return redirect(url_for("novo"))

        produto = Produto(tipo=tipo, descricao=descricao, valor=valor, peso=peso)
        db.session.add(produto)
        db.session.commit()
        flash("Produto cadastrado com sucesso.", "success")
        return redirect(url_for("index"))

    return render_template("form.html", produto=None, acao="Novo")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    produto = Produto.query.get_or_404(id)
    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        valor_raw = request.form.get("valor", "0").replace(",", ".").strip()
        peso_raw = request.form.get("peso", "").replace(",", ".").strip()

        if not tipo:
            flash("O campo tipo é obrigatório.", "danger")
            return redirect(url_for("editar", id=id))
        try:
            valor = Decimal(valor_raw)
        except Exception:
            flash("Valor inválido.", "danger")
            return redirect(url_for("editar", id=id))

        peso = None
        if peso_raw:
            try:
                peso = Decimal(peso_raw)
            except Exception:
                flash("Peso inválido.", "danger")
                return redirect(url_for("editar", id=id))

        produto.tipo = tipo
        produto.descricao = descricao
        produto.valor = valor
        produto.peso = peso

        db.session.commit()
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("index"))

    # converte para strings para preencher o form
    return render_template("form.html", produto=produto, acao="Editar")

@app.route("/apagar/<int:id>", methods=["POST"])
def apagar(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto removido.", "warning")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # cria tabelas se não existirem
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
