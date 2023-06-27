import os
import openai
import subprocess
from subprocess import Popen, PIPE, call

def query_openai(prompt, text):
    openai.api_key = os.environ['POPCLIP_OPTION_APIKEY']
    content = ""
    for chunk in openai.ChatCompletion.create(
        model= os.environ['POPCLIP_OPTION_MODEL'],
            # "gpt-3.5-turbo",
            # "gpt-3.5-turbo-16k",
            # "gpt-3.5-turbo-0613",
            # "gpt-4",
            # "gpt-4-0613",
            # "gpt-4-32k",
            # "gpt-4-32k-0613",
        messages=[
            {"role": "system", "content":"Revise the following sentences to make them more clear, concise, and coherent . /n Please DO NOT note that you need to list the changes and briefly explain why. /n You will reply to me in Chinese."},
            {"role": "user", "content":text}
        ],
        stream=True,
        temperature=0.22,
    ):
        content += chunk["choices"][0].get("delta", {}).get("content", "")
    return content

def get_icon_path():
    disk_prefix = subprocess.Popen('osascript -e \'path to desktop as text\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode()
    disk_prefix = disk_prefix.split(':')[0]
    icon_path = disk_prefix + os.getcwd().replace('/', ':') + ':assets:chatgpt-icon-tranparent.svg'
    return icon_path

def show_response_dialog(content, icon_path):
    script = f'''
    try
        display dialog "{content}" with icon alias "{icon_path}" with title "popGPT" buttons {{"I Know", "Replace", "Copy"}} default button 3
        set button to the button returned of the result
        return button
    on error errMsg
        display alert errMsg
    end try
    '''
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, text=True)
    stdout, stderr = p.communicate(script)
    if stdout.strip() == "Copy" or stdout.strip() == "Replace":
        call(('osascript', '-e', f'set the clipboard to "{content}"'))
        if stdout.strip() == "Replace":
            call(('osascript', '-e', 'tell application "System Events" to keystroke "v" using command down'))

if __name__ == "__main__":
    response_text = query_openai(input, os.environ['POPCLIP_TEXT'])
    icon_path = get_icon_path()
    show_response_dialog(response_text, icon_path)
