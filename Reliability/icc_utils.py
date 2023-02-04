import pandas as pd
def get_biodf(demofile):
    N_BIO=pd.read_excel(demofile)
    N_BIO = N_BIO.rename(columns={'Codigo':'Subject','Edad en la visita':'age','Sexo':'sex','Escolaridad':'education','Visita':'Session'})
    N_BIO=N_BIO.drop(['MMSE', 'F', 'A', 'S'], axis=1)
    N_BIO['Subject']=N_BIO['Subject'].replace({'_':''}, regex=True)#Quito el _ y lo reemplazo con '' 
    N_BIO=N_BIO[N_BIO.Session.isin(['V0'])]
    N_BIO=N_BIO.drop(['Session'], axis=1)
    return  N_BIO

def agefun(x):
    if x <= 34:
        return 'Young Adult'
    elif x >= 41:
        return 'Middle Age'
    else:
        return 'None'

def merge_biodatos(datosNoBio,N_BIO):
    N_BIO['Group2']=N_BIO.age.apply(agefun)
    datos=pd.merge(datosNoBio,N_BIO)
    datos = datos.drop(datos.index[datos['Group2']=='None'],axis=0)
    datos['Group'] = datos['Group2']
    datos=datos.drop('Group2',axis=1)
    groups_labels = list(set(datos['Group']))
    return datos,groups_labels


# Definicion de Grupos

###
###
# def goal(x,y,df):
#     d = age_counts(x,y,df)
#     d = list(d.values())
#     ddif = d[0]-d[1]
#     if ddif == 0:
#         ddif = 1
#     dsum = d[0]+d[1]
#     return ddif,dsum

# cut = np.arange(N_BIO_HEALTHY.age.min(),N_BIO_HEALTHY.age.max())
# intervals = np.arange(N_BIO_HEALTHY.age.min(),N_BIO_HEALTHY.age.max())

# from itertools import product

# flatcomb = list(product(cut,intervals))

# dsum = np.zeros((len(flatcomb),))
# ddif = np.zeros((len(flatcomb),))
# dboth =np.zeros((len(flatcomb),))

# for i,com in enumerate(flatcomb):
#     c,inte = com
#     diff,sumss=goal(c,inte,N_BIO_HEALTHY)
#     dsum[i]=sumss
#     ddif[i]=diff
#     dboth[i]=sumss/diff

# idxdiff=np.argmin(ddif)
# idxsum=np.argmax(dsum)
# idxboth=np.argmax(dboth)
# for idx in [idxboth,idxsum,idxdiff]:
#     print(flatcomb[idx],age_counts(flatcomb[idx][0],flatcomb[idx][1],N_BIO_HEALTHY))

# def foogroup(x):
#     return 'G2' if 'G2' in x else 'CTR'

# N_BIO_HEALTHY['group']=N_BIO_HEALTHY.Subject.apply(foogroup)

# def groupage(x,y,df):

#     N_G2 = df[df['group']=='G2']
#     N_CTR =df[df['group']=='CTR']
#     return (N_G2['age']<=x).sum(),(N_CTR['age']>=y).sum()
# groupage(35,40,N_BIO_HEALTHY)

