import os
from typing import List
import openai
import argparse
import re

# Load your API key from an environment variable or secret management service

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    print("Running copy kit")
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True)
    args = parser.parse_args()
    user_input = args.input
    if validate_length(user_input):
        branding_result = generate_branding_snippet(user_input)
        keywords_result = generate_keywords(user_input)
        print(f'keywords_result: {keywords_result}')
        print(f'branding_result: {branding_result}')
        print(f'User input: {user_input}')
    else:
        raise ValueError('Input is too long.')


def generate_branding_snippet(prompt:str) -> str:
    enriched_prompt = f'Generate upbeat branding snippet for {prompt}'
    response = openai.Completion.create(model="text-davinci-003", prompt=enriched_prompt, temperature=0, max_tokens=32)
    # Extract output text
    branding_text:str = response['choices'][0]['text']
    # Strip whitespace
    branding_text = branding_text.strip()
    # stores the last character
    last_char = branding_text[-1]
    # adding ... to truncated statements
    if last_char not in {'.','!','?'}:
        branding_text+= '...'
    return branding_text


def validate_length(prompt:str) -> str:
    return len(prompt) <= 12


def generate_keywords(keyword:str) -> List[str]:
    enriched_prompt = f'Generating related branding keywords for {keyword}'
    response = openai.Completion.create(model="text-davinci-003", prompt=enriched_prompt, temperature=0, max_tokens=32)
    # Extract output text
    keyword_text:str = response['choices'][0]['text']
    keyword_array = re.split("\n|,|-", keyword_text)
    keyword_array = [k.lower().strip() for k in keyword_array]
    keyword_array = [k for k in keyword_array if len(k) > 0]
    return keyword_array


if __name__ == '__main__':
    main()