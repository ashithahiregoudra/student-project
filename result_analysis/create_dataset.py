import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Create a synthetic dataset
num_samples = 100  # Number of samples
data = {
    'user_id': range(1, num_samples + 1),  # User IDs from 1 to 100
    'course_interest': np.random.choice(['Python', 'Java', 'Web Development', 'Data Science'], num_samples),
    'hours_spent': np.random.randint(1, 20, size=num_samples),  # Random hours between 1 and 20
    'completed': np.random.choice([0, 1], num_samples),  # Randomly completed or not
    'recommended': np.random.choice(['Machine Learning', 'Web Development', 'Data Science', 'Cybersecurity'], num_samples)
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file_path = 'student_data.csv'
df.to_csv(csv_file_path, index=False)

print(f"Dataset saved to {csv_file_path}")