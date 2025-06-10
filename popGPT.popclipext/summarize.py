import os
from openai import OpenAI
import subprocess
from subprocess import Popen, PIPE, call
import json

try:
    # 初始化OpenAI客户端
    client = OpenAI(
        api_key=os.environ['POPCLIP_OPTION_APIKEY'],
        base_url="https://openrouter.ai/api/v1",
    )

    # 获取用户选中的文本
    input_text = os.environ.get('POPCLIP_TEXT', '')
    
    if not input_text:
        print("ERROR: No text selected")
        exit(1)

    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model=os.environ['POPCLIP_OPTION_MODEL'],
        messages=[
            {"role": "system", "content": "You are an assistant helping summarize a document. Use this format, replacing text in brackets with the result. Do not include the brackets in the output: /n/n Summary in [Identified language of the document]: /n/n[One-paragaph summary of the document using the identified language.]."},
            {"role": "user", "content": input_text},
        ],
        temperature=0.2,
    )

    # 获取回复内容
    completion_content = completion.choices[0].message.content

    # 使用临时文件存储回复内容，避免特殊字符问题
    with open('/tmp/popclip_response.txt', 'w', encoding='utf-8') as f:
        f.write(completion_content)

    # 创建安全的AppleScript
    apple_script = '''
    set responseFile to "/tmp/popclip_response.txt"
    set responseContent to (do shell script "cat " & quoted form of responseFile)
    
    try
        set dialogResult to display dialog responseContent with title "popGPT" buttons {"I Know", "Copy", "Replace"} default button 3
        set buttonPressed to button returned of dialogResult
        do shell script "echo " & quoted form of buttonPressed
    on error errMsg
        do shell script "echo 'ERROR: " & errMsg & "'"
    end try
    '''
    
    # 执行AppleScript并获取结果
    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, text=True)
    stdout, stderr = p.communicate(apple_script)
    
    # 输出可能的错误信息以便调试
    if stderr:
        print(f"ERROR: {stderr}")
        exit(1)
    
    # 处理按钮操作
    button_pressed = stdout.strip()
    
    if button_pressed == "Copy" or button_pressed == "Replace":
        # 将回复内容放入剪贴板
        copy_script = f'''
        do shell script "cat /tmp/popclip_response.txt | pbcopy"
        '''
        subprocess.call(['osascript', '-e', copy_script])
        
        # 如果选择替换，则执行粘贴操作
        if button_pressed == "Replace":
            paste_script = '''
            tell application "System Events" to keystroke "v" using command down
            '''
            subprocess.call(['osascript', '-e', paste_script])
    
    # 返回按钮结果
    print(button_pressed)
    
except Exception as e:
    # 异常处理，确保错误可见
    error_message = str(e).replace('"', '\\"')
    error_script = f'''
    display dialog "PopClip扩展出错: {error_message}" buttons {{"OK"}} default button 1 with icon caution
    '''
    subprocess.call(['osascript', '-e', error_script])
    print(f"ERROR: {str(e)}")
    exit(1)