import os
import json
import re
import pandas as pd


# Function to extract correct answers using various regex patterns
def extract_correct_answers(json_data):
    correct_answers = []

    # Compile regex patterns once
    double_bracket_pattern = re.compile(r'\[\[([A-D])\]\]')
    bold_pattern = re.compile(r'\*\*([A-D])\.')
    single_quote_pattern = re.compile(r"'([A-D])\.")
    bold_quoted_pattern = re.compile(r"\*\*'([A-D])\.")
    traditional_pattern = re.compile(r'^([A-D])\.')
    special_case_pattern = re.compile(r'([A-D])\.\s*\'')
    fallback_pattern = re.compile(r'\b([A-D])\.')

    for entry in json_data:
        output = entry.get('output', '')
        correct_answer = ""

        # Try all regex patterns to find the correct answer
        match = double_bracket_pattern.search(output)
        if not match:
            match = bold_pattern.search(output)
        if not match:
            match = single_quote_pattern.search(output)
        if not match:
            match = bold_quoted_pattern.search(output)
        if not match:
            match = traditional_pattern.match(output)
        if not match:
            match = special_case_pattern.search(output)
        if not match:
            match = fallback_pattern.search(output)

        if match:
            correct_answer = match.group(1)

        correct_answers.append(correct_answer)

    return correct_answers
# Function to calculate mistakes and save problem with incorrect answers
def find_mistakes(user_answers, correct_answers):
    correct_answers_user = extract_correct_answers(user_answers)
    correct_answers_solution = extract_correct_answers(correct_answers)

    mistakes = []

    for idx, (ans_user, ans_solution) in enumerate(zip(correct_answers_user, correct_answers_solution)):
        if ans_user != ans_solution:
            # Capture the question, the LLM's incorrect answer, and the correct answer
            question = user_answers[idx].get('instruction', 'No instruction found')
            output = user_answers[idx].get('output', 'No output found')
            mistakes.append({
                'Problem': question,
                'LLM Output': output,
                'Correct Answer': ans_solution,
                'Mistaken Answer': ans_user
            })

    return mistakes
# Function to process all JSON files in a folder and save mistakes to a CSV file
def process_llm_mistakes(llm_output_path, truth_file, mistakes_csv_path):
    # Load the ground truth data
    with open(truth_file, 'r', encoding='utf-8') as file:
        truth_data = json.load(file)

    all_mistakes = []

    # Iterate over all JSON files in the specified folder
    for filename in os.listdir(llm_output_path):
        if filename.endswith(".json"):
            model_path = os.path.join(llm_output_path, filename)
            with open(model_path, 'r', encoding='utf-8') as file:
                print("loading the ", model_path)
                model_data = json.load(file)

            # Find mistakes for this model
            mistakes = find_mistakes(model_data, truth_data)

            # Add the model name to each mistake for context
            for mistake in mistakes:
                mistake['Model'] = filename

            # Append all mistakes for this model
            all_mistakes.extend(mistakes)

    # Save the mistakes to a CSV file using pandas
    df_mistakes = pd.DataFrame(all_mistakes)
    df_mistakes.to_csv(mistakes_csv_path, index=False)

    print(f"Mistakes saved to {mistakes_csv_path}")
# Set the folder path, ground truth file, and output CSV file paths
llm_output_path = r"D:\PyChronoBench\llm_outputs"
truth_file_path = 'pychrono_test.json'  # Path to the ground truth JSON file
mistakes_csv_path = 'llm_mistakes.csv'  # Path to save the mistakes to CSV

# Process all JSON files and save mistakes to CSV
process_llm_mistakes(llm_output_path, truth_file_path, mistakes_csv_path)
