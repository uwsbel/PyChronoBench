import json
import csv
import pandas as pd
import re

import re


import re

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

        # 1. Double Bracket Pattern: [[B]]
        match = double_bracket_pattern.search(output)
        if match:
            correct_answer = match.group(1)
        else:
            # 2. Bold Pattern: **B. ...**
            match = bold_pattern.search(output)
            if match:
                correct_answer = match.group(1)
            else:
                # 3. Single Quote Pattern: 'B. ...'
                match = single_quote_pattern.search(output)
                if match:
                    correct_answer = match.group(1)
                else:
                    # 4. Bold and Quoted Pattern: **'B. ...'**
                    match = bold_quoted_pattern.search(output)
                    if match:
                        correct_answer = match.group(1)
                    else:
                        # 5. Traditional Pattern: B. ...
                        match = traditional_pattern.match(output)
                        if match:
                            correct_answer = match.group(1)
                        else:
                            # 6. Special Case with Quotes: B. '...'
                            match = special_case_pattern.search(output)
                            if match:
                                correct_answer = match.group(1)
                            else:
                                # 7. Fallback: Any standalone A., B., C., D.
                                match = fallback_pattern.search(output)
                                if match:
                                    correct_answer = match.group(1)

        correct_answers.append(correct_answer)

    return correct_answers



# Function to calculate success rate
def calculate_success_rate(json_file_1, json_file_2):
    # Extract answers from both JSON files
    correct_answers_1 = extract_correct_answers(json_file_1)  # User's answers
    print(correct_answers_1)
    correct_answers_2 = extract_correct_answers(json_file_2)  # Correct solutions
    print(correct_answers_2)
    # Compare the answers and calculate the number of matches
    total_questions = len(correct_answers_1)
    correct_matches = sum(1 for ans1, ans2 in zip(correct_answers_1, correct_answers_2) if ans1 == ans2)

    # Calculate success rate as a percentage
    success_rate = (correct_matches / total_questions) * 100
    return success_rate, correct_matches, total_questions

#load the ground truth data
with open('pychrono_test.json', 'r', encoding='utf-8') as file:
    truth = json.load(file)
with open('pychrono_test_base.json', 'r', encoding='utf-8') as file:
    base = json.load(file)
with open('pychrono_test_finetuned1.json', 'r', encoding='utf-8') as file:
    trained = json.load(file)
#with open('pychrono_test_result2.json', 'r', encoding='utf-8') as file:
#    trained2 = json.load(file)
# Calculate success rate for both base and trained results compared to the truth
base_success_rate, base_correct_matches, base_total_questions = calculate_success_rate(truth, base)
trained_success_rate, trained_correct_matches, trained_total_questions = calculate_success_rate(truth, trained)
#trained2_success_rate, trained2_correct_matches, trained2_total_questions = calculate_success_rate(truth, trained2)

# Display the results
print(f"Base Model Success Rate: {base_success_rate}%")
print(f"Base Model Correct Matches: {base_correct_matches} out of {base_total_questions}")
print(f"Trained Model Success Rate: {trained_success_rate}%")
print(f"Trained Model Correct Matches: {trained_correct_matches} out of {trained_total_questions}")
#print(f"Trained Model 2 Success Rate: {trained2_success_rate}%")
#print(f"Trained Model 2 Correct Matches: {trained2_correct_matches} out of {trained2_total_questions}")
