from xml.dom.expatbuilder import ParseEscape
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd
import warnings
import collections
import dataframe_image as dfi

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

for db in databases:
    datos_db=controles[controles['database']==db] #Datos de una sola base de datos
    indices_db=[]
    for com in componentes_bandas:
        #print(band+' '+com+ ' '+db)
        Q1 = np.percentile(datos_db[com], 25, interpolation = 'midpoint')
        Q3 = np.percentile(datos_db[com], 75,interpolation = 'midpoint')
        IQR = Q3 - Q1 
        #print("Old Shape: ", data_Comp_copy.shape)
        dataupper=datos_db[datos_db[com] >= (Q3+1.5*IQR)]#Valores atipicos superiores
        if dataupper.empty:
            upper=[]
        else:
            #print(dataupper)
            upper=dataupper.index.tolist() #lista de indices del dataframe que son valores atipicos
            ''' Removing the Outliers '''
            #data_Comp_copy.drop(upper, inplace = True)
        datalower=datos_db[datos_db[com] <= (Q1-1.5*IQR)]#Valores atipicos inferiores
        if datalower.empty:
            lower=[]
        else:
            #print(datalower)
            lower=datalower.index.tolist()#lista de indices del dataframe que son valores atipicos
            ''' Removing the Outliers '''
            #data_Comp_copy.drop(lower, inplace = True)
        indices=upper+lower #union de upper y lower de indices del dataframe que son valores atipicos
        #lista_indices_com.extend(indices)
        indices_db.extend(indices) #Se tiene una lista de indices por cada base de datos
  
    #diccionario[db]=indices_db
    repeticiones=collections.Counter(indices_db) #Diccionario que contiene cuantas veces un indice(sujeto) tiene un dato atipico, en una banda de una componente
    bandera=True
    #print("\n"+db)
    i=2
    while(bandera):#Mientras no se encuentre el porcentaje de perdida requerido
        i+=1 #se aumenta cada que se entra al while
        data_Comp_prueba=data_Comp.copy()#  copia de data frame para no borrar datos del dataframe original,se crea cada que se entra al while
        index_to_delete=list(dict(filter(lambda x: x[1] > i, repeticiones.items())).keys()) # se crea una lista de los indices cuyas repeticiones de datos atipicos es mayor a i
        data_Comp_prueba.drop(index_to_delete, inplace = True)#Se borran los indices del dataframe de prueba para saber el porcentaje de datos borrados
        porcentaje=100-data_Comp_prueba[data_Comp_prueba['database']==db].shape[0]*100/data_Comp[data_Comp['database']==db].shape[0]#porcentaje de datos borrados
        if porcentaje<=5:
            #Si el procentaje borrado por primera vez es menor o igual a 5, se borra del dataframe copia los indices que dan el resultado deseado
            data_Comp_copy.drop(index_to_delete, inplace = True)
            bandera=False #se cambia la bandera para que no entre mas al while
            #print(porcentaje)
       


#Para observar un resumen de los datos antes y despues de eliminar sujetos con mayor cantidad de datos atipicos

for db in databases:
    print('\nBase de datos '+db)
    print('Original')
    print(data_Comp[data_Comp['database']==db].shape)
    print('Despues de eliminar datos atipicos')
    print(data_Comp_copy[data_Comp_copy['database']==db].shape)
    print('Porcentaje que se elimino %',100-data_Comp_copy[data_Comp_copy['database']==db].shape[0]*100/data_Comp[data_Comp['database']==db].shape[0])
data_Comp_copy.drop(columns='index')
data_Comp_copy.reset_index().to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather')
print('\nFinalización de eliminación de datos atipicos de componentes')

#Ver edad, educacion y genero
#link de ayuda
#https://pandas.pydata.org/docs/user_guide/indexing.html
# https://kanoki.org/2022/07/25/pandas-select-slice-rows-columns-multiindex-dataframe/
#Base de datos general
datos_estadisticos=data_Comp_copy.groupby(['group']).describe(include='all')
table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
dfi.export(table, 'Manipulacion- Rois-Componentes de todas las DB\Tablas_datos\Tabla_edad_escolaridad_sexo_todasBD_componentes.png')
print(data_Comp_copy.groupby(['group']).describe().loc[:,['age','education']])#Medice solo el promedio pero por grupo de tda la base de datos
#print(data_Comp_copy.loc[:,['sex','group']].groupby(['sex','group']).size() )
#Por cada base de datos
datos_estadisticos=data_Comp_copy.groupby(['group','database']).describe(include='all')
print(datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]])
table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
dfi.export(table, 'Manipulacion- Rois-Componentes de todas las DB\Tablas_datos\Tabla_edad_escolaridad_sexo_separadoBD_componentes.png')

#Se crea el dataframe en formato long a partir del dataframe sin atipicos, para hacer los graficos

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



# Eliminación de datos atipicos por ROIs
data_roi=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas.feather')
data_roi=data_roi.drop(columns='index')
data_roi['index'] = data_roi.index

