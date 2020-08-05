# -*- coding: utf-8 -*-
"""ascendum.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MHMVWHIKdEwij2p4GkkKVywrl1luAwlA
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing required libraries.
import pandas as pd
import numpy as np
import seaborn as sns #visualisation
import matplotlib.pyplot as plt #visualisation
# %matplotlib inline 
sns.set(color_codes=True)

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv('/content/drive/My Drive/Ascendeum/DataScientist_L2/Ascendeum_Dataset2.csv')
# To display the top 5 rows
data.head(5)

# To display the bottom 5 rows
data.tail(5)

# Checking the data type
data.dtypes

# Total number of rows and columns
data.shape

# Rows containing duplicate data
duplicate_rows_df = data[data.duplicated()]
print('number of duplicate rows:' , duplicate_rows_df.shape)

# Used to count the number of rows before removing the data
data.count()

# Dropping the duplicates 
data = data.drop_duplicates()
data.head(5)

# Counting the number of rows after removing duplicates.
data.count()

# Finding the null values.
print(data.isnull().sum())

def impute_na(data, variable):
    # function to fill na with a random sample
    df = data.copy()
    
    # random sampling
    df[variable+'_random'] = df[variable]
    
    # extract the random sample to fill the na
    random_sample = df[variable].dropna().sample(df[variable].isnull().sum(), random_state=0)
    
    # pandas needs to have the same index in order to merge datasets
    random_sample.index = df[df[variable].isnull()].index
    df.loc[df[variable].isnull(), variable+'_random'] = random_sample
    
    return df[variable+'_random']

data['total_revenue']=impute_na(data,'total_revenue')

df.isnull().sum()

#Q-Qplot
def diagnostic_plots(df, variable):
    # function to plot a histogram and a Q-Q plot
    # side by side, for a certain variable
    
    plt.figure(figsize=(15,6))
    plt.subplot(1, 2, 1)
    df[variable].hist()

    plt.subplot(1, 2, 2)
    stats.probplot(df[variable], dist="norm", plot=plt)

    plt.show()

#trying to check the gausian distribution
import scipy.stats as stats
diagnostic_plots(data, 'total_revenue')

#logarithmic transformation
data['Log_Fare']=np.log(data['total_revenue']+1)
diagnostic_plots(data,'Log_Fare')

#reciprocal transformation
data['Rec_Fare']=1/(data['total_revenue']+1)
diagnostic_plots(data,'Rec_Fare')

#square root transformation
data['sqr_Fare']=data['total_revenue']**(1/2)
diagnostic_plots(data,'sqr_Fare')

#exponential transformation
data['Exp_Fare']=data['total_revenue']**(1/5)
diagnostic_plots(data,'sqr_Fare')

#BoxCox tranformation
data['Fare_boxcox'], param = stats.boxcox(data.total_revenue+1) # you can vary the exponent as needed

print('Optimal lambda: ', param)

diagnostic_plots(data, 'Fare_boxcox')

import seaborn as sns
sns.relplot(x='site_id',y='total_revenue',data=df,hue='total_impressions')

sns.barplot(x='ad_type_id',y='total_revenue',data=df)

sns.barplot(x='site_id',y='total_revenue',data=df)

sns.barplot(x='total_impressions',y='total_revenue',data=df)

sns.barplot(x='viewable_impressions',y='total_revenue',data=df)

sns.barplot(x='ad_unit_id',y='total_revenue',data=df)

sns.barplot(x='order_id',y='total_revenue',data=df)

# Plotting a scatter plot
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(df['date'], df['total_revenue'])
ax.set_xlabel('date')
ax.set_ylabel('total_revenue')
plt.show()

data.head()

data.info()

y=data.iloc[:,13]
X= data.iloc[:,[1,2,6,14,12]]
print(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42,shuffle=False)

# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
model=regressor.fit(X_train, y_train)

# Predicting the Test set results
m_pred = model.predict(X_test)
r2 = model.score(X_train, y_train)
print(r2)

'''
#logestic regression
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
import keras
from keras.models import Sequential
from keras.layers import Dense
classifier = Sequential()
classifier.add(Dense(5, kernel_initializer = "uniform",activation = "relu", input_dim=5))
classifier.add(Dense(1, kernel_initializer = "uniform",activation = "sigmoid"))
classifier.compile(optimizer= "adam",loss = "binary_crossentropy",metrics = ["accuracy"])
classifier.fit(X_train, y_train, batch_size = 10, epochs = 5)'''

#multiple linear regression with cross validation
from sklearn.model_selection import cross_val_score
mregressor = LinearRegression()
model2 = cross_val_score(mregressor,X_train, y_train, scoring='neg_mean_squared_error',cv=5)

mean = np.mean(model2)
print(mean)
# Predicting the Test set results
#m_pred = model.predict(X_test)

# ridge regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import learning_curve, GridSearchCV
ridge=Ridge()
parameter ={'alpha':[1e-15, 1e-10, 1e-8, 1e-4, 1e-3,1e-2, 1, 5, 10, 20]}
ridge_regressor= GridSearchCV(ridge,parameter,scoring='neg_mean_squared_error',cv=5)
model3=ridge_regressor.fit(X_train,y_train)
print(model3.best_params_)
print(model3.best_score_)

#laso regression
from sklearn.linear_model import Lasso
from sklearn.model_selection import learning_curve, GridSearchCV
lasso=Lasso()
parameter ={'alpha':[1e-15, 1e-10, 1e-8, 1e-4, 1e-3,1e-2, 1, 5, 10, 20]}
ridge_regressor= GridSearchCV(lasso,parameter,scoring='neg_mean_squared_error',cv=5)
model4=ridge_regressor.fit(X_train,y_train)
print(model4.best_params_)
print(model4.best_score_)

#predict1= model2.predict(X_test)
predict2=model3.predict(X_test)
predict3=model4.predict(X_test)

sns.distplot(y_test-predict2)

sns.distplot(y_test-predict3)

from xgboost import plot_importance
from xgboost import XGBClassifier
from xgboost import plot_tree
model4 = XGBClassifier()
model4.fit(X_train, y_train)
plot_tree(model4)
plt.show()

def plot_features(booster, figsize):    
    fig, ax = plt.subplots(1,1,figsize=figsize)
    return plot_importance(booster=booster, ax=ax)

plot_features(model4, (10,14))

from numpy.random import normal
from numpy import mean
from numpy import std
from scipy.stats import norm
# calculate parameters
sample_mean = mean(predict2)
sample_std = std(predict2)
print('Mean=%.3f, Standard Deviation=%.3f' % (sample_mean, sample_std))

cdf=norm.cdf(predict2)
cdf.mean()

pdf=norm.pdf(predict2)
pdf.mean()

#reserve value to set
r= (1-cdf)/(pdf)
r.mean()

#maximum revenue generated
y.max()

#min revenue generated
y.min()





