import math
import os
import json
import openai
import re

class OpenAI_API:
    def __init__(self):
        self
    
    def generate_map_JSON(self, map_description):
        sample_JSON = json.dumps(json.load(open("src\Maps\Voyager.json")))
        prompt = map_description + " " + sample_JSON


    
    def generate_enemy_JSON(self, enemy_description):
        sample_JSON = json.dumps(json.load(open("src\Maps\Voyager.json"))['enemies'])
        prompt = f"This JSON represents game enemies. Make 5 'enemies' JSON for a {enemy_description} game. {sample_JSON}"
        response = self.make_api_call(prompt)
        cleaned = self.clean_json_response(response['choices'][0]['text'])
        return cleaned

    def clean_json_response(self, response):
        cleaned = re.sub(r'\n\n', r'', response)
        # cleaned = re.sub(r'\\', r'', cleaned)
        # cleaned = cleaned.replace("'[{", '[{')
        JSON = json.loads(cleaned)
        return JSON

    def make_api_call(self, prompt):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        current_tokens = len(prompt)/4
        max_tokens = 4096
        remaining_tokens = math.floor(max_tokens - current_tokens-300)

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=remaining_tokens,
                temperature=0.9
            )
            return response
        except:
            print("Error: OpenAI API call failed")