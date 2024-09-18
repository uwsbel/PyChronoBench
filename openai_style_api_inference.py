import json
from tqdm import tqdm
from openai import OpenAI
import os
#read any key for open-ai style APIs
key=os.environ.get("KEY")
opensource_model_links = {
    "gemma-2-9b-it": "google/gemma-2-9b-it",
    "gemma-2-27b-it": "google/gemma-2-27b-it",
    "gemma-2-2b-it":"google/gemma-2-2b-it",
    "llama-3.1-405b-instruct": "meta/llama-3.1-405b-instruct",
    "llama-3.1-70b-instruct":"meta/llama-3.1-70b-instruct",
    "llama-3.1-8b-instruct":"meta/llama-3.1-8b-instruct",
    "phi-3-mini-128k-instruct":"microsoft/phi-3-mini-128k-instruct",
    "phi-3-medium-128k-instruct":"microsoft/Phi-3-medium-128k-instruct",
    "nemotron-4-340b-instruct":"nvidia/nemotron-4-340b-instruct",
    "mistral-nemo-12b-instruct":"nv-mistralai/mistral-nemo-12b-instruct",
    "mixtral-8x22b-instruct-v0.1":"mistralai/mixtral-8x22b-instruct-v0.1",
    "codestral-22b-instruct-v0.1":"mistralai/codestral-22b-instruct-v0.1",
    "mixtral-8x7b-instruct-v0.1":"mistralai/mixtral-8x7b-instruct-v0.1",
    "mistral-large-latest":"mistralai/mistral-large",
    "mamba-codestral-7b-v0.1":"mistralai/mamba-codestral-7b-v0.1",
}
def test_prompt(instruction,model_link):
    try:
        prompts=f"You are a PyChrono expert. {instruction}"
        completion = client.chat.completions.create(
            model=model_link,  # Replace with the appropriate model link or name
            messages=[
                #{"role": "system", "content": "You are a PyChrono expert."},
                {"role": "user", "content": prompts}
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
def test_LLMs(data,model_link):
    saved_result = []

    for entry in tqdm(data):

        original_instruction = entry['instruction']
        output = test_prompt(original_instruction,model_link)
        saved_result.append({
            "instruction": original_instruction,
            "output": output
        })

    return saved_result

test_model_list= ["mamba-codestral-7b-v0.1"]
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = key
)
Output_path=r"D:\PyChronoBench\llm_outputs"

for test_model in tqdm(test_model_list):
    print('entering model:', test_model)
    test_model_link = opensource_model_links[test_model]
    output_model_path = os.path.join(Output_path, test_model)
    #os.makedirs(output_model_path, exist_ok=True)

    with open('pychrono_test.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    result = test_LLMs(json_data,test_model_link)
    Output_json_path=os.path.join(Output_path, f"{test_model}.json")
# Save the improved data to a new JSON file
    with open(Output_json_path, 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False, indent=4)

    print(f'{test_model} results saved to {Output_json_path}".')