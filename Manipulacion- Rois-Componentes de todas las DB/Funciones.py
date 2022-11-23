
import pandas as pd
import warnings
import collections
import numpy as np

"Functions to save dataframes for graphics"

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
    data_new=data_new[data_new['database']=='DUQUE']
    data_new['ROI']=data_new['ROI'].replace({'ROI_':''}, regex=True)#Quito el _ y lo reemplazo con '' 
    data_new.reset_index().to_feather('{path}\Datosparaorganizardataframes\{name}.feather'.format(path=path,name=name))
    print('Dataframe para graficos de {type} guardado: {name}'.format(type=type,name=name))

def dataframe_long_components(data,type,columns,name,path):
    '''Function used to convert a wide dataframe into a long one to be used for graphing by IC'''
    #demographic data and neuropsychological test columns
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    columns_df=data_dem+[type, 'Band', 'Component']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands
    bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
    #Components
    componentes=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                band=j
        for c in componentes:
            if c in i:
                componente=c
        d_sep['Band']=[band]*len(d_sep)
        d_sep['Component']=[componente]*len(d_sep)
        d_sep= d_sep.rename(columns={i:type})
        data_new=data_new.append(d_sep,ignore_index = True) #Uno el dataframe 
    data_new.reset_index().to_feather('{path}\Datosparaorganizardataframes\{name}.feather'.format(path=path,name=name))
    print('Dataframe para graficos de {type} guardado: {name}'.format(type=type,name=name))


def dataframe_long_cross(data,type='Cross Frequency',columns=None,name=None,path=None):
    '''Function used to convert a dataframe to be used for graphing.'''
    #demographic data and neuropsychological test columns
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    columns_df=data_dem+[type, 'Band','M_Band', 'Component']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands
    bandas=['_Delta','_Theta','_Alpha-1','_Alpha-2','_Beta1','_Beta2','_Beta3','_Gamma']
    m_bandas=['M_delta','M_theta','M_alpha-1','M_alpha-2','M_beta1','M_beta2','M_beta3','M_gamma']
    componentes=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']

    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                band=j
        for m in m_bandas:
            if m in i:
                bandm=m
        for c in componentes:
            if c in i:
                componente=c
        d_sep['Band']=[band]*len(d_sep)
        d_sep['M_Band']=[bandm]*len(d_sep)
        d_sep['Component']=[componente]*len(d_sep)
        d_sep= d_sep.rename(columns={i:type})
        data_new=data_new.append(d_sep,ignore_index = True) #Uno el dataframe 
    data_new['Band']=data_new['Band'].replace({'_':''}, regex=True)#Quito el _ y lo reemplazo con ''
    data_new=data_new[data_new['database']=='DUQUE']
    data_new.reset_index().to_feather('{path}\Datosparaorganizardataframes\{name}.feather'.format(path=path,name=name))
    print('Dataframe para graficos de {type} guardado'.format(type=type))

def dataframe_componentes_deseadas(data,columnas):
    """Function that returns a dataframe with the desired columns, only having data with the independent components of interest
    columnas=list of columns to be retained
    """
    columnas_deseadas=[*columnas,'C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25'] #columns of interest
    col_completas=list(data.columns)
    columnas=[]
    for i in range(len(columnas_deseadas)):
        for j in range(len(col_completas)):
            if columnas_deseadas[i] in col_completas[j]:
                columnas.append(col_completas[j])
    data_new=data.loc[:,columnas] #Dataframe with columns of interest
    return data_new


