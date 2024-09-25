from flask import Flask, request, jsonify
import redis
import json
import re

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

USERS_KEY = "chat_users" 
MESSAGES_KEY = "chat_messages"

def is_valid_nickname(nickname):
    return re.match(r'^[a-zA-Z0-9]{1,20}$', nickname)

@app.route('/join-chat/<nickname>', methods=['GET'])
def join_chat(nickname):
    if not is_valid_nickname(nickname):
        return jsonify({"error": "invalid_nickname"}), 400
    
    if r.sismember(USERS_KEY, nickname):
        return jsonify({"error": "already_in_use"}), 400
    
    r.sadd(USERS_KEY, nickname)
    
    users = list(r.smembers(USERS_KEY))
    users = [user.decode('utf-8') for user in users]
    
    return jsonify({"users": users}), 200

@app.route('/send-message/<nickname>', methods=['POST'])
def send_message(nickname):
    if not r.sismember(USERS_KEY, nickname):
        return jsonify({"error": "user_not_found"}), 404

    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "empty_message"}), 400
    
    r.lpush(MESSAGES_KEY, json.dumps({"nickname": nickname, "message": message}))

    return jsonify({"status": "ok"}), 200

@app.route('/get-messages/<nickname>', methods=['GET'])
def get_messages(nickname):
    if not r.sismember(USERS_KEY, nickname):
        return jsonify({"error": "user_not_found"}), 404

    
    messages = r.lrange(MESSAGES_KEY, 0, -1) 
    messages = [json.loads(msg.decode('utf-8')) for msg in messages]

    return jsonify({"messages": messages}), 200

if __name__ == '__main__':
    app.run(host="192.168.1.45", port=5000)
