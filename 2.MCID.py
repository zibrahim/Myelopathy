import pandas as pd
from scipy.stats import ttest_ind

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

from Utils import  above_threshold_effect_size, get_distribution_percentages, get_effect_size

data = pd.read_csv("Data/cleaned.csv")

cleaned_data = data.copy()

mdi_before = cleaned_data['mdi_baseline_score']
mdi_after = cleaned_data['mdi_12m_score']
mdi_delta = mdi_after - mdi_before
mean_mdi_delta = mdi_delta.mean()

x = ttest_ind(mdi_before , mdi_after , equal_var=False)
tstatstic = x.statistic
pvalue = x.pvalue
effect_size, sd= get_effect_size(mdi_before, mdi_after)
print(" EFFECT SIZE: ", effect_size)

cleaned_data['outcome_effect_size'] = [(y-x)/sd for x, y in zip(mdi_before, mdi_after)]
cleaned_data['outcome_effect_size_binary'] = [above_threshold_effect_size(x,y, effect_size, sd) for x, y in zip(mdi_before, mdi_after)]

print(" outcome distribution using Cohen-D ", get_distribution_percentages(cleaned_data['outcome_effect_size_binary']))

cleaned_data.to_csv("Data/cleandedDataSE.csv", index=False)