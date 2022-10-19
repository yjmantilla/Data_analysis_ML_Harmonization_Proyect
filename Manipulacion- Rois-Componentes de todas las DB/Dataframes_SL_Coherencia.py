"""Codigo para manipular los dataframes de los archivos de SL y coherencia de cada base de datos para luego usarlos para graficar"""

from cmath import nan
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display_html, display
import collections


# SL
SRM_sl=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_SRM.feather')
CHBMP_sl=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_CHBMP.feather')
BIO_sl=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_BIOMARCADORES.feather')
DUQUE_sl=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_sl_column_ROI_norm_DUQUE.feather')
#datos_sl=pd.concat([SRM,BIO,CHBMP,DUQUE]) #concatenation of data
BIO_sl['group'].replace({'G1':'Control','G2':'Control','CTR':'Control'}, inplace=True)

#Coherence
SRM_c=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_Coherence_column_norm_SRM.feather')
CHBMP_c=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_Coherence_column_norm_CHBMP.feather')
BIO_c=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_Coherence_column_norm_BIOMARCADORES.feather')
#DUQUE_c=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_Coherence_column_ROI_norm_DUQUE.feather')
BIO_c['group'].replace({'G1':'Control','G2':'Control','CTR':'Control'}, inplace=True)


#Merge con ROIS
data_roi=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas_sin_atipicos.feather')
data_roi=data_roi.drop(columns=['level_0','index'])
data_roi.reset_index(inplace=True, drop=True)

#Union por cada base de datos con los datos de roi
d_SRM=pd.merge(left=data_roi[data_roi['database']=='SRM'],right=SRM_sl)
d_SRM=pd.merge(d_SRM,SRM_c)

mergeCHBMP=data_roi[data_roi['database']=='CHBMP']
mergeCHBMP.reset_index(inplace=True, drop=True)
mergeCHBMP=mergeCHBMP.drop(['visit'], axis=1)
d_CHBMP=pd.merge(mergeCHBMP,CHBMP_sl)
d_CHBMP=pd.merge(d_CHBMP,CHBMP_c)

mergeBIO=data_roi[data_roi['database']=='BIOMARCADORES']
mergeBIO.reset_index(inplace=True, drop=True)
d_BIO=pd.merge(mergeBIO,BIO_sl)
d_BIO=pd.merge(d_BIO,BIO_c)

mergeDUQUE=data_roi[data_roi['database']=='DUQUE']
mergeDUQUE.reset_index(inplace=True, drop=True)
mergeDUQUE=mergeDUQUE.drop(['visit'], axis=1)
DUQUE_sl=DUQUE_sl.drop(['group'], axis=1)
d_DUQUE=pd.merge(mergeDUQUE,DUQUE_sl)
#DUQUE_c=DUQUE_c.drop(['group'], axis=1)
#d_DUQUE=pd.merge(d_DUQUE,DUQUE_c)

d_B_roi=pd.concat([d_SRM,d_BIO,d_DUQUE,d_CHBMP])#Union de todos los dataframes tiene potencias por rois, coherencia, sl

#Manipulacion d elos dataframes para hacer los graficos 
rois_bandas=['ROI_F_rDelta','ROI_C_rDelta', 'ROI_PO_rDelta', 'ROI_T_rDelta', 'ROI_F_rTheta',
       'ROI_C_rTheta', 'ROI_PO_rTheta', 'ROI_T_rTheta', 'ROI_F_rAlpha-1',
       'ROI_C_rAlpha-1', 'ROI_PO_rAlpha-1', 'ROI_T_rAlpha-1', 'ROI_F_rAlpha-2',
       'ROI_C_rAlpha-2', 'ROI_PO_rAlpha-2', 'ROI_T_rAlpha-2', 'ROI_F_rBeta1',
       'ROI_C_rBeta1', 'ROI_PO_rBeta1', 'ROI_T_rBeta1', 'ROI_F_rBeta2',
       'ROI_C_rBeta2', 'ROI_PO_rBeta2', 'ROI_T_rBeta2', 'ROI_F_rBeta3',
       'ROI_C_rBeta3', 'ROI_PO_rBeta3', 'ROI_T_rBeta3', 'ROI_F_rGamma',
       'ROI_C_rGamma', 'ROI_PO_rGamma', 'ROI_T_rGamma']
