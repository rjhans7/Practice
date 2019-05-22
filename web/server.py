from flask import Flask, render_template, request, session, Response
from database import connector
from model import entities
import json
import datetime

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)
app.secret_key = 'You Will Never Guess'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    if not session.get('logged_user_id'):
        return render_template('login.html')
    else:
        return render_template('success.html')


@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    db_session = db.getSession(engine)
    users = db_session.query(entities.User)

    for user in users:
        if user.username == username and user.password == password:
            session['logged_user_id'] = user.id
            return login()

    return render_template('fail.html')


@app.route('/current_user', methods=['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(
        entities.User.id==session['logged_user_id']).first()
    return Response(json.dumps(user, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/logout')
def logout():
    session.clear()
    return index()


@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")


@app.route('/do_register', methods=['POST'])
def do_register():
    name = request.form['name']
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    print(name, fullname, username, password)

    user = entities.User(username=username,
                         name=name,
                         fullname=fullname,
                         password=password)

    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return "Todo Ok!"


@app.route('/users', methods=['GET'])
def users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)
    data =[]
    for user in users:
        data.append(user)
    Response = json.dumps(data, cls=connector.AlchemyEncoder)
    return Response


@app.route('/clean_users')
def clean_users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)
    for user in users:
        db_session.delete(user)

    db_session.commit()
    return "Todos los usuarios eliminados"


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    data =[]
    for user in users:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods=["PUT"])
def update_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        user.fullname = request.form['fullname']
        user.password = request.form['password']
        user.username = request.form['username']
        db_session.add(user)
    db_session.commit()
    return 'Usuario actualizado'


@app.route('/users/<id>', methods=["DELETE"])
def delete_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        db_session.delete(user)
    db_session.commit()
    return "Usuario eliminado"

#CRUD users
@app.route('/crud_users', methods=['GET'])
def crud_users():
    return render_template("users.html")

#Messages

@app.route('/messages', methods=['GET'])
def messages():
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message)
    data =[]
    for message in messages:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/clean_messages')
def clean_messages():
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message)
    data =[]
    for message in messages:
        data.delete(message)

    db_session.commit()
    return "Todos los usuarios eliminados"


@app.route('/messages/<user_from>/<user_to>', methods=['GET'])
def get_message(user_from, user_to):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message
        ).filter(entities.Message.user_from_id == user_from
        ).filter(entities.Message.user_to_id==user_to)
    data = []
    for message in messages:
        data.append(message)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')

"""
@app.route('/messages/<id>', methods=['GET')
def get_message2(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    data =[]
    for message in messages:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')
"""

@app.route('/messages', methods=['POST'])
def create_message():
    #c = json.loads(request.form['values'])
    c = request.get_json(silent=True)
    db_session = db.getSession(engine)
    user_from = db_session.query(entities.User
        ).filter(entities.User.id == c['user_from_id']).first()
    user_to = db_session.query(entities.User
        ).filter(entities.User.id == c['user_to_id']).first()

    message = entities.Message(content=c['content'],
        user_from = user_from,
        user_to = user_to,
        sent_on = datetime.datetime.utcnow()
                               )
    db_session.add(message)
    db_session.commit()
    return 'Todo OK'


@app.route('/messages/<id>', methods=["PUT"])
def update_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        message.input = request.form['input']
        db_session.add(message)
    db_session.commit()
    return 'Mensaje actualizado'


@app.route('/messages/<id>', methods=["DELETE"])
def delete_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        db_session.delete(message)
    db_session.commit()
    return "Mensaje eliminado"

#stateless

@app.route('/cuantasletras/<nombre>')
def cuantas_letras(nombre):
    return str(len(nombre))

#statefull
@app.route('/suma/<numero>')
def sumar(numero):
    if 'suma' not in session:
        session['suma'] = "0"
    session['suma'] = int(session['suma']) + int(numero)
    return str(session['suma'])



if __name__ == '__main__':
    app.secret_key = ".."
    app.debug=True
    app.run(port=8080, threaded=True, host=('0.0.0.0'))

