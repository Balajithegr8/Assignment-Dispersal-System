import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder



data = pd.read_csv('dataset.csv')
le = LabelEncoder()
data['Assignment Subject'] = le.fit_transform(data['Assignment Subject'])
data['Difficulty'] = le.fit_transform(data['Difficulty'])
data['Due Date'] = le.fit_transform(data['Due Date'])
data['Recommended Day'] = le.fit_transform(data['Recommended Day'])
data['Feedback'] = le.fit_transform(data['Feedback'])

data['Workload'] = data['Workload'].astype(int)
data['Number of past assignments'] = data['Number of past assignments'].astype(int)
data['Current Assignments'] = data['Current Assignments'].astype(int)

# Extracting the features and labels
X = data[["Assignment Subject", "Difficulty", "Due Date", "Workload", "Number of past assignments", "Current Assignments"]]
y = data["Recommended Day"]

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating and training the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predicting the recommended day
X_predict = pd.DataFrame([[1, 1, 1, 1, 1, 1]],
                        columns=["Assignment Subject", "Difficulty", "Due Date", "Workload", "Number of past assignments", "Current Assignments"])
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
predicted_day = days[clf.predict(X_predict)[0]]
print("The recommended day is:", predicted_day)

from sklearn.model_selection import cross_val_score
scores = cross_val_score(clf, X_train, y_train, cv=5)
print("Cross-validation scores: {}".format(scores))
print("Average cross-validation score: {:.2f}".format(scores.mean()))
clf.fit(X_train, y_train)
train_score = clf.score(X_train, y_train)
print("Training Score:", train_score)
from sklearn.metrics import accuracy_score
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(acc*100))

