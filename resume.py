from openai import OpenAI
import os

client = OpenAI(api_key="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")

def chat_with_chatgpt(prompt,model="gpt-3.5-turbo"):
    response = client.chat.completions.create(model=model,
    messages=[
        {
            "role": "system",
            "content": "Give me two columns of pros and cons for each product separated by a *, is very important to put the * at the end of the first column and at the beginning of the second column.",
            "content": "Always put a ----- separator between the information of each product (obligatory)"
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0)
    print('ChatGPT response')
    return response.choices[0].message.content

def compare_products():
    print('Comparing Products ChatGPT')
    file = open('./output/my_transcript_text_only.txt','r')

    user_prompt = file.read()

    chatbot_response = chat_with_chatgpt(user_prompt)

    return chatbot_response