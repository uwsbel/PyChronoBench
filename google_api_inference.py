import os
import google.generativeai as genai
import os
import json
from tqdm import tqdm#
GEMINI_API_KEY=os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)



def read_script(file_path):
  with open(file_path, "r", encoding="utf-8") as file:
    return file.read()

def test_prompt(instruction,model_link):
    prompt = instruction
    try:
        prompts=f"You are a PyChrono expert. {instruction}"
        generation_config = {
            "temperature": 0.1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name=model_link,
            generation_config=generation_config,
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
        )

        chat_session = model.start_chat(
            history=[
            ]
        )

        response = chat_session.send_message(prompts).text
        #print(response)
        return response
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


opensource_model_links = {
  "Gemini": "gemini-1.5-pro",
    "Gemini-flash":"gemini-1.5-flash"
}

test_model_list = ["Gemini-flash"]

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