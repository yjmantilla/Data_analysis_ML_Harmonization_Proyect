from xml.dom.expatbuilder import ParseEscape
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import pingouin as pg
from scipy import stats
import pandas as pd
import warnings
import collections

#componentes=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
componentes_bandas=['C14_rDelta', 'C14_rTheta', 'C14_rAlpha-1', 'C14_rAlpha-2',
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
bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']

data_Comp=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas.feather')
data_Comp=data_Comp.drop(columns='index')
data_Comp['index'] = data_Comp.index
data_Comp_copy=data_Comp.copy()
databases=data_Comp['database'].unique()
controles=data_Comp[data_Comp['group']=='Control']
diccionario={}
lista_indices_com=[]
for com in componentes_bandas:
    for db in databases:
        #print(band+' '+com+ ' '+db)
        datos_db=controles[controles['database']==db]
        Q1 = np.percentile(datos_db[com], 25, interpolation = 'midpoint')
        Q3 = np.percentile(datos_db[com], 75,interpolation = 'midpoint')
        IQR = Q3 - Q1
        #print("Old Shape: ", data_Comp_copy.shape)
        dataupper=datos_db[datos_db[com] >= (Q3+1.5*IQR)]
        if dataupper.empty:
            upper=[]
        else:
            #print(dataupper)
            upper=dataupper.index.tolist()
            ''' Removing the Outliers '''
            #data_Comp_copy.drop(upper, inplace = True)
        datalower=datos_db[com][datos_db[com] <= (Q1-1.5*IQR)]
        if datalower.empty:
            lower=[]
        else:
            #print(datalower)
            lower=datalower.index.tolist()
            ''' Removing the Outliers '''
            #data_Comp_copy.drop(lower, inplace = True)
        indices=upper+lower
        diccionario[com+'_'+db]=indices
        lista_indices_com.extend(indices)
        # print(diccionario[com+'_'+db])
        # print(lista_indices_com)
        
repeticiones=collections.Counter(lista_indices_com)  
print('valor maximo que se repite un sujeto con dato atipico: ',np.max(list(repeticiones.values())))
index_to_delete=list(dict(filter(lambda x: x[1] > 8, repeticiones.items())).keys())
data_Comp_copy.drop(index_to_delete, inplace = True)
for db in databases:
    print('Base de datos '+db)
    print('Original')
    print(data_Comp[data_Comp['database']==db].shape)
    print('Despues de eliminar datos atipicos')
    print(data_Comp_copy[data_Comp_copy['database']==db].shape)
    print('Porcentaje que se elimino %',100-data_Comp_copy[data_Comp_copy['database']==db].shape[0]*100/data_Comp[data_Comp['database']==db].shape[0])
data_Comp_copy.reset_index().to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather')


datai=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
componentes=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
d_long=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'Power', 'Band', 'Component'])

for i in componentes_bandas:
    datax=datai.copy()
    datax.append(i)
    d_sep=data_Comp_copy.loc[:,datax] #Tomo las columnas que necesito 
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
d_long.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados_sin_atipicos.feather')
print('valelinda')

print('valelinda')
        #print("New Shape: ", data_Comp_copy.shape)


"""
Eliminacion de datos atipicos en el dataframe formato long, no sirve debido a que necesitamos que siempre se elimine el mismo sujeto
#Datos Componentes
data_Comp=pd.read_feather(r"Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados.feather")
data_Comp_copy=data_Comp.copy()
bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
componentes=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']

databases=data_Comp['database'].unique()
controles=data_Comp[data_Comp['group']=='Control']
for band in bandas:
    datos_band=controles[controles['Band']==band]
    for com in componentes:
        datos_com=datos_band[datos_band['Component']==com]
        for db in databases:
            #print(band+' '+com+ ' '+db)
            datos_db=datos_com[datos_com['database']==db]
            Q1 = np.percentile(datos_db['Power'], 25, interpolation = 'midpoint')
            Q3 = np.percentile(datos_db['Power'], 75,interpolation = 'midpoint')
            IQR = Q3 - Q1
            #print("Old Shape: ", data_Comp_copy.shape)
            dataupper=datos_db[datos_db['Power'] >= (Q3+1.5*IQR)]
            if dataupper.empty:
                pass 
            else:
                print(dataupper)
                upper=dataupper.index.tolist()
                ''' Removing the Outliers '''
                data_Comp_copy.drop(upper, inplace = True)
            datalower=datos_db[datos_db['Power'] <= (Q1-1.5*IQR)]
            if datalower.empty:
                pass 
            else:
                print(datalower)
                lower=datalower.index.tolist()
                ''' Removing the Outliers '''
                data_Comp_copy.drop(lower, inplace = True)
            #print("New Shape: ", data_Comp_copy.shape)

#Ver porcentaje de datos que se eliminaron por DB
databases=data_Comp['database'].unique()
for db in databases:
    print('Base de datos '+db)
    print('Orgiginal')
    print(data_Comp[data_Comp['database']==db].shape)
    print('Despues de eliminar datos atipicos')
    print(data_Comp_copy[data_Comp_copy['database']==db].shape)
    print('Porcentaje que se elimino %',100-data_Comp_copy[data_Comp_copy['database']==db].shape[0]*100/data_Comp[data_Comp['database']==db].shape[0])

#data_Comp_copy.reset_index().to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados_sin_atipicos.feather')
print('valelinda')
## datos componentes

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

bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
componentes=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
datos=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas.feather')
datos=datos.drop(columns='index')
datos['index'] = datos.index

groups=['Control', 'DTA']



##ROIs
datos=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas.feather')
datos=datos.drop(columns='index')
datos['index'] = datos.index

rois=['ROI_F_rDelta','ROI_C_rDelta', 'ROI_PO_rDelta', 'ROI_T_rDelta', 'ROI_F_rTheta',
       'ROI_C_rTheta', 'ROI_PO_rTheta', 'ROI_T_rTheta', 'ROI_F_rAlpha-1',
       'ROI_C_rAlpha-1', 'ROI_PO_rAlpha-1', 'ROI_T_rAlpha-1', 'ROI_F_rAlpha-2',
       'ROI_C_rAlpha-2', 'ROI_PO_rAlpha-2', 'ROI_T_rAlpha-2', 'ROI_F_rBeta1',
       'ROI_C_rBeta1', 'ROI_PO_rBeta1', 'ROI_T_rBeta1', 'ROI_F_rBeta2',
       'ROI_C_rBeta2', 'ROI_PO_rBeta2', 'ROI_T_rBeta2', 'ROI_F_rBeta3',
       'ROI_C_rBeta3', 'ROI_PO_rBeta3', 'ROI_T_rBeta3', 'ROI_F_rGamma',
       'ROI_C_rGamma', 'ROI_PO_rGamma', 'ROI_T_rGamma']
roi=['ROI_F', 'ROI_C','ROI_PO', 'ROI_T']
"""




