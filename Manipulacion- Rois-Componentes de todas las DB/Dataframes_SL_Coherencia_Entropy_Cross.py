"""
Code to manipulate the dataframes of the SL, coherence, entropy and cross frequency files
of each database and then use them for graphing.
 """

from cmath import nan
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display_html, display
import collections

path=r'C:\Users\valec\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD' #Cambia dependieron de quien lo corra

"Load data"

# SL Dataframes
SRM_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_column_ROI_norm_SRM.feather'.format(path=path))
CHBMP_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_column_ROI_norm_CHBMP.feather'.format(path=path))
BIO_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_column_ROI_norm_BIOMARCADORES.feather'.format(path=path))
DUQUE_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_column_ROI_norm_DUQUE.feather'.format(path=path))

#Coherence Dataframes
SRM_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Coherence_column_norm_SRM.feather'.format(path=path))
CHBMP_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Coherence_column_norm_CHBMP.feather'.format(path=path))
BIO_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Coherence_column_norm_BIOMARCADORES.feather'.format(path=path))
DUQUE_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Coherence_column_norm_DUQUE.feather'.format(path=path))

#Entropy Dataframes
DUQUE_e=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Entropy_column_norm_DUQUE.feather'.format(path=path))

#Cross frequency Dataframes
DUQUE_cr=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Cross_Frequency_column_norm_DUQUE.feather'.format(path=path))

#Power data by ROIs with demographic data
data_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas_sin_atipicos.feather'.format(path=path))
data_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas.feather'.format(path=path))
data_roi=data_roi.drop(columns=['index'])
#data_roi=data_roi.drop(columns=['level_0','index'])
data_roi.reset_index(inplace=True, drop=True)

#Independent component power data with demographic data
data_Comp=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather'.format(path=path))
data_Comp=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas.feather'.format(path=path))
data_Comp=data_Comp.drop(columns=['index'])
#data_Comp=data_Comp.drop(columns=['level_0','index']) va este
data_Comp.reset_index(inplace=True, drop=True)


'''The power data by ROIs is merged with the demographic data, 
first merged for each database and then all the databases are concatenated'''

#SRM
d_SRM=pd.merge(left=data_roi[data_roi['database']=='SRM'],right=SRM_sl)
d_SRM=pd.merge(d_SRM,SRM_c)
#CHBMP
mergeCHBMP=data_roi[data_roi['database']=='CHBMP']
mergeCHBMP.reset_index(inplace=True, drop=True)
mergeCHBMP=mergeCHBMP.drop(['visit'], axis=1)
d_CHBMP=pd.merge(mergeCHBMP,CHBMP_sl)
d_CHBMP=pd.merge(d_CHBMP,CHBMP_c)
#BIOMARCADORES
mergeBIO=data_roi[data_roi['database']=='BIOMARCADORES']
mergeBIO.reset_index(inplace=True, drop=True)
d_BIO=pd.merge(mergeBIO,BIO_sl)
d_BIO=pd.merge(d_BIO,BIO_c)
#DUQUE
mergeDUQUE=data_roi[data_roi['database']=='DUQUE']
mergeDUQUE.reset_index(inplace=True, drop=True)
mergeDUQUE=mergeDUQUE.drop(['visit'], axis=1)
DUQUE_sl=DUQUE_sl.drop(['group'], axis=1)
d_DUQUE=pd.merge(mergeDUQUE,DUQUE_sl)
DUQUE_c=DUQUE_c.drop(['group'], axis=1)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_c)
DUQUE_e=DUQUE_e.drop(['group'], axis=1)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_e)
DUQUE_cr=DUQUE_cr.drop(['group'], axis=1)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_cr)

"Data concatenation: The dataframe contains power columns for ROIs, SL, coherence, entropy, cross frequency, etc"
d_B_roi=pd.concat([d_SRM,d_BIO,d_DUQUE,d_CHBMP])


'''The power data by independet components is merged with the demographic data, 
first merged for each database and then all the databases are concatenated'''

