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

# Function to calculate success rate
def calculate_success_rate(user_answers, correct_answers):
    correct_answers_user = extract_correct_answers(user_answers)
    correct_answers_solution = extract_correct_answers(correct_answers)

    total_questions = len(correct_answers_user)
    correct_matches = sum(1 for ans1, ans2 in zip(correct_answers_user, correct_answers_solution) if ans1 == ans2)

    success_rate = (correct_matches / total_questions) * 100 if total_questions else 0
    return success_rate, correct_matches, total_questions

# Function to process all JSON files in a folder and save results to a CSV file
def process_llm_results(llm_output_path, truth_file, output_csv_path):
    # Load the ground truth data
    with open(truth_file, 'r', encoding='utf-8') as file:

        truth_data = json.load(file)

    results = []

    # Iterate over all JSON files in the specified folder
    for filename in os.listdir(llm_output_path):
        if filename.endswith(".json"):
            model_path = os.path.join(llm_output_path, filename)
            with open(model_path, 'r', encoding='utf-8') as file:
                print("loading the ",model_path )
                model_data = json.load(file)

            # Calculate success rate for this model
            success_rate, correct_matches, total_questions = calculate_success_rate(model_data, truth_data)

            # Print the results
            print(f"Model: {filename}")
            print(f"Success Rate: {success_rate}%")
            print(f"Correct Matches: {correct_matches} out of {total_questions}\n")

            # Append the results to the list for CSV
            results.append({
                'Model': filename,
                'Success Rate (%)': success_rate,
                'Correct Matches': correct_matches,
                'Total Questions': total_questions
            })

    # Save the results to a CSV file using pandas
    df = pd.DataFrame(results)
    df.to_csv(output_csv_path, index=False)

    print(f"Results saved to {output_csv_path}")

# Set the folder path, ground truth file, and output CSV file path
llm_output_path = r"D:\PyChronoBench\llm_outputs"
truth_file_path = 'pychrono_test.json'  # Path to the ground truth JSON file
output_csv_path = 'llm_results.csv'  # Path to save the CSV results

# Process all JSON files and save results to CSV
process_llm_results(llm_output_path, truth_file_path, output_csv_path)
