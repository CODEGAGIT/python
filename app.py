from flask import Flask, request, render_template, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)

#Creation de la base de donnée

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///vente.db'
db = SQLAlchemy(app)

# Création de table Produit

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(60), nullable = False)
    prix = db.Column(db.Float(100), nullable = False)
    quantité = db.Column(db.Float(50), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"vente {self.name}"


class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    desc = db.Column(db.String(60), nullable = False)
    article = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    def __repr__(self):
        return f"vente {self.name}"

db.create_all()


# définition des routes

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        new_produit = Produit(name = name)
        try:
            db.session.add(new_produit)
            db.session.commit()
            return redirect("/")
        except Exception:
            return "une erreur s'est produite !!!"
    else:
        produits = Produit.query.order_by(Produit.created_at)
    return render_template("index.html", produits = produits)

