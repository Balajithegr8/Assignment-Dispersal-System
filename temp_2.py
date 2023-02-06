import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Load the csv file into a pandas DataFrame
df = pd.read_csv('dataset_new.csv')
le = LabelEncoder()
df['Difficulty'] = le.fit_transform(df['Difficulty'])

# Split the data into features (X) and target (y)
X = df.drop(columns=['Due Date'])
y = df['Due Date']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Use the trained model to predict the due date for a new sample
new_sample = pd.DataFrame({
    'Difficulty': [2],
    'Workload': [1],
    'Assigned date': [2]
})
new_prediction = model.predict(new_sample)
print("Predicted due date:", new_prediction)
