from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO, emit
import json
from app.utils import chat


app = Flask(__name__, template_folder=r'app\templates')
socketio = SocketIO(app)

with open(r'app\config.json', "r", encoding='utf-8') as configFile:
    configData = json.load(configFile)

with open(r'app\prompt\chatgpt_prompts.json', "r", encoding='utf-8') as promptFile:
    promptData: list = json.load(promptFile)

# session_config = {
#     'msg': [
#             {"role": "system", "content": configData['chatgpt']['preset']}
#     ]
# }


class Session:
    def __init__(self):
        self.msg = [
            {"role": "system", "content": configData['chatgpt']['preset']}]


info = Session()

# 初始化人格，直接点submmit则不初始化,保持默认
@app.route('/', methods=['GET', 'POST'])
def PromptSet():
    if request.method == 'GET':
        return render_template(r'form.html')
    else:
        prompt: str = request.form.get('prompt')
        chat.promptSet(info, promptData, prompt)
        return redirect('/chat')

# 最开始的版本，暂时注释掉
# @app.route('/chat', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         text: str = request.form.get('text')
#         message: str = chat.chatWithGPT(text, info, configData)
#         print(message)
#         return render_template(r'index.html', processed_text=message)
#     else:
#         return render_template(r'index.html')

# Chat with GPT
@app.route('/chat')
def index():
    return render_template('index2.html')


@socketio.on('connect')
def handle_connect():
    print('Connected to client')


@socketio.on('disconnect')
def handle_disconnect():
    print('Disconnected from client')


@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    text: str = data['message']
    emit('message', {'message': '======================='}, broadcast=True)
    emit('message', {'message': 'User : '+text}, broadcast=True)
    reply: str = chat.chatWithGPT(text, info, configData)
    print(reply)

    emit('message', {'message': 'GPT : '+reply}, broadcast=True)


if __name__ == '__main__':
    # app.run(port=5000, debug=False)
    socketio.run(app, port=5000, debug=True)
