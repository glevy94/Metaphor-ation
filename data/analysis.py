import pandas as pd

file_path = 'ratings3.csv'
try:
    ratings = pd.read_csv(file_path, encoding='utf-8')  # Default attempt
except UnicodeDecodeError:
    ratings = pd.read_csv(file_path, encoding='latin1')  # Alternative encoding
print(ratings.head())

# Output rating metrics for each model
model_stats = ratings.groupby('model_name').agg({'Rating': ['mean', 'std', lambda x: x.max() - x.min(), 'min', 'max']})
model_stats.columns = ['Average Rating', 'Standard Deviation', 'Range', 'Minimum Rating', 'Maximum Rating']
model_stats = model_stats.sort_values('Average Rating', ascending=False)

print(model_stats)

output_file = 'model_stats3.csv'
model_stats.to_csv(output_file)

# Average the ratings by difficulty 
ratings.columns = ['model_name', 'input_sentence', 'generated_output', 'Rating', 'Explanation']
ratings['Rating'] = pd.to_numeric(ratings['Rating'], errors='coerce')
ratings['starts_with_the'] = ratings['input_sentence'].str.startswith("The", na=False)

grouped_averages = (
    ratings.groupby(['model_name', 'starts_with_the'])['Rating']
    .mean()
    .unstack(fill_value=0)
    .reset_index()
)
grouped_averages.columns = ['model_name', 'average_rating_not_the', 'average_rating_with_the']

print(grouped_averages)
grouped_averages.to_csv("model_name_with_the_analysis2.csv", index=False)