#SRM
d_SRM=pd.merge(left=data_Comp[data_Comp['database']=='SRM'],right=SRM_sl)
d_SRM=pd.merge(d_SRM,SRM_c)
#CHBMP
mergeCHBMP=data_Comp[data_Comp['database']=='CHBMP']
mergeCHBMP.reset_index(inplace=True, drop=True)
mergeCHBMP=mergeCHBMP.drop(['visit'], axis=1)
d_CHBMP=pd.merge(mergeCHBMP,CHBMP_sl)
d_CHBMP=pd.merge(d_CHBMP,CHBMP_c)
#BIOMARCADORES
mergeBIO=data_Comp[data_Comp['database']=='BIOMARCADORES']
mergeBIO.reset_index(inplace=True, drop=True)
d_BIO=pd.merge(mergeBIO,BIO_sl)
d_BIO=pd.merge(d_BIO,BIO_c)
#DUQUE
mergeDUQUE=data_Comp[data_Comp['database']=='DUQUE']
mergeDUQUE.reset_index(inplace=True, drop=True)
mergeDUQUE=mergeDUQUE.drop(['visit'], axis=1)
d_DUQUE=pd.merge(mergeDUQUE,DUQUE_sl)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_c)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_e)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_cr)

"Data concatenation: The dataframe contains power columns for independent components, SL, coherence, entropy, cross frequency, etc"
d_B_com=pd.concat([d_SRM,d_BIO,d_DUQUE,d_CHBMP])#Union de todos los dataframes


"""Conversion of dataframes to perform the different SL, coherence, entropy, cross frequency, etc. graphs"""



#Sl columns
SL=['SL_ROI_F_Delta', 'SL_ROI_C_Delta', 'SL_ROI_PO_Delta', 'SL_ROI_T_Delta',
       'SL_ROI_F_Theta', 'SL_ROI_C_Theta', 'SL_ROI_PO_Theta', 'SL_ROI_T_Theta',
       'SL_ROI_F_Alpha-1', 'SL_ROI_C_Alpha-1', 'SL_ROI_PO_Alpha-1',
       'SL_ROI_T_Alpha-1', 'SL_ROI_F_Alpha-2', 'SL_ROI_C_Alpha-2',
       'SL_ROI_PO_Alpha-2', 'SL_ROI_T_Alpha-2', 'SL_ROI_F_Beta1',
       'SL_ROI_C_Beta1', 'SL_ROI_PO_Beta1', 'SL_ROI_T_Beta1', 'SL_ROI_F_Beta2',
       'SL_ROI_C_Beta2', 'SL_ROI_PO_Beta2', 'SL_ROI_T_Beta2', 'SL_ROI_F_Beta3',
       'SL_ROI_C_Beta3', 'SL_ROI_PO_Beta3', 'SL_ROI_T_Beta3', 'SL_ROI_F_Gamma',
       'SL_ROI_C_Gamma', 'SL_ROI_PO_Gamma', 'SL_ROI_T_Gamma']

#Coherence columns
coherence=['Coherence_Delta', 'Coherence_Theta', 'Coherence_Alpha-1',
       'Coherence_Alpha-2', 'Coherence_Beta1', 'Coherence_Beta2',
       'Coherence_Beta3', 'Coherence_Gamma']

#Entropy columns    
entropy=['Entropy_ROI_F_Delta',
       'Entropy_ROI_C_Delta', 'Entropy_ROI_PO_Delta', 'Entropy_ROI_T_Delta',
       'Entropy_ROI_F_Theta', 'Entropy_ROI_C_Theta', 'Entropy_ROI_PO_Theta',
       'Entropy_ROI_T_Theta', 'Entropy_ROI_F_Alpha-1', 'Entropy_ROI_C_Alpha-1',
       'Entropy_ROI_PO_Alpha-1', 'Entropy_ROI_T_Alpha-1',
       'Entropy_ROI_F_Alpha-2', 'Entropy_ROI_C_Alpha-2',
       'Entropy_ROI_PO_Alpha-2', 'Entropy_ROI_T_Alpha-2',
       'Entropy_ROI_F_Beta1', 'Entropy_ROI_C_Beta1', 'Entropy_ROI_PO_Beta1',
       'Entropy_ROI_T_Beta1', 'Entropy_ROI_F_Beta2', 'Entropy_ROI_C_Beta2',
       'Entropy_ROI_PO_Beta2', 'Entropy_ROI_T_Beta2', 'Entropy_ROI_F_Beta3',
       'Entropy_ROI_C_Beta3', 'Entropy_ROI_PO_Beta3', 'Entropy_ROI_T_Beta3',
       'Entropy_ROI_F_Gamma', 'Entropy_ROI_C_Gamma', 'Entropy_ROI_PO_Gamma',
       'Entropy_ROI_T_Gamma']

