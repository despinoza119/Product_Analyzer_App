from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI() #copy your api key here

def chat_with_chatgpt(prompt,model="gpt-3.5-turbo"):
    response = client.chat.completions.create(model=model,
    messages=[
        {
            "role": "system",
            "content": "You are receiving a youtube transcript and i want you to do a summary specifying the differences between the two products that they talk about",
            "content": "Always put a ----- separator between the information of each product (obligatory), give me the answer always in english"
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