import pandas as pd
from scipy import stats

import scikit_posthocs as sp
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt  # To visualize
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from scipy.stats import norm


import sys


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


predictor_ticks = {'gender': ['Male', 'Female'],
                   'approach' : ['Posterior', 'Anterior'],
                    'levels': ['0','1','2','3','4'],
                   'diabetes': ['No', 'Yes'],
                   'obesity' : ['No', 'Yes'],
                   'cord_signal_change' : ['No', 'Yes', 'Unknown'],
                   'radicular' : ['No', 'Yes'],
                   }
predictor_labels = {'eq5d_baseline':'EQ5D\n Baseline',
                    'mdi_baseline_score': 'MDI\n Baseline',
                    'age': 'Age',
                    'gender': 'Gender',
                    'approach': 'Approach',
                    'levels': 'Levels',
                    'diabetes': 'Diabetes',
                    'obesity': 'Obesity',
                    'cord_signal_change':'Cord Signal \nChange',
                    'radicular': 'Radicular\n Pain'
                    }

data = pd.read_csv('Data/cleandedDataSE.csv')
predictors = ['eq5d_baseline','mdi_baseline_score',  'age','gender',
                        'approach',
                        'levels',
                        'diabetes',
                        'obesity',
                        'cord_signal_change',
                        'radicular'
                        ]

y = data['outcome_effect_size']
improved = data.loc[data['outcome_effect_size_binary'] == 1]
improved.columns = data.columns
X_improved = improved[predictors]

degraded = data.loc[data['outcome_effect_size_binary'] == -1]
degraded.columns = data.columns
X_degraded = degraded[predictors]
unchanged = data.loc[data['outcome_effect_size_binary'] == 0]
unchanged.columns = data.columns
X_unchanged = unchanged[predictors]

n_bins = 3
fig, axes= plt.subplots(nrows=2, ncols=5, sharey=False, sharex=False, figsize=(20,7))


for p, ax in zip(predictors, axes.flatten()):

    X = [ X_unchanged[p], X_degraded[p], X_improved[p]]

    colors = ['#5ca904', '#03719c', '#fc5a50'] #leaf green, ocean blue, coral
    labels = ["Unchanged", "Degraded","Improved"]
    ax.hist(X,density=False, histtype='bar', stacked=False, label=labels)
    if X_improved[p].nunique() <=6:
        ax.set_xticks(range(0, len(predictor_ticks[p])))
        ax.set_xticklabels(predictor_ticks[p], rotation='vertical')
    ax.set_title(predictor_labels[p])
    handles, labels = ax.get_legend_handles_labels()

fig.legend(handles, labels,
           loc="lower center",  # Position of legend
           borderaxespad=0.1,  # Small spacing around legend box
           title="Status 12 Months \n Post-Operation")
plt.subplots_adjust(right=0.85)

plt.tight_layout()
plt.tight_layout(h_pad=0.4, w_pad = 0.4, pad = 3)
plt.savefig("Figures/StackedHistogramES.png")

