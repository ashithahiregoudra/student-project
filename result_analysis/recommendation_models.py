# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


csv_file_path = 'student_data.csv'
df = pd.read_csv(csv_file_path)


# Encoding categorical features
le_course = LabelEncoder()
le_recommend = LabelEncoder()

df['course_interest_encoded'] = le_course.fit_transform(df['course_interest'])
df['recommended_encoded'] = le_recommend.fit_transform(df['recommended'])

# Features and target
X = df[['course_interest_encoded', 'hours_spent', 'completed']]
y = df['recommended_encoded']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# Define models with predefined hyperparameters
models = {
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=7),
    'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=2, random_state=42),
    'Support Vector Machine': SVC(C=1, kernel='rbf'),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=300, learning_rate=0.05, max_depth=5, min_samples_split=5, subsample=1.0, random_state=42)
}

results = []

# Loop through each model for training and evaluation
for name, model in models.items():
    # Perform cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy')
    cross_val_accuracy = np.mean(cv_scores)  # Average cross-validation accuracy

    # Train the model on the full training set
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)  # Make predictions
    test_accuracy = accuracy_score(y_test, y_pred)  # Calculate test accuracy
    
    results.append({
        'Model': name,
        'Cross-Validation Accuracy': round(cross_val_accuracy, 2),
        'Test Accuracy': round(test_accuracy, 2)
    })

    # Print model performance
    print(f"--- {name} ---")
    print(f"Cross-Validation Accuracy: {round(cross_val_accuracy, 2)}")
    print(f"Test Accuracy: {test_accuracy:.2f}")
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples')
    plt.title(f'Confusion Matrix - {name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(f'confusion_matrix_{name.replace(" ", "_")}.png')  # Save in the current directory
    plt.close()


# Convert results to DataFrame and save
results_df = pd.DataFrame(results)
results_df.to_csv('final_model_comparison_table.csv', index=False)  # Save in the current directory

# Plot accuracy comparison
plt.figure(figsize=(10, 6))
sns.barplot(data=results_df, x='Model', y='Test Accuracy', palette='mako')
plt.title('Model Accuracy Comparison')
plt.ylabel('Accuracy')
plt.ylim(0, 1.1)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('final_model_accuracy_comparison.png')  # Save in the current directory
plt.close()

print("Model comparison completed. Outputs saved.")
