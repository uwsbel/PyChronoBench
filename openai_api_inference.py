import json
from tqdm import tqdm
from openai import OpenAI
import os
# Initialize the OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def test_prompt(instruction):
    prompt = instruction
    try:
        completion = client.chat.completions.create(
            #model="gpt-4o-mini",  # Replace with the appropriate model link or name
            #model="ft:gpt-4o-mini-2024-07-18:uw-sbel::A6Rd900h",
            model="ft:gpt-4o-mini-2024-07-18:uw-sbel::A877JndG",
            messages=[
                {"role": "system", "content": "You are a PyChrono expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            top_p=1.0,
            max_tokens=1024,
            stream=False
        )
        new_prompt = completion.choices[0].message.content.strip()
        return new_prompt
    except Exception as e:
        print('error2:', e)
        return str(e), str(e)


def test_LLMs(data):
    saved_result = []

    for entry in tqdm(data):

        original_instruction = entry['instruction']
        output = test_prompt(original_instruction)
        saved_result.append({
            "instruction": original_instruction,
            "output": output
        })

    return saved_result

# Load the JSON data with correct encoding
with open('deduplicated_pychrono_test.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Improve the quality of the JSON data
result = test_LLMs(json_data)

# Save the improved data to a new JSON file
with open('pychrono_test_finetuned1.json', 'w', encoding='utf-8') as outfile:
    json.dump(result, outfile, ensure_ascii=False, indent=4)

print(f'Improved data saved to "test_result.json".')