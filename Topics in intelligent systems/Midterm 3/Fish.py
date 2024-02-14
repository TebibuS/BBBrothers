import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
file_path = 'C:/Users/tebib/OneDrive/Desktop/J2/Topics in intelligent systems/Midterm 3/seeds.csv'
data = pd.read_csv(file_path, delimiter=',')

# Assuming 'Type' is the class column, replace it with the actual name of your class column
X = data.drop('Type', axis=1)
y = data['Type']

# Standardize the feature space
X_standardized = StandardScaler().fit_transform(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_standardized, y, test_size=0.2, random_state=42)

# Train SVM without PCA
svm_classifier = SVC()
svm_classifier.fit(X_train, y_train)
y_pred = svm_classifier.predict(X_test)
print("SVM Classification report without PCA:")
print(classification_report(y_test, y_pred))

# Apply PCA to reduce dimensions to 3 features
pca = PCA(n_components=3)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Train SVM with PCA-transformed data
svm_classifier_pca = SVC()
svm_classifier_pca.fit(X_train_pca, y_train)
y_pred_pca = svm_classifier_pca.predict(X_test_pca)
print("SVM Classification report with PCA:")
print(classification_report(y_test, y_pred_pca))

# Comparing accuracy
accuracy_without_pca = accuracy_score(y_test, y_pred)
accuracy_with_pca = accuracy_score(y_test, y_pred_pca)

print(f'Accuracy without PCA: {accuracy_without_pca}')
print(f'Accuracy with PCA: {accuracy_with_pca}')
