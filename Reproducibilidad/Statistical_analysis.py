import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from scipy import stats
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def graphic_normality_box(data,x_value,y_value,title):
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    #plt.title(title)
    sns.boxplot(x=x_value, y=y_value, data=data, ax=ax)
    sns.swarmplot(x=x_value, y=y_value, data=data, color='black', alpha = 0.5, ax=ax);
    plt.show()

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


icc_data_Roi=pd.read_csv(r'C:\Users\valec\Documents\JI\Codigos\Data_analysis_ML_Harmonization_Proyect\Reproducibilidad\ICC_values_csv\icc_values_ROIS_G2-CTR.csv',sep=';')
icc_data_Comp=pd.read_csv(r'C:\Users\valec\Documents\JI\Codigos\Data_analysis_ML_Harmonization_Proyect\Reproducibilidad\ICC_values_csv\icc_values_Components_G2-CTR.csv',sep=';')
icc_data_Roi=icc_data_Roi[icc_data_Roi['Stage']=='Normalized data']
icc_data_Comp=icc_data_Comp[icc_data_Comp['Stage']=='Normalized data']

graphic_normality_box(icc_data_Roi,'Group','ICC','ICC por grupos y Rois')
graphic_normality_box(icc_data_Comp,'Group','ICC','ICC por grupos y Componentes')

##Como anova diferencias entre grupos pero no parametrica
bands=icc_data_Comp['Bands'].unique()
print('Componentes')
for i in bands:
    print(i)
    print(pg.pairwise_gameshowell(data=icc_data_Comp[icc_data_Comp['Bands']==i], dv='ICC', between='Group'))

print('\nRois')
for i in bands:
    print(i)
    print(pg.pairwise_gameshowell(data=icc_data_Roi[icc_data_Roi['Bands']==i], dv='ICC', between='Group'))