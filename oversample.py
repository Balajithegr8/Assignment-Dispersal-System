from imblearn.over_sampling import SMOTE
import pandas as pd
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler

# read in the data
data = pd.read_csv("dataset.csv")
le = LabelEncoder()
data['Assignment Subject'] = le.fit_transform(data['Assignment Subject'])
data['Difficulty'] = le.fit_transform(data['Difficulty'])
data['Due Date'] = le.fit_transform(data['Due Date'])
data['Recommended Day'] = le.fit_transform(data['Recommended Day'])
data['Feedback'] = le.fit_transform(data['Feedback'])

data['Workload'] = data['Workload'].astype(int)
data['Number of past assignments'] = data['Number of past assignments'].astype(int)
data['Current Assignments'] = data['Current Assignments'].astype(int)


X = data.drop(columns=['Recommended Day'])
y = data['Recommended Day']

ros = RandomOverSampler(sampling_strategy=0.5, random_state=42)
X_resampled, y_resampled = ros.fit_resample(X, y)

# Number of rows in oversampled data
print(X_resampled.shape[0])

