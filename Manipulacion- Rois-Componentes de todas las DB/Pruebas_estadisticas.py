import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from scipy import stats
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

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


    '''
    return pg.normality(data=data, dv=dv, group=group,method='shapiro')
    data: pandas.DataFrame, series, list or 1D np.array
    Iterable. Can be either a single list, 1D numpy array, or a wide- or long-format pandas dataframe.

    dv: vstr (are de values)
    Dependent variable (only when data is a long-format dataframe).

    group:str
    Grouping variable (only when data is a long-format dataframe).
    '''
    

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
# If p-value<0.05 we can reject the null hypothesis that the values analyzed are equal between the groups

#All grooups
#pg.welch_anova(data=df, dv='name where are the values', between='groups to compare') 

#This function makes  two-by-two comparisons  which do not require the groups to have equal variances. It is non-parametric
#pg.pairwise_gameshowell(data=df, dv='name where are the values', between='groups to compare')


icc=['C14_rDelta', 'C14_rTheta', 'C14_rAlpha-1', 'C14_rAlpha-2',
       'C14_rBeta1', 'C14_rBeta2', 'C14_rBeta3', 'C14_rGamma', 'C15_rDelta',
       'C15_rTheta', 'C15_rAlpha-1', 'C15_rAlpha-2', 'C15_rBeta1',
       'C15_rBeta2', 'C15_rBeta3', 'C15_rGamma', 'C18_rDelta', 'C18_rTheta',
       'C18_rAlpha-1', 'C18_rAlpha-2', 'C18_rBeta1', 'C18_rBeta2',
       'C18_rBeta3', 'C18_rGamma', 'C20_rDelta', 'C20_rTheta', 'C20_rAlpha-1',
       'C20_rAlpha-2', 'C20_rBeta1', 'C20_rBeta2', 'C20_rBeta3', 'C20_rGamma',
       'C22_rDelta', 'C22_rTheta', 'C22_rAlpha-1', 'C22_rAlpha-2',
       'C22_rBeta1', 'C22_rBeta2', 'C22_rBeta3', 'C22_rGamma', 'C23_rDelta',
       'C23_rTheta', 'C23_rAlpha-1', 'C23_rAlpha-2', 'C23_rBeta1',
       'C23_rBeta2', 'C23_rBeta3', 'C23_rGamma', 'C24_rDelta', 'C24_rTheta',
       'C24_rAlpha-1', 'C24_rAlpha-2', 'C24_rBeta1', 'C24_rBeta2',
       'C24_rBeta3', 'C24_rGamma', 'C25_rDelta', 'C25_rTheta', 'C25_rAlpha-1',
       'C25_rAlpha-2', 'C25_rBeta1', 'C25_rBeta2', 'C25_rBeta3']

datos=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas.feather')
datos=datos.drop(columns='index')
datos['index'] = datos.index

for i in icc:
    print('\nDatos de '+i)
    if(datos[i].isnull().tolist()[0]==False):
        print(pg.normality(data=datos, dv=i, group='database',method='shapiro'))


print(pg.welch_anova(data=datos, dv=i, between='database'))
pg.pairwise_gameshowell(data=datos[datos['group']=='Control'], dv='C14_rDelta', between='database')

pg.welch_anova(data=datos, dv='C14_rDelta', between='database') 

# Comparaciones múltiples
