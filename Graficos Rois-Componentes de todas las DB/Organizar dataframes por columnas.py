import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display_html, display
import dataframe_image as dfi
import researchpy as rp

# Independent Components data
SRM=pd.read_feather(r'D:\BASESDEDATOS\SRM\derivatives\data_powers_components_norm_SRM.feather')
CHBMP=pd.read_feather(r'D:\BASESDEDATOS\CHBMP\derivatives\data_powers_components_norm_CHBMP.feather')
BIO=pd.read_feather(r'D:\BASESDEDATOS\BIOMARCADORES_DERIVATIVES_VERO\derivatives\data_powers_components_norm_BIOMARCADORES.feather')

datos=pd.concat([SRM,BIO,CHBMP]) #concatenation of data

columnas_deseadas=['subject', 'visit', 'group','condition','Study','C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
col_completas=list(datos.columns)
columnas=[]

for i in range(len(columnas_deseadas)):
    for j in range(len(col_completas)):
        if columnas_deseadas[i] in col_completas[j]:
            columnas.append(col_completas[j])

datos1=datos.loc[:,columnas] #Datos de las bases de datos con las componentes de interes
datos1= datos1.rename(columns={'subject':'participant_id','Study':'database'})#Cambio el nombre de columnas
datos1['participant_id']='sub-'+datos1['participant_id']
#print(len(datos1.columns))
##print(datos1)
datosICC=datos1 #Datos con las columnas necesarias

#Datos demograficos y pruebas neuropsicologicas

N_BIO=pd.read_csv('D:\BASESDEDATOS\BIOMARCADORES_DERIVATIVES_VERO\participants.tsv', sep='\t')
N_BIO=N_BIO.drop(['hand'], axis=1)

D_CHBMP=pd.read_csv("D:\BASESDEDATOS\CHBMP\Demographic_data.csv",header=1, sep=",")
col_demC=['Code', 'Gender', 'Age',  'Education Level ']
Dem_CHBMP=D_CHBMP.loc[:,col_demC]
MMSE_CHBMP=pd.read_csv("D:\BASESDEDATOS\CHBMP\MMSE.csv",header=1)
MMSE_CHBMP=MMSE_CHBMP.loc[:,['Code', 'Total Score']]
N_CHBMP=pd.merge(left=Dem_CHBMP,right=MMSE_CHBMP, how='left', left_on='Code', right_on='Code')
N_CHBMP = N_CHBMP.rename(columns={'Code':'participant_id','Age':'age','Gender':'sex','Education Level ':'education','Total Score':'MM_total'})
N_CHBMP['participant_id']='sub-'+N_CHBMP['participant_id']

N_SRM=pd.read_csv("D:\BASESDEDATOS\SRM\participants.tsv",sep='\t')
N_SRM=N_SRM.loc[:,['participant_id', 'age', 'sex','vf_1','vf_2','vf_3']] #Elegí vf3 ya que tenia resultados mas parecidos a los de biomarcadores (habian 3 vf)
N_SRM = N_SRM.rename(columns={'vf_1':'FAS_F','vf_2':'FAS_S','vf_3':'FAS_A'}) #Verificar con vero pero denom es igual a fluidez verbal?? creo que por eso la elegimos

p_N=pd.concat([N_BIO,N_CHBMP,N_SRM]) #Union d elos datos demograficos
N_BIO.replace({'None':np.NaN},inplace=True)
N_CHBMP.replace({'None':np.NaN},inplace=True)
N_SRM.replace({'None':np.NaN},inplace=True)
p_N.replace({'None':np.NaN},inplace=True)
#Union de los dataframe
d_B=pd.merge(left=datosICC,right=p_N, how='left', left_on='participant_id', right_on='participant_id')
d_B['sex'].replace({'f':'F','m':'M'}, inplace=True) #Cambio a que queden con sexo F y M
d_B['education'].replace({'None':np.NaN,'University School':'17','High School':'12', 'Secondary School':'11','College School':'16',}, inplace=True)
d_B['education'] = d_B['education'].astype('float64')



#Falta organizar el nivel de educacion 
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

#print(rp.summary_cont(d_B.groupby(['database', 'age'])['C25_rBeta3']))
#print(d_B.describe())

#Cantidad de datos vacios antes y despues de unir los dataframes

#Datos vacion antes de unir los dataframes demograficos e ICC
df_dem=pd.DataFrame()
df_dem['BIOMARCADORES']=N_BIO.isnull().sum()
df_dem['CHBMP']=N_CHBMP.isnull().sum()
df_dem['SRM']=N_SRM.isnull().sum()

print('\nTotal de datos demograficos BIOMARCADORES',len(N_BIO))
print('Total de datos demograficos CHBMP ',len(N_CHBMP))
print('Total de datos demograficos SRM ',len(N_SRM))

#Cantidad de datos luego de unir los dataframes




def ver_datos_vacios(d_B):
    
    df=pd.DataFrame()
    databases=d_B['database'].unique()
    for i in databases:
        dx=d_B[d_B['database']==i][['age', 'sex', 'education', 'MM_total', 'FAS_F','FAS_S','FAS_A']].isnull().sum()
        df[i]=dx
        print('\n', i)
        print('Numero de sujetos:',len(d_B[d_B['database']==i]['participant_id'].unique()))
        print('Numero de datos:',len(d_B[d_B['database']==i]))
    print('\nCantidad de datos vacios')
    print(df)
    return None


print('\nCantidad de datos vacios antes de unir  el dataframe con los datos demograficos')
print(df_dem)

print('\nTotal de datos al unir los IC con datos demograficos')
ver_datos_vacios(d_B)

## Filtrado de datos vacios




vacio_SRM=d_B[d_B['database']=='SRM'].isnull()
vacio_CHBMP=d_B[d_B['database']=='CHBMP'].isnull()
vacio_BIO=d_B[d_B['database']=='BIOMARCADORES'].isnull()

d_B.drop(vacio_SRM.index[vacio_SRM['FAS_F']==True], inplace = True)
d_B.drop(vacio_BIO.index[(vacio_BIO['FAS_F']==True) | (vacio_BIO['MM_total']==True)], inplace = True)
#d_B.drop(vacio_SRM.index[vacio_SRM['FAS_A']==True], inplace = True)
#d_B.drop(vacio_SRM.index[vacio_SRM['FAS_S']==True], inplace = True)
#Cambiar 
d_B.drop(vacio_CHBMP.index[(vacio_CHBMP['education']==True) | (vacio_CHBMP['MM_total']==True)], inplace = True) #Datos finalmente filtrados

#d_B.drop(d_B[d_B['database']=='CHBMP'][['MM_total']].isnull().index, inplace = True)

print('\nCantidad de datos vacios luego de filtrar')
ver_datos_vacios(d_B)
 #------------------------------------------------------
#Filtrado de datos en formato long

sujetos=d_B['participant_id'].unique()
datos_long=pd.read_feather(r"C:\Users\valec\Documents\JI\Codigos\Data_analysis_ML_Harmonization_Proyect\Graficos Rois-Componentes de todas las DB\Datos_componentes_formatolargo_sin_filtrar.feather")
datos_long['Subject']='sub-'+datos_long['Subject']

data_Comp=datos_long[datos_long.Subject.isin(sujetos)]
#print(len(data_Comp))

#data_Comp.reset_index().to_feather('Datos_componentes_formatolargo_filtrados.feather')

print('Valelinda')
#des.dfi.export('describebandas'+study[k]+'.png')

 #------------------------------------------------------
#Prueba normalidad
#Correlación entre la edad y las potencias graficamente y prueba de correlacion dependiendo de la normalidad
#Diferencias entre grupos por banda y frecuencia
#Diferencias en genero
 #------------------------------------------------------

