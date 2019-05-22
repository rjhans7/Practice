from flask import Flask, render_template, request, session, Response
from sqlalchemy import and_
from sqlalchemy import or_
from web.model import entities
from web.database import connector
import json
import datetime

app = Flask(__name__)
db = connector.Manager()
engine = db.createEngine()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    if 'logged_user' not in session:
        return render_template('login.html')

    else:
        return render_template("chat/chat.html")


@app.route('/sign_up', methods=['GET'])
def sign_up():
    return render_template("sign_up.html")



@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/do_login', methods=['POST'])
def do_login():
    Username = request.form['Username']
    Password = request.form['Password']
    session = db.getSession(engine)
    users = session.query(entities.User)

    for user in users:
        if user.username == Username and user.password == Password:
            return render_template("chat/chat.html")
    return render_template("fail.html")


@app.route('/mobile_login', methods=['POST'])
def mobile_login():
    body = request.get_json(silent=True)
    print(body)
    username = body['username']
    password = body['password']
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(
        and_(entities.User.username == username , entities.User.password==password)
    ).first()
    if user != None :
        session['logged'] = user.id
        return Response(json.dumps(
            {'response':True, 'id':user.id},
            cls=connector.AlchemyEncoder
        ), mimetype='application/json')
    else:
        return Response(json.dumps(
            {'response': False},
            cls=connector.AlchemyEncoder
        ), mimetype='application/json')



@app.route('/users', methods=['POST'])
def post_users():
    username = request.form['username']
    name = request.form['name']
    fullname = request.form['fullname']
    password = request.form['password']
    user = entities.User (username = username,
                          name = name,
                          fullname = fullname,
                          password = password)
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Create User'


@app.route('/users', methods=['GET'])
def users():
    session = db.getSession(engine)
    users = session.query(entities.User)
    data = []

    for user in users:
        data.append(user)
    return Response( json.dumps({'data':data}, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        session.delete(user)
    session.commit()
    return "Deleted User!"


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)
    response = " "
    for user in users:
        response += str(user.id) + " -> " + user.name
    return response


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    session = db.getSession(engine)
    users = session.query(entities.User).filter(entities.User.id == id)

    for user in users:
        user.username = request.form['username']
        user.name = request.form['name']
        user.fullname = request.form['fullname']
        user.password = request.form['password']
        session.add(user)

    session.commit()
    return "User updated!"


@app.route('/setup')
def setup_users():
    user = entities.User (username = username,
                          name = name,
                          fullname = fullname,
                          password = password)
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Create User'


@app.route('/cuantasletras/<nombre>')  # comunicacion stateles
def cuantas_letras(nombre):
    return str(len(nombre))


@app.route('/sumar/<numero>')
def sumar(numero):
    if 'suma' not in session:  # session sirve para guardar en memoria
        session['suma'] = 0
    session['suma'] = int(session['suma']) + int(numero)
    return str(session['suma'])


@app.route('/chat')
def chat():
    return render_template("chat/chat.html")



# MESSAGE API
@app.route('/messages', methods=['GET'])
def get_messages():
    sessiondb = db.getSession(engine)
    messages = sessiondb.query(entities.Message)
    response = []

    for message in messages:
        response.append(message)

    return Response(
        json.dumps({'data': response},
                   cls=connector.AlchemyEncoder),mimetype='application/json')

@app.route('/messages', methods=['POST'])
def create_message():
    body = request.get_json(silent=True)
    sessiondb = db.getSession(engine)
    content = body['content']
    user_from_id = body['user_from_id']
    user_to_id = body['user_to_id']

    user_from = sessiondb.query(entities.User).filter(entities.User.id == user_from_id).first()
    user_to = sessiondb.query(entities.User).filter(entities.User.id == user_to_id).first()

    message = entities.Message(
        content = content,
        user_from = user_from,
        user_to = user_to,
        sent_on = datetime.datetime.utcnow()
    )
    sessiondb.add(message)
    sessiondb.commit()
    return Response(json.dumps({'response': True},cls=connector.AlchemyEncoder),
                    mimetype = 'application/json')

@app.route('/chats/<user_from_id>/<user_to_id>', methods=['GET'])
def getChats(user_from_id,user_to_id):
    sessiondb = db.getSession(engine)
    chats = sessiondb.query(entities.Message).filter(
        or_(
            and_(entities.Message.user_from_id == user_from_id, entities.Message.user_to_id == user_to_id ),
            and_(entities.Message.user_from_id == user_to_id, entities.Message.user_to_id == user_from_id)
        )
    )
    data  = []
    for chat in chats:
        data.append(chat)

    return Response(
        json.dumps({'response':data},cls=connector.AlchemyEncoder),
        mimetype='application/json')


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('0.0.0.0'))