#Cross frequency columns
cross=['Cross_ROI_F_Delta','Cross_ROI_C_Delta', 'Cross_ROI_PO_Delta', 'Cross_ROI_T_Delta',
       'Cross_ROI_F_Theta', 'Cross_ROI_C_Theta', 'Cross_ROI_PO_Theta',
       'Cross_ROI_T_Theta', 'Cross_ROI_F_Alpha-1', 'Cross_ROI_C_Alpha-1',
       'Cross_ROI_PO_Alpha-1', 'Cross_ROI_T_Alpha-1', 'Cross_ROI_F_Alpha-2',
       'Cross_ROI_C_Alpha-2', 'Cross_ROI_PO_Alpha-2', 'Cross_ROI_T_Alpha-2',
       'Cross_ROI_F_Beta1', 'Cross_ROI_C_Beta1', 'Cross_ROI_PO_Beta1',
       'Cross_ROI_T_Beta1', 'Cross_ROI_F_Beta2', 'Cross_ROI_C_Beta2',
       'Cross_ROI_PO_Beta2', 'Cross_ROI_T_Beta2', 'Cross_ROI_F_Beta3',
       'Cross_ROI_C_Beta3', 'Cross_ROI_PO_Beta3', 'Cross_ROI_T_Beta3',
       'Cross_ROI_F_Gamma', 'Cross_ROI_C_Gamma', 'Cross_ROI_PO_Gamma',
       'Cross_ROI_T_Gamma']


def dataframe_long_roi(data,type,columns,name,path):
    '''Function used to convert a dataframe to be used for graphing by ROIs'''
    #demographic data and neuropsychological test columns
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    columns_df=data_dem+[type, 'Band', 'ROI']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands
    bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
    #ROIs 
    roi=['ROI_F', 'ROI_C','ROI_PO', 'ROI_T']

    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                band=j
        for c in roi:
            if c in i:
                r=c
        d_sep['Band']=[band]*len(d_sep)
        d_sep['ROI']=[r]*len(d_sep)
        d_sep= d_sep.rename(columns={i:type})
        data_new=data_new.append(d_sep,ignore_index = True) #Uno el dataframe 
    data_new['ROI']=data_new['ROI'].replace({'ROI_':''}, regex=True)#Quito el _ y lo reemplazo con '' 
    data_new=data_new[data_new['database']=='DUQUE']
    data_new.reset_index().to_feather('{path}\Datosparaorganizardataframes\{name}.feather'.format(path=path,name=name))
    print('Dataframe para graficos de {type} guardado'.format(type=type))

def dataframe_long_coherence(data,type='Coherence',columns=None,name=None,path=None):
    '''Function used to convert a dataframe to be used for graphing.'''
    #demographic data and neuropsychological test columns
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    columns_df=data_dem+[type, 'Band', 'ROI']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands
    bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']

    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                band=j
        d_sep['Band']=[band]*len(d_sep)
        d_sep= d_sep.rename(columns={i:type})
        data_new=data_new.append(d_sep,ignore_index = True) #Uno el dataframe 
    data_new=data_new[data_new['database']=='DUQUE']
    data_new.reset_index().to_feather('{path}\Datosparaorganizardataframes\{name}.feather'.format(path=path,name=name))
    print('Dataframe para graficos de {type} guardado'.format(type=type))

#New dataframes from ROIs
#SL
dataframe_long_roi(d_B_roi,type='SL',columns=SL,name="Datos_para_graficos_SL_desdeunionpotencias_roi",path=path)
#Coherencia
dataframe_long_coherence(d_B_roi,type='Coherence',columns=coherence,name="Datos_para_graficos_COHERENCE_desdeunionpotencias_roi",path=path)
#Entropia
dataframe_long_roi(d_B_roi,type='Entropy',columns=entropy,name="Datos_para_graficos_ENTROPY_desdeunionpotencias_roi",path=path)
#Cross frequency
dataframe_long_roi(d_B_roi,type='Cross_Frequency',columns=cross,name="Datos_para_graficos_CROSS_Frequency_desdeunionpotencias_roi",path=path)

#New dataframes from Independent components
#SL
dataframe_long_roi(d_B_com,type='SL',columns=SL,name="Datos_para_graficos_SL_desdeunionpotencias_Componentes",path=path)
#Coherencia
dataframe_long_coherence(d_B_com,type='Coherence',columns=coherence,name="Datos_para_graficos_COHERENCE_desdeunionpotencias_componentes",path=path)
#Entropia
dataframe_long_roi(d_B_com,type='Entropy',columns=entropy,name="Datos_para_graficos_ENTROPY_desdeunionpotencias_componentes",path=path)
#Cross frequency
dataframe_long_roi(d_B_com,type='Cross_Frequency',columns=cross,name="Datos_para_graficos_CROSS_Frequency_desdeunionpotencias_components",path=path)


