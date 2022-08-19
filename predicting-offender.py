#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings('ignore')

data = pd.read_csv('static/traffic_violaions.csv')
data.drop(['country_name', 'search_type', "driver_race"], axis=1, inplace=True)
data.drop('driver_age_raw', axis=1, inplace=True)
data = data.dropna(how='any')
data['stop_year'] = data['stop_date'].apply(lambda x: int(x.split('/')[2]))
data['stop_month'] = data['stop_date'].apply(lambda x: int(x.split('/')[0]))
data['stop_day'] = data['stop_date'].apply(lambda x: int(x.split('/')[1]))
data.drop('stop_date', axis=1, inplace=True)
data['stop_time'] = data['stop_time'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60)
data['driver_gender'] = data['driver_gender'].map({'M': 1, 'F': 0})
data.drop('stop_time', axis=1, inplace=True)

data['violation'] = data['violation_raw'].apply(lambda x: x)
data.drop(['violation_raw'], axis=1, inplace=True)
data['search_conducted'] = data['search_conducted'].apply(lambda x: 1 if x == True else 0)
data.rename({'violation': 'Offense', 'is_arrested': 'Offender'}, axis=1, inplace=True)
data['Offender'] = data['Offender'].apply(lambda x: 'Offender' if x == True else "Not an Offennder")
data.drop('stop_duration', axis=1, inplace=True)
data['drugs_related_stop'] = data['drugs_related_stop'].apply(lambda x: 1 if x == True else 0)

data.drop('stop_outcome', axis=1, inplace=True)

temp = pd.get_dummies(data['Offense'], drop_first=False)
data = pd.concat([data, temp], axis=1)
data.drop('Offense', axis=1, inplace=True)

data['number_booked'] = np.random.randint(0, 5, size=len(data))

data.rename({'Equipment/Inspection Violation': 'EIV', 'Motorist Assist/Courtesy': 'MAC',
             'Speeding': 'SPD', 'Call for Service': 'CFS', 'Other Traffic Violation': 'OTV',
             'Registration Violation': 'RV',
             'Special Detail/Directed Patrol': 'SDDP', 'Violation of City/Town Ordinance': 'VCTO',
             'Suspicious Person': 'SP'},
            axis=1, inplace=True)
data.drop(['APB', 'CFS', "MAC", 'SDDP', 'VCTO', 'Warrant'], axis=1, inplace=True)

# ### Spliting the dataset into training and testing and creating the X component and the y component
from sklearn.model_selection import train_test_split

X = data.drop('Offender', axis=1)
y = data['Offender']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=100)
X_train.head()

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# print(accuracy)
print(y_pred)

import pickle

pickle.dump(classifier, open("model.pkl", "wb"))
