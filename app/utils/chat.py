import traceback
import openai

# 接受用户文本，执行指令


def chatWithGPT(text: str, info, configData: dict):
    try:
        if text.strip() == '':
            return '您好，我是人工智能助手，如果您有任何问题，请随时告诉我，我将尽力回答。\n如果您需要重置我们的会话，请回复`重置会话`'

        if '重置会话' == text.strip():
            # 清除对话内容但保留人设
            info.msg = info.msg[:1]
            return "会话已重置"
        if '重置人格' == text.strip():
            # 清空对话内容并恢复预设人设
            info.msg = [
                {"role": "system", "content": configData['chatgpt']['preset']}
            ]
            return '人格已重置'
        if '指令说明' == text.strip():
            return "指令如下(群内需@机器人)：\n1.[重置会话] 请发送 重置会话\n2.[设置人格] 请发送 设置人格+人格描述\n3.[重置人格] 请发送 重置人格\n4.[指令说明] 请发送 " \
                   "指令说明\n注意：\n重置会话不会清空人格,重置人格会重置会话!\n设置人格后人格将一直存在，除非重置人格或重启逻辑端!"
        if text.strip().startswith('设置人格'):
            # 清空对话并设置人设
            info.msg = [
                {"role": "system", "content": text.strip().replace('设置人格', '')}
            ]
            return '人格设置成功'
        # 设置本次对话内容
        info.msg.append({"role": "user", "content": text})
        # 与ChatGPT交互获得对话内容
        message = chat(info, configData)
        # 记录上下文
        if not message.startswith('Please try again!'):
            info.msg.append({"role": "assistant", "content": message})

        print("ChatGPT返回内容: ")
        print(message)
        return message

    except Exception as error:
        traceback.print_exc()
        return str('异常: ' + str(error))


# 调用API
def chat(info, configData: dict):
    try:
        if not configData['openai']['api_key']:
            return "请设置Api Key"
        else:
            openai.api_key = configData['openai']['api_key']

        resp: str = openai.ChatCompletion.create(
            model=configData['chatgpt']['model'],
            messages=info.msg
        )
        resp = resp['choices'][0]['message']['content']

    except openai.OpenAIError as e:
        print('openai 接口报错: ' + str(e))
        resp = 'Please try again! Restart the chat!'
        info.msg = [
            {"role": "system", "content": configData['chatgpt']['preset']}
        ]
        # resp = str(e)
    return resp

def promptSet(info,promptData:dict,promptCmd:str):
    for prompt in promptData:
        if prompt["cmd"]==promptCmd:
            info.msg=[{"role": "system", "content": prompt['prompt']}]
            return
    print("NO such prompt cmd!")
    
