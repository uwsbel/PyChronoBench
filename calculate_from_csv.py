import os
import json
import re
import pandas as pd
# Function to calculate success rate based on manually corrected CSV files
def calculate_success_rate_from_csv(llm_csv_folder, output_csv_path):
    results = []

    # Iterate over all CSV files in the specified folder
    for filename in os.listdir(llm_csv_folder):
        if filename.endswith(".csv"):
            model_path = os.path.join(llm_csv_folder, filename)
            try:
                # Try reading the CSV with utf-8 encoding
                df = pd.read_csv(model_path, encoding='utf-8')
            except UnicodeDecodeError:
                # If there's an encoding error, try reading with latin-1
                print(f"UnicodeDecodeError for {filename}, trying 'latin-1' encoding.")
                df = pd.read_csv(model_path, encoding='latin-1')

            # Compare extracted answers with correct answers
            correct_matches = sum(df['Correct Answer'] == df['Extracted Answer'])
            total_questions = len(df)
            success_rate = (correct_matches / total_questions) * 100 if total_questions else 0

            # Print the success rate
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

    # Save the success rate results to a CSV file using pandas
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_csv_path, index=False)

    print(f"Success rates saved to {output_csv_path}")

# Set the folder path for the manually corrected CSVs and the output CSV path
llm_csv_folder = r"D:\PyChronoBench\llm_csv"  # Folder containing the manually corrected CSV files
output_csv_path = 'success_rates.csv'  # Path to save the success rate results

# Calculate success rates from CSV files
calculate_success_rate_from_csv(llm_csv_folder, output_csv_path)