roi=['ROI_F', 'ROI_C','ROI_PO', 'ROI_T']
datai=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
d_long=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'Power', 'Band', 'ROI'])

SL=['SL_ROI_F_Delta', 'SL_ROI_C_Delta', 'SL_ROI_PO_Delta', 'SL_ROI_T_Delta',
       'SL_ROI_F_Theta', 'SL_ROI_C_Theta', 'SL_ROI_PO_Theta', 'SL_ROI_T_Theta',
       'SL_ROI_F_Alpha-1', 'SL_ROI_C_Alpha-1', 'SL_ROI_PO_Alpha-1',
       'SL_ROI_T_Alpha-1', 'SL_ROI_F_Alpha-2', 'SL_ROI_C_Alpha-2',
       'SL_ROI_PO_Alpha-2', 'SL_ROI_T_Alpha-2', 'SL_ROI_F_Beta1',
       'SL_ROI_C_Beta1', 'SL_ROI_PO_Beta1', 'SL_ROI_T_Beta1', 'SL_ROI_F_Beta2',
       'SL_ROI_C_Beta2', 'SL_ROI_PO_Beta2', 'SL_ROI_T_Beta2', 'SL_ROI_F_Beta3',
       'SL_ROI_C_Beta3', 'SL_ROI_PO_Beta3', 'SL_ROI_T_Beta3', 'SL_ROI_F_Gamma',
       'SL_ROI_C_Gamma', 'SL_ROI_PO_Gamma', 'SL_ROI_T_Gamma']
coherence=['Coherence_Delta', 'Coherence_Theta', 'Coherence_Alpha-1',
       'Coherence_Alpha-2', 'Coherence_Beta1', 'Coherence_Beta2',
       'Coherence_Beta3', 'Coherence_Gamma']
for i in rois_bandas:
    datax=datai.copy()
    datax.append(i)
    d_sep=d_B_roi.loc[:,datax] #Tomo las columnas que necesito 
    for j in bandas:
        if j in i:
            band=j
    for c in roi:
        if c in i:
            r=c
    d_sep['Band']=[band]*len(d_sep)
    d_sep['ROI']=[r]*len(d_sep)
    d_sep= d_sep.rename(columns={i:'Power'})
    d_long=d_long.append(d_sep,ignore_index = True) #Uno el dataframe 
d_long['ROI']=d_long['ROI'].replace({'ROI_':''}, regex=True)#Quito el _ y lo reemplazo con '' 

#d_long.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_ROI_formatolargo_filtrados_sin_atipicos.feather')
d_sl=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'SL', 'Band', 'ROI'])

for i in SL:
    datax=datai.copy()
    datax.append(i)
    d_sep=d_B_roi.loc[:,datax] #Tomo las columnas que necesito 
    for j in bandas:
        if j in i:
            band=j
    for c in roi:
        if c in i:
            r=c
    d_sep['Band']=[band]*len(d_sep)
    d_sep['ROI']=[r]*len(d_sep)
    d_sep= d_sep.rename(columns={i:'SL'})
    d_sl=d_sl.append(d_sep,ignore_index = True) #Uno el dataframe 
d_sl['ROI']=d_sl['ROI'].replace({'ROI_':''}, regex=True)#Quito el _ y lo reemplazo con '' 
d_sl.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_SL_desdeunionpotencias_roi.feather')

d_c=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'Coherence', 'Band'])

for i in coherence:
    datax=datai.copy()
    datax.append(i)
    d_sep=d_B_roi.loc[:,datax] #Tomo las columnas que necesito 
    for j in bandas:
        if j in i:
            band=j
    # for c in roi:
    #     if c in i:
    #         r=c
    d_sep['Band']=[band]*len(d_sep)
    #d_sep['ROI']=[r]*len(d_sep)
    d_sep= d_sep.rename(columns={i:'Coherence'})
    d_c=d_c.append(d_sep,ignore_index = True) #Uno el dataframe 

d_c.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_COHERENCE_desdeunionpotencias_roi.feather')

