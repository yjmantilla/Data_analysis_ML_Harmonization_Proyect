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
from Funciones import dataframe_long_roi,dataframe_long_components,dataframe_componentes_deseadas,dataframe_long_cross
from Funciones import columns_SL_roi,columns_coherence_roi,columns_entropy_rois,columns_cross_rois
from Funciones import columns_SL_ic,columns_coherence_ic,columns_entropy_ic,columns_cross_ic

path=r'C:\Users\valec\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD' #Cambia dependieron de quien lo corra

"Load data"

#Data by ROIs with demographic data

#Power
data_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas_sin_atipicos.feather'.format(path=path))
data_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas.feather'.format(path=path))
data_roi=data_roi.drop(columns=['index'])
#data_roi=data_roi.drop(columns=['level_0','index'])
data_roi.reset_index(inplace=True, drop=True)

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

"Load data"
#Independent component data with demographic data

#Power
data_Comp=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather'.format(path=path))
data_Comp=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas.feather'.format(path=path))
data_Comp=data_Comp.drop(columns=['index'])
#data_Comp=data_Comp.drop(columns=['level_0','index']) va este
data_Comp.reset_index(inplace=True, drop=True)

# SL Dataframes
# SRM_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_column_ROI_norm_SRM.feather'.format(path=path))
# CHBMP_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_column_ROI_norm_CHBMP.feather'.format(path=path))
# BIO_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_column_ROI_norm_BIOMARCADORES.feather'.format(path=path))
DUQUE_sl=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_sl_columns_components_DUQUE.feather'.format(path=path))
DUQUE_sl=dataframe_componentes_deseadas(DUQUE_sl,columnas=['participant_id'])

#Coherence Dataframes
# SRM_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Coherence_column_norm_SRM.feather'.format(path=path))
# CHBMP_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Coherence_column_norm_CHBMP.feather'.format(path=path))
# BIO_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_Coherence_column_norm_BIOMARCADORES.feather'.format(path=path))
DUQUE_c=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_cohfreq_columns_components_DUQUE.feather'.format(path=path))
DUQUE_c=dataframe_componentes_deseadas(DUQUE_c,columnas=['participant_id'])
#Entropy Dataframes
DUQUE_e=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_entropy_columns_components_DUQUE.feather'.format(path=path))
DUQUE_e=dataframe_componentes_deseadas(DUQUE_e,columnas=['participant_id'])
#Cross frequency Dataframes
DUQUE_cr=pd.read_feather(r'{path}\Datosparaorganizardataframes\data_crossfreq_columns_components_DUQUE.feather'.format(path=path))
DUQUE_cr=dataframe_componentes_deseadas(DUQUE_cr,columnas=['participant_id'])

columns_cross_ic=DUQUE_cr.columns.tolist()
columns_cross_ic.remove('participant_id')
'''The power data by independet components is merged with the demographic data, 
first merged for each database and then all the databases are concatenated'''

# #SRM
# d_SRM=pd.merge(left=data_Comp[data_Comp['database']=='SRM'],right=SRM_sl)
# d_SRM=pd.merge(d_SRM,SRM_c)
# #CHBMP
# mergeCHBMP=data_Comp[data_Comp['database']=='CHBMP']
# mergeCHBMP.reset_index(inplace=True, drop=True)
# mergeCHBMP=mergeCHBMP.drop(['visit'], axis=1)
# d_CHBMP=pd.merge(mergeCHBMP,CHBMP_sl)
# d_CHBMP=pd.merge(d_CHBMP,CHBMP_c)
# #BIOMARCADORES
# mergeBIO=data_Comp[data_Comp['database']=='BIOMARCADORES']
# mergeBIO.reset_index(inplace=True, drop=True)
# d_BIO=pd.merge(mergeBIO,BIO_sl)
# d_BIO=pd.merge(d_BIO,BIO_c)
#DUQUE
mergeDUQUE=data_roi[data_roi['database']=='DUQUE']
mergeDUQUE.reset_index(inplace=True, drop=True)

d_DUQUE=pd.merge(mergeDUQUE,DUQUE_sl)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_c)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_e)
d_DUQUE=pd.merge(d_DUQUE,DUQUE_cr)

"Data concatenation: The dataframe contains power columns for independent components, SL, coherence, entropy, cross frequency, etc"
d_B_com=d_DUQUE
#d_B_com=pd.concat([d_SRM,d_BIO,d_DUQUE,d_CHBMP])#Union de todos los dataframes

"""Conversion of dataframes to perform the different SL, coherence, entropy, cross frequency, etc. graphs"""

#New dataframes from ROIs
#SL
dataframe_long_roi(d_B_roi,type='SL',columns=columns_SL_roi,name="Datos_para_graficos_SL_desdeunionpotencias_roi",path=path)
#Coherencia
#dataframe_long_roi(d_B_roi,type='Coherence',columns=columns_coherence_roi,name="Datos_para_graficos_COHERENCE_desdeunionpotencias_roi",path=path)
#Entropia
dataframe_long_roi(d_B_roi,type='Entropy',columns=columns_entropy_rois,name="Datos_para_graficos_ENTROPY_desdeunionpotencias_roi",path=path)
#Cross frequency
#dataframe_long_roi(d_B_roi,type='Cross_Frequency',columns=columns_cross_rois,name="Datos_para_graficos_CROSS_Frequency_desdeunionpotencias_roi",path=path)

#New dataframes from Independent components
#SL
dataframe_long_components(d_B_com,type='SL',columns=columns_SL_ic,name="Datos_para_graficos_SL_desdeunionpotencias_Componentes",path=path)
#Coherencia
dataframe_long_components(d_B_com,type='Coherence',columns=columns_coherence_ic,name="Datos_para_graficos_COHERENCE_desdeunionpotencias_componentes",path=path)
#Entropia
dataframe_long_components(d_B_com,type='Entropy',columns=columns_entropy_ic,name="Datos_para_graficos_ENTROPY_desdeunionpotencias_componentes",path=path)
#Cross frequency
dataframe_long_cross(d_B_com,type='Cross Frequency',columns=columns_cross_ic,name="Datos_para_graficos_CROSS_Frequency_desdeunionpotencias_components",path=path)