def removing_outliers(data,columns):
    '''
    Function used to return a dataframe without outliers, where it is verified that no more than 5$%$ of the data is lost per database.
    '''
    data['index'] = data.index #It was necessary to create a column labeled "index" to take the indexes in an easy way
    data_copy=data.copy()
    databases=data['database'].unique()
    for db in databases:
        datos_db=data[data['database']==db] 
        indices_db=[]
        for com in columns:
            Q1 = np.percentile(datos_db[com], 25, interpolation = 'midpoint')
            Q3 = np.percentile(datos_db[com], 75,interpolation = 'midpoint')
            IQR = Q3 - Q1 
            dataupper=datos_db[datos_db[com] >= (Q3+1.5*IQR)]#Valores atipicos superiores
            if dataupper.empty:
                upper=[]
            else:
                upper=dataupper.index.tolist() #lista de indices del dataframe que son valores atipicos
            datalower=datos_db[datos_db[com] <= (Q1-1.5*IQR)]#Valores atipicos inferiores
            if datalower.empty:
                lower=[]
            else:
                lower=datalower.index.tolist()#lista de indices del dataframe que son valores atipicos
            indices=upper+lower #union de upper y lower de indices del dataframe que son valores atipicos
            indices_db.extend(indices) #Se tiene una lista de indices por cada base de datos
    
        repeticiones=collections.Counter(indices_db) #Diccionario que contiene cuantas veces un indice(sujeto) tiene un dato atipico, en una banda de una componente
        bandera=True
        
        i=2
        while(bandera):#Mientras no se encuentre el porcentaje de perdida requerido
            i+=1 #se aumenta cada que se entra al while
            data_prueba=data.copy()#  copia de data frame para no borrar datos del dataframe original,se crea cada que se entra al while
            index_to_delete=list(dict(filter(lambda x: x[1] > i, repeticiones.items())).keys()) # se crea una lista de los indices cuyas repeticiones de datos atipicos es mayor a i
            data_prueba.drop(index_to_delete, inplace = True)#Se borran los indices del dataframe de prueba para saber el porcentaje de datos borrados
            porcentaje=100-data_prueba[data_prueba['database']==db].shape[0]*100/data[data['database']==db].shape[0]#porcentaje de datos borrados
            if porcentaje<=5:
                #Si el procentaje borrado por primera vez es menor o igual a 5, se borra del dataframe copia los indices que dan el resultado deseado
                data_copy.drop(index_to_delete, inplace = True)
                bandera=False #se cambia la bandera para que no entre mas al while
                #print(porcentaje)
    data_copy.drop(columns='index')
    #Para observar un resumen de los datos antes y despues de eliminar sujetos con mayor cantidad de datos atipicos
    for db in databases:
        print('\nBase de datos '+db)
        print('Original')
        print(data[data['database']==db].shape)
        print('Despues de eliminar datos atipicos')
        print(data_copy[data_copy['database']==db].shape)
        print('Porcentaje que se elimino %',100-data_copy[data_copy['database']==db].shape[0]*100/data[data['database']==db].shape[0])
    return data_copy

def estadisticos_demograficos(data,name,path):
    """
    Function that exports tables of general description of age, gender and sex of the data.

    link de ayuda
    https://pandas.pydata.org/docs/user_guide/indexing.html
    https://kanoki.org/2022/07/25/pandas-select-slice-rows-columns-multiindex-dataframe/

    """
    
    import dataframe_image as dfi
    datos_estadisticos=data.groupby(['group']).describe(include='all')
    table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
    dfi.export(table, '{path}\Tablas_datos\Tabla_edad_escolaridad_sexo_todasBD_{name}.png'.format(path=path,name=name))
    #Por cada base de datos
    datos_estadisticos=data.groupby(['database','group']).describe(include='all')
    table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
    dfi.export(table, '{path}\Tablas_datos\Tabla_edad_escolaridad_sexo_separadoBD_{name}.png'.format(path=path,name=name))

