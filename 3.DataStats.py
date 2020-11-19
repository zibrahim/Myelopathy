import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, r2_score

from Utils import get_distribution_counts, get_distribution_percentages

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def get_deta(x,y):
    return x-y

original_data = pd.read_csv('Data/cleaned.csv')
predictors = ['eq5d_baseline','mdi_baseline_score',  'age','gender',
                        'approach',
                        'levels',
                        'diabetes',
                        'obesity',
                        'cord_signal_change',
                        'radicular'
                        ]

original_data['outcome_delta'] = [get_deta(x,y) for x, y in zip(original_data['mdi_12m_score'],
                                                                     original_data['mdi_baseline_score'])]
X = original_data[predictors]
y = original_data['outcome_delta']

X.hist()
plt.tight_layout(pad=0.4, w_pad=0.4, h_pad=1.0)
plt.savefig("Figures/DataHistogram.png")

print(X.columns)
print("Gender: ", get_distribution_counts(X['gender']),  get_distribution_percentages(X['gender']))
print("Approach: ", get_distribution_counts(X['approach']),  get_distribution_percentages(X['approach']))
print("Diabetes: ", get_distribution_counts(X['diabetes']),  get_distribution_percentages(X['diabetes']))
print("Obesity: ", get_distribution_counts(X['obesity']),  get_distribution_percentages(X['obesity']))
print("Cord Signal Change: ", get_distribution_counts(X['cord_signal_change']),
      get_distribution_percentages(X['cord_signal_change']))
print("Radicular: ", get_distribution_counts(X['radicular']),  get_distribution_percentages(X['radicular']))
