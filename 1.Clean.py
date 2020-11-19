import pandas as pd
import xlrd
from scipy.stats import ttest_ind
from Utils import get_age, get_levels, add_diabetes, add_obesity, get_gender_int, get_approach_int, \
    clean, get_cord_int, add_radicular

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

original_data = pd.read_excel (r'Data/mySheet.xlsx') #place "r" before the path string to address special character, such as '\'. Don't forget to put the file name at the end of the path + '.xlsx'

cleaned_data = original_data.copy()
cleaned_data.columns =  ['pathway_id',
                        'activityDate',
                        'eq5d_baseline_date',
                        'eq5d_baseline',
                        'eq5d_12m_date',
                        'eq5d_12m',
                        'mdi_baseline_date',
                        'mdi_baseline_score',
                        'mdi_12m_date',
                        'mdi_12m_score',
                        'gender',
                        'birth_year',
                        'approach',
                        'surgery_level',
                        'symptoms',
                        'cord_signal_change',
                        'comorbidities'
                        ]


cleaned_data['age'] = get_age(cleaned_data['activityDate'], cleaned_data['birth_year'])
cleaned_data['levels'] = get_levels(cleaned_data['surgery_level'])
cleaned_data['diabetes'] = add_diabetes(cleaned_data['comorbidities'])
cleaned_data['obesity'] = add_obesity(cleaned_data['comorbidities'])
cleaned_data['gender'] = get_gender_int(cleaned_data['gender'])
cleaned_data['approach'] = get_approach_int(cleaned_data['approach'])
cleaned_data['cord_signal_change'] = get_cord_int(cleaned_data['cord_signal_change'])

print(cleaned_data.cord_signal_change)
cleaned_data['radicular'] = add_radicular(cleaned_data['symptoms'])
cleaned_data = clean(cleaned_data)



cleaned_data.to_csv("Data/cleaned.csv", index=False)
