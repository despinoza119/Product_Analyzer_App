from openai import OpenAI

client = OpenAI(api_key="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")
import os


def chat_with_chatgpt(prompt,model="gpt-3.5-turbo"):
    response = client.chat.completions.create(model=model,
    messages=[
        {
            "role": "system",
            "content": "You will do a summary of a youtube video based on transcripts, this information is comapring two products. You can create a list of pros and cons of each product and then compare them."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0)
    return response.choices[0].message.content

def compare_products():
    file = open('./output/my_transcript_text_only.txt','r')

    user_prompt = file.read()

    chatbot_response = chat_with_chatgpt(user_prompt)

    return chatbot_response