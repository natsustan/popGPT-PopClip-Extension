# popGPT-PopClip-Extension

## Description

Send the selected text to [ChatGPT](https://openai.com/blog/chatgpt), and append the response.
The main action, **Chat**, sends the selected text to OpenAI's ChatGPT and
appends the response as a new line.

### Configuration

#### API Key
To use this extension, you need to provide it with an API Key for an OpenAI account. To get an API Key:
1. Sign up for an OpenAI Account here: [https://platform.openai.com/](https://platform.openai.com/)
2. Generate an API key here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
3. Copy and paste the API Key (it starts with `sk-`) into the _API Key_ field in the extension's settings.

#### Import the openai library

if needed, install and/or upgrade to the latest version of the OpenAI Python library

```
pip install --upgrade openai
```

### Acknowledgements
Icons:
- "openai" by [Simple Icons](https://simpleicons.org/).

### Requirements
Requires an Open AI API.
