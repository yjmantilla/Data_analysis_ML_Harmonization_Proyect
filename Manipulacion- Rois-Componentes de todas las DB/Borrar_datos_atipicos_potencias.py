'''
Code used to delete subjects with more atypical power data by ROIs and independent components.
'''

from xml.dom.expatbuilder import ParseEscape
import pandas as pd
import numpy as np
from scipy import stats
import pandas as pd
import warnings
import collections
from Funciones import dataframe_long_roi, dataframe_long_components,estadisticos_demograficos,removing_outliers
from Funciones import columns_powers_ic
'Eliminating outliers in powers by independent components'

#Load data
path=r'C:\Users\valec\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD' 
data_Comp=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas.feather'.format(path=path))
data_Comp=data_Comp.drop(columns='index')


data_Comp_copy=removing_outliers(data_Comp,columns_powers_ic)# dataframe without outliers

#The dataframe of independent component powers is saved without atypical data
data_Comp_copy.reset_index().to_feather('{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather'.format(path=path))
print('\nFinalización de eliminación de datos atipicos de componentes')

'Eliminating outliers in powers by ROIs'
#Load data
data_roi=pd.read_feather(r'{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas.feather'.format(path=path))
data_roi=data_roi.drop(columns='index')

#Columns of interest
rois_bandas=['ROI_F_rDelta','ROI_C_rDelta', 'ROI_PO_rDelta', 'ROI_T_rDelta', 'ROI_F_rTheta',
       'ROI_C_rTheta', 'ROI_PO_rTheta', 'ROI_T_rTheta', 'ROI_F_rAlpha-1',
       'ROI_C_rAlpha-1', 'ROI_PO_rAlpha-1', 'ROI_T_rAlpha-1', 'ROI_F_rAlpha-2',
       'ROI_C_rAlpha-2', 'ROI_PO_rAlpha-2', 'ROI_T_rAlpha-2', 'ROI_F_rBeta1',
       'ROI_C_rBeta1', 'ROI_PO_rBeta1', 'ROI_T_rBeta1', 'ROI_F_rBeta2',
       'ROI_C_rBeta2', 'ROI_PO_rBeta2', 'ROI_T_rBeta2', 'ROI_F_rBeta3',
       'ROI_C_rBeta3', 'ROI_PO_rBeta3', 'ROI_T_rBeta3', 'ROI_F_rGamma',
       'ROI_C_rGamma', 'ROI_PO_rGamma', 'ROI_T_rGamma']

data_roi_copy=removing_outliers(data_roi,rois_bandas)# dataframe without outliers

#The dataframe of ROIs powers is saved without atypical data
data_roi_copy.reset_index().to_feather('{path}\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas_sin_atipicos.feather'.format(path=path))
print('\nFinalización de eliminación de datos atipicos de ROIs')


#Dataframes are saved by ROI and components for graphics.
dataframe_long_roi(data_roi_copy,'Power',columns=rois_bandas,name='Datos_ROI_formatolargo_filtrados_sin_atipicos',path=path)
dataframe_long_components(data_Comp_copy,'Power',columns=columns_powers_ic,name='Datos_componentes_formatolargo_filtrados_sin_atipicos',path=path)

#Distribucion de edad, escolaridad y educación
estadisticos_demograficos(data_Comp_copy,'componentes',path)
estadisticos_demograficos(data_roi_copy,'ROIs',path)

