import os
import json
import numpy as np
import pandas as pd
import sqlite3
import functools as ft
import matplotlib.pyplot as plt
#%matplotlib inline

# reading the Excel file into Python
loans = pd.read_excel('Loan data for BI - excel.xlsx')
print(loans)

# how many nulls we have
print(loans.isnull().sum())

# showing the dimension of the data
print(loans.shape)

# how many NA we have
print(loans.isna().sum())

# clearing the NA
loans.dropna(inplace=True)
print(loans)

# how many NA we have
print(loans.isna().sum())

# top 5 lines in the data
print(loans.head())

# drop column ID from the data
loans.drop(columns=["ID"], inplace=True)
print(loans)

# remove duplicates in data
loans.drop_duplicates(inplace=True)
print(loans)

# find rows including words
errors = loans["Dependents"].str.extract(pat='(\w+)', expand=False)
errors

# "NOT" = ~
errors[~errors.isna()]

# remove rows including words
loans.drop(errors[~errors.isna()].index, inplace=True)
loans

# how many duplicates we have
loans.duplicated().sum()

# one-hot-vector on  Married column
pd.get_dummies(loans, columns=["Married"])

# data types
loans.dtypes

# create a plot
loans["Loan_Amount"].plot(kind="box")

# creating quantiles based on Age & Loan_Amount
outliers = loans[['Age', 'Loan_Amount']]

Q1 = outliers['Loan_Amount'].quantile(0.25)
Q3 = outliers['Loan_Amount'].quantile(0.75)

IQR = Q3 - Q1

# TUKEY: bandwidth: 1.5 outliers --> far...far...far..
bandwidth = 2.5

max_value = Q3 + bandwidth * IQR
min_value = Q1 - bandwidth * IQR

outliers = outliers[(outliers['Loan_Amount'] > max_value) | (outliers['Loan_Amount'] < min_value)]
outliers



