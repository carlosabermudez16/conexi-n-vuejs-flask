from flask import Flask, request, jsonify, json
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Cors = CORS(app)


CORS(app, resources={r'/*': {'origins': '*'}}, CORS_SUPPORTS_CREDENTIALS = True)

app.config['CORS_HEADERS'] = 'Content-Type'

###############
app.config['SQLALCHEMY_DATABASE_URI']= f'mysql+mysqlconnector://admin:123456@localhost:3306/integrationdb_flask_vue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
print ('conexión establecida')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(15))
    department = db.Column(db.String(15))
    
    def __init__(self,name,department):
        self.name = name
        self.department = department

db.create_all()
###############

@app.route("/dataentry", methods = ["GET","POST"])
def submitData():
    
    # insertar dato
    if request.method == "POST":
        
        name = request.get_json().get('name')
        department = request.get_json().get('department')
        
        # se inserta el dato
        nuevo_usuario = User(name=name,department=department)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
    
    # Consulta dato
    user = User.query.all()    
    lista = []
    for i in user:
        dic = {}
        dic["NAME"] = i.name
        dic["DEPARTMENT"] = i.department
        lista.append(dic)
    
    return jsonify({"datos": lista})

if __name__ == '__main__':
    app.run(debug = False)