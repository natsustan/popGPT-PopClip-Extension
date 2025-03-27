import os
from openai import OpenAI
import subprocess
from subprocess import Popen, PIPE, call

client = OpenAI(
    api_key = os.environ['POPCLIP_OPTION_APIKEY'],
    base_url = "https://openrouter.ai/api/v1",
    )


# Create chat completion with the Chat API 
completion = client.chat.completions.create(
    model= os.environ['POPCLIP_OPTION_MODEL'],
    messages=[
        {"role": "system", "content": "As a Product and UX writer expert, your task is to refine the prompts and copy of a user interface. /n Rewrite the user interface prompts and copy in clear, concise word. Ensure that the rewritten text follows existing style guidelines and accurately conveys the original message, including grammar, punctuation, syntax, and other linguistic conventions. /n And you will reply to me in Chinese."},
        {"role": "user", "content": os.environ['POPCLIP_TEXT']},
    ],
    temperature=0.2,
)

completion_content = completion.choices[0].message.content

def get_icon_path():
    disk_prefix = subprocess.Popen('osascript -e \'path to desktop as text\'', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode()
    disk_prefix = disk_prefix.split(':')[0]
    icon_path = disk_prefix + os.getcwd().replace('/', ':') + ':assets:openai.svg'
    return icon_path

icon_path = get_icon_path()

def show_response_dialog():
    script = f'''
    try
        display dialog "{completion_content}" with icon alias "{icon_path}" with title "popGPT" buttons {{"I Know", "Copy", "Replace"}} default button 3
        set button to the button returned of the result
        return button
    on error errMsg
        display alert errMsg
    end try
    '''
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, text=True)
    stdout, stderr = p.communicate(script)
    if stdout.strip() == "Copy" or stdout.strip() == "Replace":
        call(('osascript', '-e', f'set the clipboard to "{completion_content}"'))
        if stdout.strip() == "Replace":
            call(('osascript', '-e', 'tell application "System Events" to keystroke "v" using command down'))

response = show_response_dialog()
print(response)
