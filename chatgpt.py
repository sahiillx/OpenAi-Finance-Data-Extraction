import openai
from dotenv import load_dotenv
import os

def configure() :
    load_dotenv()

configure()
openai.api_key = os.getenv('api_key')

response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        { "role": "user", "content": "Write a 100 words short note on CM Arvind Kejriwal"}
    ]    
)


def main():
    print(response['choices'][0]['message']['content'])

main()