from flask import Flask, render_template, request
import json
from app.utils import chat


app = Flask(__name__, template_folder=r'.\app\templates')


with open(r'app\config.json', "r", encoding='utf-8') as configFile:
    configData = json.load(configFile)

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
def index():
    if request.method == 'POST':
        text: str = request.form.get('text')
        message: str = chat.chatWithGPT(text, info, configData)
        print(message)
        return render_template(r'index.html', processed_text=message)
    else:
        return render_template(r'index.html')


if __name__ == '__main__':
    app.run()