#Listas de columnas
columns_powers_ic=['C14_rDelta', 'C14_rTheta', 'C14_rAlpha-1', 'C14_rAlpha-2',
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

columns_powers_rois=['ROI_F_rDelta','ROI_C_rDelta', 'ROI_PO_rDelta', 'ROI_T_rDelta', 'ROI_F_rTheta',
       'ROI_C_rTheta', 'ROI_PO_rTheta', 'ROI_T_rTheta', 'ROI_F_rAlpha-1',
       'ROI_C_rAlpha-1', 'ROI_PO_rAlpha-1', 'ROI_T_rAlpha-1', 'ROI_F_rAlpha-2',
       'ROI_C_rAlpha-2', 'ROI_PO_rAlpha-2', 'ROI_T_rAlpha-2', 'ROI_F_rBeta1',
       'ROI_C_rBeta1', 'ROI_PO_rBeta1', 'ROI_T_rBeta1', 'ROI_F_rBeta2',
       'ROI_C_rBeta2', 'ROI_PO_rBeta2', 'ROI_T_rBeta2', 'ROI_F_rBeta3',
       'ROI_C_rBeta3', 'ROI_PO_rBeta3', 'ROI_T_rBeta3', 'ROI_F_rGamma',
       'ROI_C_rGamma', 'ROI_PO_rGamma', 'ROI_T_rGamma']



#Sl columns Roi
columns_SL_roi=['SL_ROI_F_Delta', 'SL_ROI_C_Delta', 'SL_ROI_PO_Delta', 'SL_ROI_T_Delta',
       'SL_ROI_F_Theta', 'SL_ROI_C_Theta', 'SL_ROI_PO_Theta', 'SL_ROI_T_Theta',
       'SL_ROI_F_Alpha-1', 'SL_ROI_C_Alpha-1', 'SL_ROI_PO_Alpha-1',
       'SL_ROI_T_Alpha-1', 'SL_ROI_F_Alpha-2', 'SL_ROI_C_Alpha-2',
       'SL_ROI_PO_Alpha-2', 'SL_ROI_T_Alpha-2', 'SL_ROI_F_Beta1',
       'SL_ROI_C_Beta1', 'SL_ROI_PO_Beta1', 'SL_ROI_T_Beta1', 'SL_ROI_F_Beta2',
       'SL_ROI_C_Beta2', 'SL_ROI_PO_Beta2', 'SL_ROI_T_Beta2', 'SL_ROI_F_Beta3',
       'SL_ROI_C_Beta3', 'SL_ROI_PO_Beta3', 'SL_ROI_T_Beta3', 'SL_ROI_F_Gamma',
       'SL_ROI_C_Gamma', 'SL_ROI_PO_Gamma', 'SL_ROI_T_Gamma']

#Coherence columns Roi
columns_coherence_roi=['Coherence_Delta', 'Coherence_Theta', 'Coherence_Alpha-1',
       'Coherence_Alpha-2', 'Coherence_Beta1', 'Coherence_Beta2',
       'Coherence_Beta3', 'Coherence_Gamma']

#Entropy columns Roi  
columns_entropy_rois=['Entropy_ROI_F_Delta',
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

#Cross frequency columns Roi
columns_cross_rois=['Cross_ROI_F_Delta','Cross_ROI_C_Delta', 'Cross_ROI_PO_Delta', 'Cross_ROI_T_Delta',
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

columns_SL_ic=['sl_C14_Delta', 'sl_C14_Theta', 'sl_C14_Alpha-1',
       'sl_C14_Alpha-2', 'sl_C14_Beta1', 'sl_C14_Beta2', 'sl_C14_Beta3',
       'sl_C14_Gamma', 'sl_C15_Delta', 'sl_C15_Theta', 'sl_C15_Alpha-1',
       'sl_C15_Alpha-2', 'sl_C15_Beta1', 'sl_C15_Beta2', 'sl_C15_Beta3',
       'sl_C15_Gamma', 'sl_C18_Delta', 'sl_C18_Theta', 'sl_C18_Alpha-1',
       'sl_C18_Alpha-2', 'sl_C18_Beta1', 'sl_C18_Beta2', 'sl_C18_Beta3',
       'sl_C18_Gamma', 'sl_C20_Delta', 'sl_C20_Theta', 'sl_C20_Alpha-1',
       'sl_C20_Alpha-2', 'sl_C20_Beta1', 'sl_C20_Beta2', 'sl_C20_Beta3',
       'sl_C20_Gamma', 'sl_C22_Delta', 'sl_C22_Theta', 'sl_C22_Alpha-1',
       'sl_C22_Alpha-2', 'sl_C22_Beta1', 'sl_C22_Beta2', 'sl_C22_Beta3',
       'sl_C22_Gamma', 'sl_C23_Delta', 'sl_C23_Theta', 'sl_C23_Alpha-1',
       'sl_C23_Alpha-2', 'sl_C23_Beta1', 'sl_C23_Beta2', 'sl_C23_Beta3',
       'sl_C23_Gamma', 'sl_C24_Delta', 'sl_C24_Theta', 'sl_C24_Alpha-1',
       'sl_C24_Alpha-2', 'sl_C24_Beta1', 'sl_C24_Beta2', 'sl_C24_Beta3',
       'sl_C24_Gamma']
columns_coherence_ic=['cohfreq_C14_Delta', 'cohfreq_C14_Theta',
       'cohfreq_C14_Alpha-1', 'cohfreq_C14_Alpha-2', 'cohfreq_C14_Beta1',
       'cohfreq_C14_Beta2', 'cohfreq_C14_Beta3', 'cohfreq_C14_Gamma',
       'cohfreq_C15_Delta', 'cohfreq_C15_Theta', 'cohfreq_C15_Alpha-1',
       'cohfreq_C15_Alpha-2', 'cohfreq_C15_Beta1', 'cohfreq_C15_Beta2',
       'cohfreq_C15_Beta3', 'cohfreq_C15_Gamma', 'cohfreq_C18_Delta',
       'cohfreq_C18_Theta', 'cohfreq_C18_Alpha-1', 'cohfreq_C18_Alpha-2',
       'cohfreq_C18_Beta1', 'cohfreq_C18_Beta2', 'cohfreq_C18_Beta3',
       'cohfreq_C18_Gamma', 'cohfreq_C20_Delta', 'cohfreq_C20_Theta',
       'cohfreq_C20_Alpha-1', 'cohfreq_C20_Alpha-2', 'cohfreq_C20_Beta1',
       'cohfreq_C20_Beta2', 'cohfreq_C20_Beta3', 'cohfreq_C20_Gamma',
       'cohfreq_C22_Delta', 'cohfreq_C22_Theta', 'cohfreq_C22_Alpha-1',
       'cohfreq_C22_Alpha-2', 'cohfreq_C22_Beta1', 'cohfreq_C22_Beta2',
       'cohfreq_C22_Beta3', 'cohfreq_C22_Gamma', 'cohfreq_C23_Delta',
       'cohfreq_C23_Theta', 'cohfreq_C23_Alpha-1', 'cohfreq_C23_Alpha-2',
       'cohfreq_C23_Beta1', 'cohfreq_C23_Beta2', 'cohfreq_C23_Beta3',
       'cohfreq_C23_Gamma', 'cohfreq_C24_Delta', 'cohfreq_C24_Theta',
       'cohfreq_C24_Alpha-1', 'cohfreq_C24_Alpha-2', 'cohfreq_C24_Beta1',
       'cohfreq_C24_Beta2', 'cohfreq_C24_Beta3', 'cohfreq_C24_Gamma']
columns_entropy_ic=['entropy_C14_Delta', 'entropy_C14_Theta',
       'entropy_C14_Alpha-1', 'entropy_C14_Alpha-2', 'entropy_C14_Beta1',
       'entropy_C14_Beta2', 'entropy_C14_Beta3', 'entropy_C14_Gamma',
       'entropy_C15_Delta', 'entropy_C15_Theta', 'entropy_C15_Alpha-1',
       'entropy_C15_Alpha-2', 'entropy_C15_Beta1', 'entropy_C15_Beta2',
       'entropy_C15_Beta3', 'entropy_C15_Gamma', 'entropy_C18_Delta',
       'entropy_C18_Theta', 'entropy_C18_Alpha-1', 'entropy_C18_Alpha-2',
       'entropy_C18_Beta1', 'entropy_C18_Beta2', 'entropy_C18_Beta3',
       'entropy_C18_Gamma', 'entropy_C20_Delta', 'entropy_C20_Theta',
       'entropy_C20_Alpha-1', 'entropy_C20_Alpha-2', 'entropy_C20_Beta1',
       'entropy_C20_Beta2', 'entropy_C20_Beta3', 'entropy_C20_Gamma',
       'entropy_C22_Delta', 'entropy_C22_Theta', 'entropy_C22_Alpha-1',
       'entropy_C22_Alpha-2', 'entropy_C22_Beta1', 'entropy_C22_Beta2',
       'entropy_C22_Beta3', 'entropy_C22_Gamma', 'entropy_C23_Delta',
       'entropy_C23_Theta', 'entropy_C23_Alpha-1', 'entropy_C23_Alpha-2',
       'entropy_C23_Beta1', 'entropy_C23_Beta2', 'entropy_C23_Beta3',
       'entropy_C23_Gamma', 'entropy_C24_Delta', 'entropy_C24_Theta',
       'entropy_C24_Alpha-1', 'entropy_C24_Alpha-2', 'entropy_C24_Beta1',
       'entropy_C24_Beta2', 'entropy_C24_Beta3', 'entropy_C24_Gamma']
columns_cross_ic=[]
