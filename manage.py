from flask import Flask, redirect, render_template, request
import json
from app.utils import chat


app = Flask(__name__, template_folder=r'.\app\templates')


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


@app.route('/', methods=['GET', 'POST'])
def PromptSet():
    if request.method == 'GET':
        return render_template(r'form.html')
    else:
        prompt: str = request.form.get('prompt')
        chat.promptSet(info, promptData, prompt)
        return redirect('/chat')


@app.route('/chat', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text: str = request.form.get('text')
        message: str = chat.chatWithGPT(text, info, configData)
        print(message)
        return render_template(r'index.html', processed_text=message)
    else:
        return render_template(r'index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=False)