#Merge con componentes

data_Comp=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather')
data_Comp=data_Comp.drop(columns=['level_0','index'])
data_Comp.reset_index(inplace=True, drop=True)
data_Comp_copy=data_Comp.copy()

#Union por cada base de datos con los datos de componentes
d_SRM=pd.merge(left=data_Comp[data_Comp['database']=='SRM'],right=SRM_sl)
d_SRM=pd.merge(d_SRM,SRM_c)

mergeCHBMP=data_Comp[data_Comp['database']=='CHBMP']
mergeCHBMP.reset_index(inplace=True, drop=True)
mergeCHBMP=mergeCHBMP.drop(['visit'], axis=1)
d_CHBMP=pd.merge(mergeCHBMP,CHBMP_sl)
d_CHBMP=pd.merge(d_CHBMP,CHBMP_c)

mergeBIO=data_Comp[data_Comp['database']=='BIOMARCADORES']
mergeBIO.reset_index(inplace=True, drop=True)
d_BIO=pd.merge(mergeBIO,BIO_sl)
d_BIO=pd.merge(d_BIO,BIO_c)

mergeDUQUE=data_Comp[data_Comp['database']=='DUQUE']
mergeDUQUE.reset_index(inplace=True, drop=True)
mergeDUQUE=mergeDUQUE.drop(['visit'], axis=1)
#DUQUE_sl=DUQUE_sl.drop(['group'], axis=1)
d_DUQUE=pd.merge(mergeDUQUE,DUQUE_sl)
#DUQUE_c=DUQUE_c.drop(['group'], axis=1)
#d_DUQUE=pd.merge(d_DUQUE,DUQUE_c)

d_B_com=pd.concat([d_SRM,d_BIO,d_DUQUE,d_CHBMP])#Union de todos los dataframes

#Manipulacion de los dataframes para hacer los graficos

datai=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
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
       'C25_rAlpha-2', 'C25_rBeta1', 'C25_rBeta2', 'C25_rBeta3','C25_rGamma']
componentes=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
d_long=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'Power', 'Band', 'Component'])

for i in icc:
    datax=datai.copy()
    datax.append(i)
    d_sep=d_B_com.loc[:,datax] #Tomo las columnas que necesito 
    for j in bandas:
        if j in i:
            band=j
    for c in componentes:
        if c in i:
            componente=c
    d_sep['Band']=[band]*len(d_sep)
    d_sep['Component']=[componente]*len(d_sep)
    d_sep= d_sep.rename(columns={i:'Power'})
    d_long=d_long.append(d_sep,ignore_index = True) #Uno el dataframe 
d_sl=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'SL', 'Band', 'ROI'])

for i in SL:
    datax=datai.copy()
    datax.append(i)
    d_sep=d_B_com.loc[:,datax] #Tomo las columnas que necesito 
    for j in bandas:
        if j in i:
            band=j
    for c in roi:
        if c in i:
            r=c
    d_sep['Band']=[band]*len(d_sep)
    d_sep['ROI']=[r]*len(d_sep)
    d_sep= d_sep.rename(columns={i:'SL'})
    d_sl=d_sl.append(d_sep,ignore_index = True) #Uno el dataframe 
d_sl['ROI']=d_sl['ROI'].replace({'ROI_':''}, regex=True)#Quito el _ y lo reemplazo con '' 
d_sl.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_SL_desdeunionpotencias_Componentes.feather')

d_c=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'Coherence', 'Band'])

for i in coherence:
    datax=datai.copy()
    datax.append(i)
    d_sep=d_B_com.loc[:,datax] #Tomo las columnas que necesito 
    for j in bandas:
        if j in i:
            band=j
    # for c in roi:
    #     if c in i:
    #         r=c
    d_sep['Band']=[band]*len(d_sep)
    #d_sep['ROI']=[r]*len(d_sep)
    d_sep= d_sep.rename(columns={i:'Coherence'})
    d_c=d_c.append(d_sep,ignore_index = True) #Uno el dataframe 

d_c.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_para_graficos_COHERENCE_desdeunionpotencias_componentes.feather')

print('valelinda')