rois_bandas=['ROI_F_rDelta','ROI_C_rDelta', 'ROI_PO_rDelta', 'ROI_T_rDelta', 'ROI_F_rTheta',
       'ROI_C_rTheta', 'ROI_PO_rTheta', 'ROI_T_rTheta', 'ROI_F_rAlpha-1',
       'ROI_C_rAlpha-1', 'ROI_PO_rAlpha-1', 'ROI_T_rAlpha-1', 'ROI_F_rAlpha-2',
       'ROI_C_rAlpha-2', 'ROI_PO_rAlpha-2', 'ROI_T_rAlpha-2', 'ROI_F_rBeta1',
       'ROI_C_rBeta1', 'ROI_PO_rBeta1', 'ROI_T_rBeta1', 'ROI_F_rBeta2',
       'ROI_C_rBeta2', 'ROI_PO_rBeta2', 'ROI_T_rBeta2', 'ROI_F_rBeta3',
       'ROI_C_rBeta3', 'ROI_PO_rBeta3', 'ROI_T_rBeta3', 'ROI_F_rGamma',
       'ROI_C_rGamma', 'ROI_PO_rGamma', 'ROI_T_rGamma']



data_roi_copy=data_roi.copy()
databases=data_roi['database'].unique()
controles=data_roi[data_roi['group']=='Control']
diccionario_roi={}
lista_indices_roi=[]
for db in databases:
    datos_db=controles[controles['database']==db]
    indices_db=[]
    for r in rois_bandas:
        #print(band+' '+com+ ' '+db)
        
        Q1 = np.percentile(datos_db[r], 25, interpolation = 'midpoint')
        Q3 = np.percentile(datos_db[r], 75,interpolation = 'midpoint')
        IQR = Q3 - Q1
        #print("Old Shape: ", data_Comp_copy.shape)
        dataupper=datos_db[datos_db[r] >= (Q3+1.5*IQR)]
        if dataupper.empty:
            upper=[]
        else:
            #print(dataupper)
            upper=dataupper.index.tolist()
            ''' Removing the Outliers '''
            #data_Comp_copy.drop(upper, inplace = True)
        datalower=datos_db[datos_db[r] <= (Q1-1.5*IQR)]
        if datalower.empty:
            lower=[]
        else:
            #print(datalower)
            lower=datalower.index.tolist()
            ''' Removing the Outliers '''
            #data_Comp_copy.drop(lower, inplace = True)
        indices=upper+lower
        #lista_indices_roi.extend(indices)
        indices_db.extend(indices)
  
    #diccionario[db]=indices_db
    repeticiones=collections.Counter(indices_db)
    bandera=True
    #print("\n"+db)
    i=2
    while(bandera):
        i+=1
        data_roi_prueba=data_roi.copy()
        index_to_delete=list(dict(filter(lambda x: x[1] > i, repeticiones.items())).keys())
        data_roi_prueba.drop(index_to_delete, inplace = True)
        porcentaje=100-data_roi_prueba[data_roi_prueba['database']==db].shape[0]*100/data_roi[data_roi['database']==db].shape[0]
        if porcentaje<=5:
            data_roi_copy.drop(index_to_delete, inplace = True)
            bandera=False
            #print(porcentaje)
    
       
        
# repeticiones_roi=collections.Counter(lista_indices_roi)  
# print('valor maximo que se repite un sujeto con dato atipico: ',np.max(list(repeticiones_roi.values())))
# index_to_delete_roi=list(dict(filter(lambda x: x[1] >= 6, repeticiones_roi.items())).keys())
# data_roi_copy.drop(index_to_delete_roi, inplace = True)
for db in databases:
    print('\nBase de datos '+db)
    print('Original')
    print(data_roi[data_roi['database']==db].shape)
    print('Despues de eliminar datos atipicos')
    print(data_roi_copy[data_roi_copy['database']==db].shape)
    print('Porcentaje que se elimino %',100-data_roi_copy[data_roi_copy['database']==db].shape[0]*100/data_roi[data_roi['database']==db].shape[0])
data_roi_copy.drop(columns='index')
data_roi_copy.reset_index().to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_ROIporcolumnas_sin_atipicos.feather')
print('\nFinalización de eliminación de datos atipicos de ROIs')

datos_estadisticos=data_roi_copy.groupby(['group']).describe(include='all')
table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
dfi.export(table, 'Manipulacion- Rois-Componentes de todas las DB\Tablas_datos\Tabla_edad_escolaridad_sexo_todasBD_roi.png')
print(data_Comp.groupby(['group']).describe().loc[:,['age','education']])#Medice solo el promedio pero por grupo de tda la base de datos
#print(data_Comp.loc[:,['sex','group']].groupby(['sex','group']).size() )
#Por cada base de datos
datos_estadisticos=data_roi_copy.groupby(['group','database']).describe(include='all')
print(datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]])
table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
dfi.export(table, 'Manipulacion- Rois-Componentes de todas las DB\Tablas_datos\Tabla_edad_escolaridad_sexo_separadoBD_roi.png')


#Formato para graficos
datai=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
d_long=pd.DataFrame(columns=['participant_id', 'visit', 'group', 'condition', 'database', 'age','sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S', 'Power', 'Band', 'ROI'])

for i in rois_bandas:
    datax=datai.copy()
    datax.append(i)
    d_sep=data_roi_copy.loc[:,datax] #Tomo las columnas que necesito 
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

d_long.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_ROI_formatolargo_filtrados_sin_atipicos.feather')



        



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




