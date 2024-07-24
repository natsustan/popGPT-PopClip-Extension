const prefixes = {
    "native": "Paraphrase the following sentences to make it more native:\n",
    "revise": "Revise the following sentences to make them more clear concise and coherent:\n",
    "standard": "Correct this to standard English:\n",
    "polish": "Please correct the grammar and polish the following sentences, do not provide any translation, comments, or notes, and use the same language as input:\n",
    "authentic": "Rewrite the text in authentic English:\n",
    "ielts": "Rewrite the text using IELTS standard:\n",
}
const messages = []; // history of previous messages
async function chat (input, options) {
  const openai = require("axios").create({
    baseURL: options.baseURL,
    headers: { Authorization: `Bearer ${options.apikey}` },
  });
  messages.push(
    { "role": "system", "content": "Revise the following sentences to make them more clear, concise, and coherent . /n Please DO NOT note that you need to list the changes and briefly explain why. /n You will reply to me in Chinese." },
    { "role": "user", "content": input.text }
    );
  const { data } = await openai.post("/chat/completions", {
    model: options.model,
    messages,
    temperature: parseFloat(options.temperature),
  });
  messages.push(data.choices[0].message);
  return input.text.trimEnd() + "\n\n" + messages.at(-1).content.trim();
};