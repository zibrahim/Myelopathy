import pandas as pd
from scipy import stats

import scikit_posthocs as sp
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt  # To visualize
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from scipy.stats import norm, ttest_ind

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


predictors = ['eq5d_baseline','mdi_baseline_score',  'age','gender',
                        'approach',
                        'levels',
                        'diabetes',
                        'obesity',
                        'cord_signal_change',
                        'radicular'
                        ]

categories = {'gender': ['Male', 'Female'],
                   'approach' : ['Posterior', 'Anterior'],
                    'levels': ['0','1','2','3','4'],
                   'diabetes': ['No', 'Yes'],
                   'obesity' : ['No', 'Yes'],
                   'cord_signal_change' : ['No', 'Yes', 'Unknown'],
                   'radicular' : ['No', 'Yes'],
                   }

data = pd.read_csv('Data/cleandedDataSE.csv')

cols = data.columns
imp_mean = IterativeImputer(random_state=0)
imp_mean.fit(data[predictors])
data[predictors] = imp_mean.transform(data[predictors])
data.columns = cols

y = data['outcome_effect_size']
y_binary = data['outcome_effect_size_binary']
improved = data.loc[data['outcome_effect_size_binary'] == 1]
improved.columns = data.columns
degraded = data.loc[data['outcome_effect_size_binary'] == -1]
degraded.columns = data.columns
unchanged = data.loc[data['outcome_effect_size_binary'] == 0]
unchanged.columns = data.columns

o= open("Figures/StatisticalSignificanceES.txt", "w")
print("***************************************** Overall ********************************************", file=o)

print("\t Improved: ", len(improved), "(", "{:.2f}".format(len(improved)/len(data)), "%)",
      "\t degraded: ", len(improved), "(", "{:.2f}".format(len(degraded)/len(data)), "%)",
      "\t unchanged: ", len(unchanged), "(", "{:.2f}".format(len(unchanged)/len(data)), "%)", file=o)
print("**********************************************************************************************\n ", file=o)

for p in predictors:
    p_improved = improved[p]
    p_degraded = degraded[p]
    p_unchanged = unchanged[p]
    test_data = [p_improved, p_degraded, p_unchanged]

    ######plot stacked bar

    labels = ['Improved', 'Degraded', 'Unchanged']
    print("********************", p, "***********************", file=o)
    n = p_improved.unique()
    if len(n) <=6 and p !='mdi_baseline_score':
        for i in n:
            cat_i = [x for x in p_improved if x ==i]
            print(" \t\t Improved - Category: ", categories[p][int(i)], "num patients: ", len(cat_i), file=o)

    n = p_degraded.unique()
    if len(n) <=6  and p !='mdi_baseline_score':
        for i in n:
            cat_i = [x for x in p_degraded if x ==i]
            print(" \t\t Degraded - Category: ",categories[p][int(i)], "num patients: ", len(cat_i), file=o)

    n = p_unchanged.unique()
    if len(n) <=6  and p !='mdi_baseline_score':
        for i in n:
            cat_i = [x for x in p_unchanged if x ==i]
            print(" \t\t Unchanged - Category: ", categories[p][int(i)], "num patients: ", len(cat_i), file=o)

    print("Kruskal-Wallis:", stats.kruskal(p_improved, p_degraded, p_unchanged), file =o)
    print("One-way Annova:", stats.f_oneway(p_improved, p_degraded, p_unchanged), file =o)
    print("Dunn's Post-Hoc Test", file=o)
    print(sp.posthoc_dunn(test_data, p_adjust='bonferroni'), file =o)
    print("\nT-test: +Ve vs -Ve:", ttest_ind(p_improved, p_degraded), file =o)
    print("Dunn's Post-Hoc Test of only +Ve vs -Ve", file=o)
    test_small = [p_improved, p_degraded]
    print(sp.posthoc_dunn(test_small, p_adjust='bonferroni'), file =o)




    print("\n", file=o)

o.close()