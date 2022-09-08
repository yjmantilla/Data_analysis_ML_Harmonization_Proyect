import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def graphic_component(data,name_band,num_columns=4, save=True,plot=True):
    max=data['Power'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="Power",data=data,hue='database',dodge=True, kind="box",col='Component',col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('Relative '+r'$\bf{'+name_band+r'}$'+ ' power in the components of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(.59,.95),ncol=3,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.05, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.01, 0.5,  'Relative powers', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('Manipulacion- Rois-Componentes de todas las DB\Graficos-Components\{name_band}_Components.png'.format(name_band=name_band))
        plt.close()
    
    return 


#se cargan los datos para hacer los graficos
# BIO=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BIOMARCADORES_longitudinal_data_powers_long_CE_norm_components.feather')

# SRM=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\SRM_longitudinal_data_powers_long_resteyesc_norm_components.feather')

# CHBMP=pd.read_feather(r'Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\CHBMP_longitudinal_data_powers_long_protmap_norm_components.feather')

# datos=pd.concat([SRM,BIO,CHBMP]) 

#Filtrado de los grupos en los que vana quedar los datos (Preguntar a Vero)

# datos['Group']=datos['Group'].replace({'CTR':'Control','G2':'Control','CHBMP':'Control','SRM':'Control','G1':'Control'})

# components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]
# data_Comp=datos[datos.Components.isin(components)] #Datos sin filtrar los sujetos con datos vacios

# datos_sin_filtrar=data_Comp.iloc[:,1:]
# datos_sin_filtrar.reset_index().to_feather('Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_sin_filtrar.feather')

data_Comp=pd.read_feather(r"Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados.feather")#Datos con sujetos sin datos vacios

bands= data_Comp['Band'].unique()
for band in bands:
    d_banda=data_Comp[data_Comp['Band']==band]
    graphic_component(d_banda,band,num_columns=4,save=True,plot=False)

print('valelinda')


#Filtrado de datos