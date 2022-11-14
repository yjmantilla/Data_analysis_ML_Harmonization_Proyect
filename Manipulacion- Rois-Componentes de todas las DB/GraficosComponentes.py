import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def graphic_component(data,name_band,id,num_columns=4,save=True,plot=True):
    max=data['Power'].max()
    sns.set(rc={'figure.figsize':(15,12)})
    sns.set_theme(style="white")
    axs=sns.catplot(x='group',y="Power",data=data,hue='database',dodge=True, kind="box",col='Component',col_wrap=num_columns,palette='winter_r',fliersize=1.5,linewidth=0.5,legend=False)
    #plt.yticks(np.arange(0,round(max),0.1))
    axs.set(xlabel=None)
    axs.set(ylabel=None)
    axs.fig.suptitle('Relative '+r'$\bf{'+name_band+r'}$'+ ' power in the components of normalized data given by the databases ')
    axs.add_legend(loc='upper right',bbox_to_anchor=(.59,.95),ncol=4,title="Database")

    axs.fig.subplots_adjust(top=0.85,bottom=0.121, right=0.986,left=0.05, hspace=0.138, wspace=0.062) # adjust the Figure in rp
    axs.fig.text(0.5, 0.04, 'Group', ha='center', va='center')
    axs.fig.text(0.01, 0.5,  'Relative powers', ha='center', va='center',rotation='vertical')
    if plot:
        plt.show()
    if save==True:
        plt.savefig('Manipulacion- Rois-Componentes de todas las DB\Graficos-Components\{name_band}_Components_{id}.png'.format(name_band=name_band,id=id))
        plt.close()
    
    return 



data_Comp=pd.read_feather(r"Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados.feather")#Datos con sujetos sin datos vacios
data_Comp1=pd.read_feather(r"Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\Datos_componentes_formatolargo_filtrados_sin_atipicos.feather")#Datos con sujetos sin datos vacios

bands= data_Comp['Band'].unique()
for band in bands:
    d_banda=data_Comp[data_Comp['Band']==band]
    d_banda1=data_Comp1[data_Comp1['Band']==band]
    graphic_component(d_banda,band,'con datos atipicos',num_columns=4,save=True,plot=False)
    graphic_component(d_banda1,band,'sin datos atipicos',num_columns=4,save=True,plot=False)

print('Graficos Componentes guardados')

        