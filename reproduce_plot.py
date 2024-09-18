
import matplotlib.pyplot as plt

# Data extracted from the CSV
models = ['GPT4o', 'Claude-3-sonnet', 'nemotron-340b', 'GPT4o-mini', 'Codestral-22b', 'llama3.1-405b', 'llama3.1-70b', 'llama3.1-8b', 'Gemini-1.5pro', 'Gemini-1.5flash', 'mamba-Codestral-27b', 'Gemma2-9b', 'Gemma2-27b', 'mixtral-8x22b', 'phi3-medium-128k', 'phi3-mini-128k', 'mistral-large', 'mistral-nemo-12b', 'mixtral-8x7b', 'Gemma2-2b']
success_rates = [85.0, 78.92857142857143, 78.92857142857143, 76.78571428571429, 76.78571428571429, 75.35714285714286, 74.64285714285714, 74.28571428571429, 71.78571428571429, 71.78571428571429, 71.42857142857143, 71.07142857142857, 70.35714285714286, 70.35714285714286, 70.35714285714286, 69.64285714285714, 66.78571428571428, 66.42857142857143, 65.35714285714286, 61.78571428571429]
correct_matches = [238, 221, 221, 215, 215, 211, 209, 208, 201, 201, 200, 199, 197, 197, 197, 195, 187, 186, 183, 173]
total_questions = [280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280, 280]

# Create a scatter plot with simplified LLM names
plt.figure(figsize=(10, 6))
plt.scatter(models, success_rates, color='blue', s=100,marker='x')

# Add title and labels
plt.title('LLM Performance on PyChronoBench', fontsize=16)
plt.xlabel('LLM Models', fontsize=12)
plt.ylabel('Success Rate (%)', fontsize=12)

# Rotate x labels for better readability
plt.xticks(rotation=90, fontsize=10)

# Adding grid for better readability of the plot
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.savefig("visualization.png")
plt.show()
