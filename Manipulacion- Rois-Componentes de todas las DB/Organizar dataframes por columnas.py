from cmath import nan
import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display_html, display
#import dataframe_image as dfi
#import researchpy as rp

# Independent Components data
SRM=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_powers_components_norm_SRM.feather')
CHBMP=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_powers_components_norm_CHBMP.feather')
BIO=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\data_powers_components_norm_BIOMARCADORES.feather')

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

N_BIO=pd.read_excel('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Demograficosbiomarcadores.xlsx')
N_BIO = N_BIO.rename(columns={'Codigo':'participant_id','Edad en la visita':'age','Sexo':'sex','Escolaridad':'education','MMSE':'MM_total','F':'FAS_F','S':'FAS_S','A':'FAS_A','Visita':'visit'})
N_BIO['participant_id']=N_BIO['participant_id'].replace({'_':''}, regex=True)#Quito el _ y lo reemplazo con '' el participant Id
N_BIO['participant_id']='sub-'+N_BIO['participant_id']
subjects_bio=N_BIO['participant_id'].unique()

#subjects_bio=['sub-CTR001']
for i in subjects_bio:
    num_vis=len(N_BIO[N_BIO['participant_id']==i].loc[:,'visit'])
    if num_vis==5:
        #print('Antes')
        #print(N_BIO[N_BIO['participant_id']==i])
        V0=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V0'
        V1=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V1'
        V2=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V2'
        V3=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V3'
        V4=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V4'
        index0=N_BIO[N_BIO['participant_id']==i].loc[V0].index.tolist()[0]
        index1=N_BIO[N_BIO['participant_id']==i].loc[V1].index.tolist()[0]
        index2=N_BIO[N_BIO['participant_id']==i].loc[V2].index.tolist()[0]
        index3=N_BIO[N_BIO['participant_id']==i].loc[V3].index.tolist()[0]
        index4=N_BIO[N_BIO['participant_id']==i].loc[V4].index.tolist()[0]
        #Para modificar el MM_total y FAS MM_total
        if N_BIO[N_BIO['participant_id']==i].loc[V1]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index1,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index0,['MM_total','FAS_F','FAS_A','FAS_S']]
        if N_BIO[N_BIO['participant_id']==i].loc[V3]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index3,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index2,['MM_total','FAS_F','FAS_A','FAS_S']]
        if N_BIO[N_BIO['participant_id']==i].loc[V4]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index4,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index2,['MM_total','FAS_F','FAS_A','FAS_S']]
        #print('Despues')
        #print(N_BIO[N_BIO['participant_id']==i])
    if num_vis==4:
        #print('Antes')
        #print(N_BIO[N_BIO['participant_id']==i])
        V0=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V0'
        V1=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V1'
        V2=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V2'
        V3=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V3'
        index0=N_BIO[N_BIO['participant_id']==i].loc[V0].index.tolist()[0]
        index1=N_BIO[N_BIO['participant_id']==i].loc[V1].index.tolist()[0]
        index2=N_BIO[N_BIO['participant_id']==i].loc[V2].index.tolist()[0]
        index3=N_BIO[N_BIO['participant_id']==i].loc[V3].index.tolist()[0]
        #Para modificar el MM_total y FAS MM_total
        if N_BIO[N_BIO['participant_id']==i].loc[V1]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index1,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index0,['MM_total','FAS_F','FAS_A','FAS_S']]
        if N_BIO[N_BIO['participant_id']==i].loc[V3]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index3,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index2,['MM_total','FAS_F','FAS_A','FAS_S']]    
        #print('Despues')
        #print(N_BIO[N_BIO['participant_id']==i])
    if num_vis==2:
        # print('Antes')
        # print(N_BIO[N_BIO['participant_id']==i])
        V0=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V0'
        V1=N_BIO[N_BIO['participant_id']==i].loc[:,'visit']=='V1'
        index0=N_BIO[N_BIO['participant_id']==i].loc[V0].index.tolist()[0]
        index1=N_BIO[N_BIO['participant_id']==i].loc[V1].index.tolist()[0]
        if N_BIO[N_BIO['participant_id']==i].loc[V1]['FAS_F'].isna().tolist()[0]:
            N_BIO.loc[index1,['MM_total','FAS_F','FAS_A','FAS_S']]=N_BIO.loc[index0,['MM_total','FAS_F','FAS_A','FAS_S']]
        # print('Despues')
        # print(N_BIO[N_BIO['participant_id']==i])


