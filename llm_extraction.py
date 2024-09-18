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


# Function to save extracted answers to a CSV for each JSON file
def save_llm_results_to_csv(llm_output_path, truth_file, llm_csv_folder):
    # Load the ground truth data
    with open(truth_file, 'r', encoding='utf-8') as file:
        truth_data = json.load(file)

    correct_answers_solution = extract_correct_answers(truth_data)

    # Iterate over all JSON files in the specified folder
    for filename in os.listdir(llm_output_path):
        if filename.endswith(".json"):
            model_path = os.path.join(llm_output_path, filename)
            with open(model_path, 'r', encoding='utf-8') as file:
                print("loading the ", model_path)
                model_data = json.load(file)

            # Extract correct answers from the model output
            extracted_answers = extract_correct_answers(model_data)

            # Create a list of problem/answer data
            problem_data = []
            for idx, entry in enumerate(model_data):
                problem = entry.get('instruction', 'No instruction found')
                output = entry.get('output', 'No output found')
                correct_answer = correct_answers_solution[idx]
                extracted_answer = extracted_answers[idx] if idx < len(extracted_answers) else "Not extracted"

                # Append the row to the problem_data list
                problem_data.append({
                    'Problem': problem,
                    'Correct Answer': correct_answer,
                    'LLM Output': output,
                    'Extracted Answer': extracted_answer
                })

            # Save the results to a CSV file for the current LLM model
            llm_csv_path = os.path.join(llm_csv_folder, f'{filename}.csv')
            df_problems = pd.DataFrame(problem_data)
            df_problems.to_csv(llm_csv_path, index=False)

            print(f"Results saved to {llm_csv_path}")


# Set the folder path, ground truth file, and output CSV folder path
llm_output_path = r"D:\PyChronoBench\llm_outputs"
truth_file_path = 'pychrono_test.json'  # Path to the ground truth JSON file
llm_csv_folder = r"D:\PyChronoBench\llm_csv"  # Folder to save the CSV files for each LLM

# Process all JSON files and save extracted answers to individual CSVs
save_llm_results_to_csv(llm_output_path, truth_file_path, llm_csv_folder)
