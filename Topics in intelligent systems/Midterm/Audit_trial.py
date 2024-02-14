import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, confusion_matrix, cohen_kappa_score, roc_auc_score

# Load dataset
file_path = r'C:\Users\tebib\OneDrive\Desktop\J2\Topics in intelligent systems\Midterm\Audit_Trial4.csv'
data = pd.read_csv(file_path)

# Select the top 8 features (replace with your actual feature names)
selected_features = ['Score', 'PARA_A', 'TOTAL', 'SCORE_A', 'SCORE_B', 'District', 'PARA_B', 'MONEY_Marks']

# Separate features and target
X = data[selected_features]
y = data['Risk']  # Replace 'Risk' with your target column name

# Fill missing values
X.fillna(X.mean(), inplace=True)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the classifier
classifier = RandomForestClassifier()

# Train the classifier
classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = classifier.predict(X_test)
y_proba = classifier.predict_proba(X_test)[:, 1]  # Probabilities for AUC score

# Performance metrics
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
false_alarm_rate = fp / (fp + tn)
kappa_accuracy = cohen_kappa_score(y_test, y_pred)
specificity = tn / (tn + fp)
auc_score = roc_auc_score(y_test, y_proba)

# Print the scores
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"False Alarm Rate: {false_alarm_rate}")
print(f"Kappa-Accuracy: {kappa_accuracy}")
print(f"Specificity: {specificity}")
print(f"AUC score: {auc_score}")
