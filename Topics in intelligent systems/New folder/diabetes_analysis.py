import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load the dataset
csv_file_path = r'C:\Users\tebib\OneDrive\Desktop\J2\Topics in intelligent systems\New folder\pima-indians-diabetes_edited (1).csv'
dataset = pd.read_csv(csv_file_path, header=None)

# Replace missing values
dataset.replace([0, 99999], np.nan, inplace=True)
dataset.fillna(dataset.mean(), inplace=True)

# Standardize Plasma glucose concentration (#2) and Diastolic blood pressure (#3)
mean_glucose = dataset[1].mean()
std_glucose = dataset[1].std()
mean_bp = dataset[2].mean()
std_bp = dataset[2].std()

dataset[1] = (dataset[1] - mean_glucose) / std_glucose
dataset[2] = (dataset[2] - mean_bp) / std_bp

# Splitting the dataset
X = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVM Classifier
classifier = SVC(kernel='linear', random_state=42)
classifier.fit(X_train, y_train)

# Evaluate the model
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy after standardization: {accuracy}')
