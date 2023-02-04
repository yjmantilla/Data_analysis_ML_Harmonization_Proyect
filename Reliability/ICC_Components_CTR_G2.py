'''Code used to filter the BIOMARCADORES database by components of the G2 and CTR groups.
They have the same number of visits but do not correspond to the same visits.
The ICC is calculated with these data '''

import numpy as np
import pandas as pd 
import collections
import scipy.io
from tokenize import group
import pingouin as pg
from scipy import stats
import dataframe_image as dfi
import warnings
from scipy.stats import mannwhitneyu
warnings.filterwarnings("ignore")
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from Reliability.icc_utils import get_biodf,merge_biodatos
mode = 'components'
column = 'Components'
if mode == 'components':
    selection = ['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ] #Neuronal components
else:
    selection = None #['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ] #Neuronal components


datos1=pd.read_feather(rf"Reliability\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_{mode}.feather") 
datos2=pd.read_feather(rf"Reliability\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_norm_{mode}.feather")
datos=pd.concat((datos1, datos2))#Original Data

demofile = r"Y:\all\Demograficosbiomarcadores.xlsx"
N_BIO=get_biodf(demofile)
N_BIO_HEALTHY = N_BIO.copy()

def foohealth(x):
    return 'G2' in x or 'CTR' in x
N_BIO_HEALTHY['HEALTHY'] = N_BIO_HEALTHY['Subject'].apply(foohealth)
N_BIO_HEALTHY = N_BIO_HEALTHY[N_BIO_HEALTHY['HEALTHY']]


def pair_data(datos,components,column):
    #datos=datos.drop(datos[datos['Session']=='V4P'].index)#Borrar datos
    datos['Session']=datos['Session'].replace({'VO':'V0','V4P':'V4'})
    groups=['CTR','G2'] # Pair groups 
    datos=datos[datos[column].isin(components) ] # Only data of components select
    datos=datos[datos.Group.isin(groups) ] #Only data of CTR y G2
    visitas=['V0','V1','V2','V3']
    #Script for drop subjects without four sessions select
    for i in groups:
        g=datos[datos['Group']==i]
        sujetos=g['Subject'].unique()
        print('Cantidad de sujetos de '+i+': ', len(sujetos))
        k=0
        for j in sujetos:
            s=g[g['Subject']==j]
            if len(s['Session'].unique()) !=4:
                k=k+1
                datos=datos.drop(datos[datos['Subject']==j].index)
            if len(s['Session'].unique()) ==4:
                v=s['Session'].unique()
                for vis in range(len(visitas)):
                    datos.loc[(datos.Subject==j)&(datos.Session==v[vis]),'Session']=visitas[vis]     
        print('Sujetos a borrar:', k)
        print('Sujetos a analizar con 4 visitas: ',len(sujetos)-k)
    for i in groups:
        g=datos[datos['Group']==i]
        print('Cantidad de sujetos al filtrar '+ i+': ',len(g['Subject'].unique()))
    #datos['Group']=datos['Group'].replace({'CTR':'Control','G2':'Control'})
    print('Visitas de los sujetos: ',datos['Session'].unique())
    return datos

if selection is None:
    selection = list(set(datos[column]))
    selection.sort()
datos=pair_data(datos,selection,column) #Datos filtrados
datosNoBio=datos.copy()

datos,groups_labels = merge_biodatos(datosNoBio,N_BIO)


N_BIO_HEALTHY = N_BIO[N_BIO.Subject.isin(datos.Subject)]
# def age_counts(x,y,df):
#     return {x:(df['age']<=x).sum(),x+y:(df['age']>=x+y).sum()}

# # for i in range(N_BIO_HEALTHY.age.min(),N_BIO_HEALTHY.age.max()):
# #     print(age_counts(i,1,N_BIO_HEALTHY))
# ds=[]
# for j in range(1,N_BIO_HEALTHY.age.max()-N_BIO_HEALTHY.age.min()):
#     for i in range(N_BIO_HEALTHY.age.min(),N_BIO_HEALTHY.age.max()):
#         da=age_counts(i,j,N_BIO_HEALTHY)
#         dk = list(da.keys())
#         age_sep=abs(dk[0]-dk[1])
#         d = list(da.values())
#         ddif = d[0]-d[1]
#         dsum = d[0]+d[1]
#         if dsum > 10 and abs(ddif) < 5:
#             if d[0] >10 and d[1]>10:
#                 if dsum/43 >=0.7:
#                     print(i,j,43-dsum,'{:.2f}'.format((dsum)/43))
#                     print(da)
#                     ddd ={'Edad Joven':f'menor a {dk[0]}','Edad Viejo':f'mayor a {dk[1]}','Num.Sujs Joven':d[0],'Num. Sujs Viejo':d[1],'Separacion edad entre grupos':age_sep,'Num. Total Sujs':dsum,'Porcentaje de Sujs Eliminados':100*(1-dsum/43)}
#                     ds.append(ddd)

# dfRange=pd.DataFrame.from_dict(ds)
# dfRange.to_csv('RangoEdad.csv',sep=';')


#Datos estadisticos de la edad, escolaridad y sexo
sel_stat = [selection[0]] #['C14']

d_p=datos[datos.Session.isin(['V0'])&datos.Bands.isin(['delta'])&datos.Components.isin(sel_stat)&datos.Stage.isin(['Normalized data'])]
datos_estadisticos=d_p.groupby(['Group']).describe(include='all')
table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
dfi.export(table, 'Reliability\Tabla_edad_escolaridad_sexo_separadoreliability.png')
#Pruebas estadisticas 
print('\nNormalidad en edad')
print(pg.normality(data=d_p, dv='age', group='Group',method='shapiro'))
print('\nNormalidad en educacion')
print(pg.normality(data=d_p, dv='education', group='Group',method='shapiro'))
print('\nDiferencias en edad entre grupos U-test')
print(mannwhitneyu(d_p[d_p.Group.isin([groups_labels[0]])]['age'], d_p[d_p.Group.isin([groups_labels[1]])]['age']))
print('\nDiferencias en escolaridad entre grupos U-test')
print(mannwhitneyu(d_p[d_p.Group.isin([groups_labels[0]])]['education'], d_p[d_p.Group.isin([groups_labels[1]])]['education']))
## Diferencias estadisticas entre CTR y G2 en cuanto la edad y escolaridad

#Tabla edad escolaridad y genero y valores p asociados a las pruebas 

# ANOVA mix
print('Anova mix')
aov = pg.mixed_anova(data = datos[datos.Stage.isin(['Normalized data'])], dv = 'Powers', between = 'Group', within = 'Session',subject = 'Subject')
pg.print_table(aov)

#U test
print('Test U')
ap=pg.mwu(datos[datos['Group']==groups_labels[0]]['Powers'],datos[datos['Group']==groups_labels[0]]['Powers'])
pg.print_table(ap)


bandas=datos['Bands'].unique()
Stage=datos['Stage'].unique()
icc_value = pd.DataFrame(columns=['ICC','F','df1','df2','pval','CI95%'])
G=groups_labels

for st in Stage:
    d_stage=datos[datos['Stage']==st] 
    for g in G:
        d_group=d_stage[d_stage['Group']==g]
        dic={}
        icc_comp=[]
        for comp in selection:
            d_comp=d_group[d_group[column]==comp]
            visits=list(d_comp['Session'].unique())
            matrix_c=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage','Subject']) #Se le asigna a un dataframe los datos d elas columnas
            subjects=d_comp['Subject'].unique() 
            for vis in visits:
                matrix_s=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage','Subject'])
                power=d_comp[d_comp['Session']==vis]['Powers'].tolist()
                n_vis=[vis]*len(power)
                matrix_s['Session']=n_vis
                matrix_s['Power']=power  
                matrix_s['Group']=d_comp[d_comp['Session']==vis]['Group'].tolist()
                matrix_s['Bands']=d_comp[d_comp['Session']==vis]['Bands'].tolist()
                matrix_s['Stage']=d_comp[d_comp['Session']==vis]['Stage'].tolist()
                matrix_s['Subject']=d_comp[d_comp['Session']==vis]['Subject'].tolist()

                matrix_c=matrix_c.append(matrix_s, ignore_index = True)            
            
            index=list(np.arange(0,len(n_vis),1))*len(visits)
            matrix_c['index']=index

            for i,ban in enumerate(bandas):
                fil_bands=matrix_c['Bands']==ban
                filter=matrix_c[fil_bands]
                icc=pg.intraclass_corr(data=filter, targets='index', raters='Session', ratings='Power').round(6)
                #icc3=icc
                icc3 = icc[icc['Type']=='ICC3k']
                icc3 = icc3.set_index('Type')
                # print(filter['Stage'])
                icc3['Stage']=st #filter['Stage'][i]
                icc3['Group']=g #filter['Group'][i]
                icc3['Bands']=ban
                icc3['Components']=comp
                icc_value=icc_value.append(icc3,ignore_index=True)

        icc_value.append(icc_value)
    icc_value.append(icc_value)
#print(icc_value)
icc_value.to_csv(rf'Reliability/ICC_values_csv/icc_values_{mode}_G2-CTR.csv',sep=';')
#matrix_c.to_csv(r'sovaharmony\Reproducibilidad\icc_values_G2-CTR_test.csv',sep=';') 