D_CHBMP=pd.read_csv("Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Demographic_data_CHBMP.csv",header=1, sep=",")
col_demC=['Code', 'Gender', 'Age',  'Education Level ']
Dem_CHBMP=D_CHBMP.loc[:,col_demC]
MMSE_CHBMP=pd.read_csv("Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\MMSE_CHBMP.csv",header=1)
MMSE_CHBMP=MMSE_CHBMP.loc[:,['Code', 'Total Score']]
N_CHBMP=pd.merge(left=Dem_CHBMP,right=MMSE_CHBMP, how='left', left_on='Code', right_on='Code')
N_CHBMP = N_CHBMP.rename(columns={'Code':'participant_id','Age':'age','Gender':'sex','Education Level ':'education','Total Score':'MM_total'})
N_CHBMP['participant_id']='sub-'+N_CHBMP['participant_id']

N_SRM=pd.read_csv("Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\participantsSRM.tsv",sep='\t')
N_SRM=N_SRM.loc[:,['participant_id', 'age', 'sex','vf_1','vf_2','vf_3']] #Elegí vf3 ya que tenia resultados mas parecidos a los de biomarcadores (habian 3 vf)
N_SRM = N_SRM.rename(columns={'vf_1':'FAS_F','vf_2':'FAS_S','vf_3':'FAS_A'}) #Verificar con vero pero denom es igual a fluidez verbal?? creo que por eso la elegimos

N_BIO.replace({'None':np.NaN},inplace=True)
N_CHBMP.replace({'None':np.NaN},inplace=True)
N_SRM.replace({'None':np.NaN},inplace=True)

#Union de los dataframe
d_SRM=pd.merge(left=datosICC[datosICC['database']=='SRM'],right=N_SRM , how='left', left_on='participant_id', right_on='participant_id')
d_CHBMP=pd.merge(datosICC[datosICC['database']=='CHBMP'],N_CHBMP)
d_BIO=pd.merge(datosICC[datosICC['database']=='BIOMARCADORES'],N_BIO)
d_B=pd.concat([d_SRM,d_BIO,d_CHBMP])
d_B['sex'].replace({'f':'F','m':'M','Masculino':'M','Femenino':'F'}, inplace=True) #Cambio a que queden con sexo F y M
d_B['education'].replace({'None':np.NaN,'University School':'17','High School':'12', 'Secondary School':'11','College School':'16',}, inplace=True)
d_B['education'] = d_B['education'].astype('float64')

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
d_B.reset_index(inplace=True, drop=True)


##Datos filtrados por cada base de datos
l=[]
l.extend(d_B[d_B['database']=='BIOMARCADORES'].dropna(subset=['MM_total','FAS_F']).index.tolist())
l.extend(d_B[d_B['database']=='SRM'].dropna(subset=['FAS_F']).index.tolist())
l.extend(d_B[d_B['database']=='CHBMP'].dropna(subset=['MM_total','education']).index.tolist())

lista=list(set(l))
d_B=d_B.loc[lista,:]
print('\nCantidad de datos vacios luego de filtrar')
ver_datos_vacios(d_B)
#Base de datos organizada
d_B.reset_index().to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas.feather')
#-------------------------------------------------------
#Formato long
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
    d_sep=d_B.loc[:,datax] #Tomo las columnas que necesito 
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
d_long['group'].replace({'G1':'Control','G2':'Control','CTR':'Control'}, inplace=True) ##Para que estos de biomarcadores queden como controles
d_long.to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados.feather')
print('valelinda')
 #------------------------------------------------------
#Filtrado de datos en formato long

#sujetos=d_B['participant_id'].unique()
#datos_long=pd.read_feather(r"Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_sin_filtrar.feather")
#datos_long['Subject']='sub-'+datos_long['Subject']

#data_Comp=datos_long[datos_long.Subject.isin(sujetos)]
#print(len(data_Comp))

#data_Comp.reset_index().to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados.feather')

#print('Valelinda')
#des.dfi.export('describebandas'+study[k]+'.png')

 #------------------------------------------------------
#Prueba normalidad
#Correlación entre la edad y las potencias graficamente y prueba de correlacion dependiendo de la normalidad
#Diferencias entre grupos por banda y frecuencia
#Diferencias en genero
 #------------------------------------------------------

