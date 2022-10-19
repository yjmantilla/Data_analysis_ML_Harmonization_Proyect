"""Codigo para manipular los dataframes de los archivos de SL y coherencia de cada base de datos para luego usarlos para graficar"""

from cmath import nan
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display_html, display
import collections


# SL
SRM=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_SRM.feather')
CHBMP=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_CHBMP.feather')
BIO=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_BIOMARCADORES.feather')
DUQUE=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_DUQUE.feather')
#datos_sl=pd.concat([SRM,BIO,CHBMP,DUQUE]) #concatenation of data

#Merge con ROIS
data_roi=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas_sin_atipicos.feather')

data_roi=data_roi.drop(columns=['level_0','index'])
data_roi.reset_index(inplace=True, drop=True)
#union_sl=pd.merge(data_roi,datos_sl)
#Merge con componentes

data_Comp=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather')
data_Comp=data_Comp.drop(columns=['level_0','index'])
data_Comp.reset_index(inplace=True, drop=True)
data_Comp_copy=data_Comp.copy()

CHBMP_c=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_Coherence_column_norm_CHBMP.feather')
print('valelinda')