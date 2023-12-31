# -*- coding: utf-8 -*-
"""Birth_Rate_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oKdIn8CnHwFKNY4FXSThxDxhgIgbcfZG

# **DS Project - Birth Rate Analysis**

# ----> Importing Libraries
"""

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor

"""# ---> Data Collection and Processing"""

df = pd.read_csv("births.csv")

df.head()

df.shape

df.info()

df.describe()

#to display categorical values -> extracts object data type
df.describe(include ="O")

df.isnull().sum()

df = df.dropna(axis=0)
df.shape

df['day'] = df['day'].astype(int)  #we set the day column to integers; previously it had been a string because some columns in the dataset contained the value 'null':
df['decade'] = 10 * (df['year'] // 10)
df.pivot_table('births', index='decade', columns='gender', aggfunc='sum')

"""We immediately see that male births outnumber female births in every decade. To see this trend a bit more clearly, we can use the built-in plotting tools in Pandas to visualize the total number of births by year

# ---> Viewing Total number of birth per year
"""

birth_decade = df.pivot_table('births', index='year', columns='gender', aggfunc='sum')
birth_decade.plot()
plt.ylabel("Total births per year")
plt.show()

"""we can immediately see the annual trend in births by gender. By eye, it appears that over the past 50 years male births have outnumbered female births by around 5%.

# ---> Further Data Exploration
We must start by cleaning the data a bit, removing outliers caused by mistyped dates (e.g., June 31st) or missing values (e.g., June 99th). One easy way to remove these all at once is to cut outliers
"""

quartiles = np.percentile(df['births'], [25, 50, 75])
mu = quartiles[1]
print(quartiles[0],quartiles[2])
sigma = np.std(df['births'])

birth_decade = df.pivot_table('births', index='day', columns='gender', aggfunc='sum')
birth_decade.plot()
plt.ylabel("Average births per day")
plt.show()

df = df.query('(births > @mu- 3* @sigma) & (births < @mu + 3* @sigma)')

birth_decade = df.pivot_table('births', index='day', columns='gender', aggfunc='sum')
birth_decade.plot()
plt.ylabel("Average births per day")
plt.show()

df.index = pd.to_datetime(10000*df.year + 100*df.month + df.day, format='%Y%m%d') #we can combine the day, month, and year to create a Date index
print(df.index)
df['day of week'] = df.index.dayofweek

"""# ---> Plotting births by weekday for several decades"""

df_day = df.pivot_table('births', index='day of week',
                                columns='decade', aggfunc='mean')
df_day.index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
df_day.plot()
plt.ylabel("Average Births by Day")
plt.show()

"""Apparently births are slightly less common on weekends than on weekdays"""

df_month = df.pivot_table('births', [df.index.month, df.index.day])
print(df_month.head())

df_month.index = [pd.datetime(1904, month, day) for (month, day) in df_month.index]
print(df_month.head())

fig, ax = plt.subplots(figsize=(12, 4))
df_month.plot(ax=ax)
plt.show()

"""In particular, the striking feature of this graph is the dip in birthrate on US holidays (e.g., Independence Day (4th-July), Labor Day(1st Monday September), Thanksgiving (4th Thursday November), Christmas (25 December), New Year's Day(1st January)) although this likely reflects trends in scheduled/induced births rather than some deep psychosomatic effect on natural births.

# Correlation:
# 1. Positive Correlation
# 2. Negative Correlation
"""

correlation = df.corr()

"""
**Constructing heatmap to understand correlation**"""

plt.figure(figsize=(6,6))
sns.heatmap(correlation, cbar=True , square=True, fmt='.1f', annot=True, annot_kws={'size':6}, cmap='PuBuGn')

#correlation values of births
print(correlation['births'])

"""**Checking the distribution of the Births**"""

sns.displot(df['births'],color='green')

"""# ---> Splitting Features and Targets"""

X = df.drop(['births','gender'],axis=1)
Y = df['births']

print(X)

print(Y)

"""# ---> Splitting into Training data and Testing data"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3,random_state=2)

"""# Model Training :
# 1) Linear Regression
# 2) Random Forest

# Linear Regression
"""

lin_reg_model = LinearRegression()

lin_reg_model.fit(X_train,Y_train)

"""**Model Evaluation**"""

training_data_prediction = lin_reg_model.predict(X_train)

error_score = metrics.r2_score(Y_train, training_data_prediction)
print("R squared Error : ", error_score)

Y_train = list(Y_train)

plt.plot(Y_train, color = 'blue' , label="Actual Birth rate")
plt.plot(Y_train, color = 'green' , label="Predicted Birth rate")
plt.xlabel("Actual Birth rate")
plt.ylabel("Predicted Birth rate")
plt.title(" Actual birth rate vs Predicted birth rate")
plt.legend()
plt.show()

test_data_prediction = lin_reg_model.predict(X_test)

error_score = metrics.r2_score(Y_test, test_data_prediction)
print("R squared Error : ", error_score)

Y_test = list(Y_test)

plt.plot(Y_test, color='blue', label = "Actual birth rate")
plt.plot(test_data_prediction, color='green', label = "Predicted birth rate")
plt.xlabel("Actual Birth rate")
plt.ylabel("Predicted Birth Rate")
plt.title(" Actual Birth rate vs Predicted Birth rate")
plt.legend()
plt.show()

"""# Random Forest"""

regressor = RandomForestRegressor(n_estimators=100)

regressor.fit(X_train,Y_train)

test_data_prediction1 = regressor.predict(X_test)
print(test_data_prediction1)

error_score= metrics.r2_score(Y_test,test_data_prediction1)

print("R Squared error = ",error_score)

Y_test = list(Y_test)

plt.plot(Y_test, color='blue', label = "Actual birth rate")
plt.plot(test_data_prediction1, color='green', label = "Predicted birth rate")
plt.xlabel("Actual Birth rate")
plt.ylabel("Predicted Birth Rate")
plt.title(" Actual Birth rate vs Predicted Birth rate")
plt.legend()
plt.show()
