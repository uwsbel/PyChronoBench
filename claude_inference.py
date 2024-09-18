import os
import json
from tqdm import tqdm
import anthropic


client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

def read_script(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()



opensource_model_links = {
    "claude-3-5-sonnet": "claude-3-5-sonnet-20240620",
}

def test_prompt(instruction,model_link):
    prompt = instruction
    try:
        prompts=f"You are a PyChrono expert. {instruction}"
        completion = client.messages.create(
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
        new_prompt = completion.content[0].text

        print(new_prompt)
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

test_model_list= ["claude-3-5-sonnet"]

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