import random
from flask import Flask, jsonify, request
import time
import json

app = Flask(__name__)
lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

games = {
}

def liste_mots(L):
    f = []
    for i in L:
        f.append(i[0])
    return f

with open("mots.csv","r",encoding="utf8") as f:
    table_mots = []
    ligne = f.readline()
    motVerifLong = ""  
    while ligne != "":
        motVerifLong = ligne.replace("\n","")
        table_mots.append([motVerifLong])
        ligne = f.readline()
table_mots = liste_mots(table_mots)

# Jeu :


def actuParties():
    global games
    for room in games.keys():
        winPlayers = []
        if games[room]["actualWord"] == "":
            games[room]["actualWord"] = random.choice(table_mots)
        for player in games[room]["players"].keys():
            games[room]["players"][player]["hintWord"] = ""
            for i in games[room]["actualWord"]:
                if i in games[room]["players"][player]["found"]:
                    games[room]["players"][player]["hintWord"] += i
                else:
                    games[room]["players"][player]["hintWord"] += "-"
            if games[room]["players"][player]["hintWord"] == games[room]["actualWord"]:
                games[room]["players"][player]["victory"] = time.time()
            if games[room]["players"][player]["victory"] != False:
                winPlayers.append([player, games[room]["players"][player]["victory"]])
        if len(winPlayers) >= len(games[room]["players"].keys()):
            for player in games[room]["players"].keys():
                games[room]["players"][player]["score"] += 1
            games[room]["players"] = {i:{"score":games[room]["players"][player]["score"], "hintWord":"", "attempts":0, "found":" ", "errors":"", "victory":False} for i in games[room]["players"].keys()}
            actuParties()

def essai(room, pseudo, car):
    global games

    if car in games[room]["actualWord"]:
        games[room]["players"][pseudo]["found"] += car
    else:
        games[room]["players"][pseudo]["errors"] += car
        games[room]["players"][pseudo]["attempts"] += 1



@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'OK', 'time':str(time())})

@app.route('/join', methods=['POST'])
def join():
    global games
    if ('roomCode' in request.form) and ('pseudo' in request.form):
        try:
            room = request.form['roomCode']
            pseudo = request.form['pseudo']
            if not(room in [i for i in games.keys()]):
                games[room] = {"actualWord":"","players":{}}
            if not(pseudo in [i for i in games[room]["players"].keys()]):
                games[room]["players"][pseudo] = {"score":0, "hintWord":"", "attempts":0, "found":" ", "errors":"", "victory":False}
            actuParties()
            return jsonify({'roomCode': room, "players":{i:(games[room]["players"][i]["score"],games[room]["players"][i]["victory"]) for i in games[room]["players"].keys()}, "personal":games[room]["players"][pseudo]})
        except:
            return jsonify({'error': 'Invalid data'})
    else:
        return jsonify({'error': 'Room code or pseudo is missing'})

@app.route('/refresh', methods=['POST'])
def refresh():
    global games
    if ('roomCode' in request.form) and ('pseudo' in request.form):
        try:
            room = request.form['roomCode']
            pseudo = request.form['pseudo']
            actuParties()
            return jsonify({'roomCode': room, "players":{i:(games[room]["players"][i]["score"],games[room]["players"][i]["victory"]) for i in games[room]["players"].keys()}, "personal":games[room]["players"][pseudo]})
        except:
            return jsonify({'error': 'Invalid data'})
    else:
        return jsonify({'error': 'Room code or pseudo is missing'})

@app.route('/play', methods=['POST'])
def play():
    global games
    if ('roomCode' in request.form) and ('pseudo' in request.form) and ('car' in request.form):
        try:
            room = request.form['roomCode']
            pseudo = request.form['pseudo']
            car = request.form['car']
            essai(room, pseudo, car)
            actuParties()
            return jsonify({'roomCode': room, "players":{i:(games[room]["players"][i]["score"],games[room]["players"][i]["victory"]) for i in games[room]["players"].keys()}, "personal":games[room]["players"][pseudo]})
        except:
            return jsonify({'error': 'Invalid data'})
    else:
        return jsonify({'error': 'Room code or pseudo is missing'})

@app.route('/win', methods=['POST'])
def win():
    global games
    if ('roomCode' in request.form) and ('pseudo' in request.form):
        try:
            room = request.form['roomCode']
            pseudo = request.form['pseudo']
            games[room]["players"][pseudo]["victory"] = time.time()
            actuParties()
            return jsonify({'roomCode': room, "players":{i:(games[room]["players"][i]["score"],games[room]["players"][i]["victory"]) for i in games[room]["players"].keys()}, "personal":games[room]["players"][pseudo]})
        except Exception as e:
            a = f"Error : {e}"
            return jsonify({'error': a})
    else:
        return jsonify({'error': 'Room code or pseudo is missing'})


if __name__ == '__main__':
    app.run(host='192.168.1.92', port=5000)