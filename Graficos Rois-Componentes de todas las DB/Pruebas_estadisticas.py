import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from scipy import stats
import pandas as pd

'''Graphical analysis'''
def graphic_normality_box(data,x_value,y_value):
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    sns.boxplot(x=x_value, y=y_value, data=data, ax=ax)
    sns.swarmplot(x=x_value, y=y_value, data=data, color='black', alpha = 0.5, ax=ax);

'''Normality tests'''

#Shapiro-Wilk Test
def normality_Shapiro(data,name_data):
    '''data: data to test
    name_data: name of data to analyze
    '''
    stat,p=stats.shapiro(data)
    print('Shapiro normality test for '+name_data+'\n')
    print('stat=%.3f, p=%.3f' % (stat,p))
    if p>0.05:
        print("Probably Gaussian\n")
    else:
        print("Probably not Gaussian\n")

def normality_N_groups_Shapiro(data,dv,group,method='shapiro'):
    '''
    data: pandas.DataFrame, series, list or 1D np.array
    Iterable. Can be either a single list, 1D numpy array, or a wide- or long-format pandas dataframe.

    dv: vstr (are de values)
    Dependent variable (only when data is a long-format dataframe).

    group:str
    Grouping variable (only when data is a long-format dataframe).
    '''
    pg.normality(data=data, dv=dv, group=group,method=method)

#D’Agostino’s K-squared test
def normality_Agostino(data,name_data):
    '''data: data to test
    name_data: name of data to analyze
    '''
    stat,p=stats.normaltest(data)
    print('D’Agostino’s K-squared normality test for '+name_data+'\n')
    print('stat=%.3f, p=%.3f' % (stat,p))
    if p>0.05:
        print("Probably Gaussian\n")
    else:
        print("Probably not Gaussian\n")

#Test de homocedasticidad

def normality_N_groups_Shapiro(data,dv,group):
    '''
    Test equality of variance

    data:pandas.DataFrame, list or dict
    Iterable. Can be either a list / dictionnary of iterables or a wide- or long-format pandas dataframe.

    dv:str
    Dependent variable (only when data is a long-format dataframe).

    group:str
    Grouping variable (only when data is a long-format dataframe).

    Returns
    statspandas.DataFrame
    'W/T': Test statistic (‘W’ for Levene, ‘T’ for Bartlett)
    'pval': p-value
    'equal_var': True if data has equal variance
    '''
    pg.homoscedasticity(data=data, dv=dv, group=group, method='levene')

'''Anova'''
#Therefore, it is recommended to use a Welch ANOVA instead, followed by Games-Howell post-hoc tests, 
# which do not require the groups to have equal variances.
# If d-value<0.05 we can reject the null hypothesis that the values analyzed are equal between the groups

#All grooups
#pg.welch_anova(data=df, dv='name where are the values', between='groups to compare') 

#This function makes  two-by-two comparisons  which do not require the groups to have equal variances. It is non-parametric
#pg.pairwise_gameshowell(data=df, dv='name where are the values', between='groups to compare')