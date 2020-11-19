from numpy import mean
from numpy import var
from math import sqrt
import time
from collections import Counter
import pandas as pd
import numpy as np
#05/07/17 00:00


def get_distribution_percentages ( y_vals ) :
    y_distr = Counter(y_vals)
    y_vals_sum = sum(y_distr.values())
    return [(i, (y_distr[i] / y_vals_sum) ) for i in range(-1,np.max(y_vals) + 1)]

def get_distribution_counts ( y_vals ) :
    y_distr = Counter(y_vals)
    return [(y_distr[i]) for i in range(np.max(y_vals) + 1)]


def get_age(operation_date, birth_year):
    age = [x.year -y for  x, y in zip (operation_date, birth_year)]

    return age

def get_levels(levels_text):
    levels = [0 if pd.isnull(x)  else len(x.split('|')) for x in levels_text]
    return levels

def add_diabetes(comorbidities_column):
    diabetes = [has_illness("iabete", x) for x in comorbidities_column]
    return diabetes

def add_obesity(comorbidities_columns):
    obesity = [has_illness("besity", x) for x in comorbidities_columns]
    return obesity

def has_illness(substr, str):
    if substr in str:
        return 1
    else:
        return 0


def get_gender_int(gender_co):
    gender_co.replace('F', 1,inplace=True)
    gender_co.replace('M', 0,inplace=True)

    return gender_co


def get_approach_int(approach):
    approach.replace('Anterior ', 1,inplace=True)
    approach.replace('Posterior', 0,inplace=True)
    approach.replace('Combined Ant. and Post.', -1, inplace=True)

    return approach

def get_cord_int(col):
    col.replace('Yes', 1,inplace=True)
    col.replace('No', 0,inplace=True)

    col1 = []
    for x in col:
        if pd.isna(x):
            col1.append(2)
        else:
            col1.append(int(x))

    print(" CORD SIGNAL CHANGE: *******",col1)
    return col1

def add_radicular(symptoms):
    radicular = [has_illness("adicular", x) for x in symptoms]
    return radicular


def clean(df):
    print(" original shape: ", df.shape)
    df = df[df['eq5d_12m_date']!= "PURGED"]

    df = df[df['approach'] != -1]

    print(" final shape: ", df.shape)
    return df

def above_threshold_effect_size(x,y, t, sd):
    difference =x-y
    if (x-y)/sd >= t:
        return 1
    elif (y-x)/sd  >= t:
        return -1
    else:
        return 0


def get_effect_size(before, after):
    #difference = [x-y for x, y in zip(after, before)]
    difference = before - after
    print("difference", difference)
    mean_before = before.mean()
    print("before mean", mean_before)
    mean_after = after.mean()
    print(" after mean", mean_after)
    mean_difference = mean_before - mean_after
    print(" mean difference", mean_difference)
    sd = pd.Series(difference).std()
    print("difference sd: ", sd)
    effect_size = mean_difference/sd
    return effect_size, sd

