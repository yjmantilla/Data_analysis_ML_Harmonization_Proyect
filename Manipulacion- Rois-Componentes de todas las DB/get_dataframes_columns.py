import json
from bids import BIDSLayout
import numpy as np
import re
import pandas as pd
from bids.layout import parse_file_entities

BIOMARCADORES_CE = {
    'name':'BIOMARCADORES',
    #'input_path':r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS',
    'input_path':r'C:\Users\valec\OneDrive - Universidad de Antioquia\Datos MsC Verónica\BIOMARCADORES',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}
CHBMP = {
    'name':'CHBMP',
    'input_path':r'C:\Users\valec\OneDrive - Universidad de Antioquia\Datos MsC Verónica\CHBMP',
    'layout':{'extension':'.edf', 'task':'protmap','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60],},
    'group_regex':None,
    'events_to_keep':[65],
    'run-label':'restCE',
    'session':None
}
SRM = {
    'name':'SRM',
    'input_path':r'C:\Users\valec\OneDrive - Universidad de Antioquia\Datos MsC Verónica\SRM',
    'layout':{'extension':'.edf', 'task':'resteyesc','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[50]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}
DUQUE = {
    'name':'DUQUE',
    'input_path':r'C:\Users\valec\OneDrive - Universidad de Antioquia\Datos MsC Verónica\DUQUE',
    'layout':{'extension':'.vhdr', 'task':'resting','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':None,
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V'
}

def get_dataframe_columnsROI_SL(THE_DATASET): 
    '''Obtain data frames with SL of ROIs in different columns''' 
    input_path = THE_DATASET.get('input_path',None)
    task = THE_DATASET.get('layout',None).get('task',None)
    group_regex = THE_DATASET.get('group_regex',None)
    name = THE_DATASET.get('name',None)
    runlabel = THE_DATASET.get('run-label','')
    data_path = input_path
    layout = BIDSLayout(data_path,derivatives=True)
    layout.get(scope='derivatives', return_type='file')

    eegs_powers= layout.get(extension='.txt', task=task,suffix='norm', return_type='filename')
    eegs_powers = [x for x in eegs_powers if f'desc-channel[{runlabel}]_sl_band' in x]
    print('valelinda2')

    F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
    T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
    C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
    PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
    rois = [F,C,PO,T]
    roi_labels = ['F','C','PO','T']

    list_subjects = []
    for i in range(len(eegs_powers)):
        print(eegs_powers[i])
        with open(eegs_powers[i], 'r') as f:
            data = json.load(f)
        total_channels=np.array(data['channels'])
        bandas = data['bands']
        new_rois = []
        potencias_roi_banda=[]

        for roi in rois:
            channels = set(data['channels']).intersection(roi)
            new_roi = []
            for channel in channels:
                index=data['channels'].index(channel)
                new_roi.append(index)
            new_rois.append(new_roi)

        datos_1_sujeto = {}
        info_bids_sujeto = parse_file_entities(eegs_powers[i])
        datos_1_sujeto['participant_id'] = 'sub-'+info_bids_sujeto['subject']
        regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
        if group_regex:
            regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
            datos_1_sujeto['group'] = regex.string[regex.regs[-1][0]:regex.regs[-1][1]]
        else:
            datos_1_sujeto['group'] = 'Control'
        try:
            datos_1_sujeto['visit'] = info_bids_sujeto['session']
        except:
            datos_1_sujeto['visit']='V0'
        datos_1_sujeto['condition'] = info_bids_sujeto['task']
        for b,band in enumerate(bandas):
            # for c,channel in enumerate(total_channels):
            #     sl_promedio = np.average(np.array(data['sl'][band])[c])
            #     datos_1_sujeto[f'Channel_{total_channels[c]}_r{band.title()}']=sl_promedio
            for r,roi in enumerate(new_rois):
                sl_promedio_roi = np.average(np.array(data['sl'][band])[roi])
                datos_1_sujeto[f'SL_ROI_{roi_labels[r]}_{band.title()}']=sl_promedio_roi
        list_subjects.append(datos_1_sujeto)
    df = pd.DataFrame(list_subjects)
    df['database']=[name]*len(list_subjects)
    df.to_feather(r'{input_path}\derivatives\data_sl_column_ROI_norm_{name}.feather'.format(name=name,input_path=input_path))
    print('Done!')
def get_dataframe_columnsROI_Coherencia(THE_DATASET): 
    '''Obtain data frames with powers of ROIs in different columns''' 
    input_path = THE_DATASET.get('input_path',None)
    task = THE_DATASET.get('layout',None).get('task',None)
    group_regex = THE_DATASET.get('group_regex',None)
    name = THE_DATASET.get('name',None)
    runlabel = THE_DATASET.get('run-label','')
    data_path = input_path
    layout = BIDSLayout(data_path,derivatives=True)
    layout.get(scope='derivatives', return_type='file')
    eegs_powers= layout.get(extension='.txt', task=task,suffix='norm', return_type='filename')
    eegs_powers = [x for x in eegs_powers if f'desc-channel[{runlabel}]_coherence_band' in x]
    #eegs_powers = [x for x in eegs_powers if 'coherence_band' in x]

    F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
    T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
    C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
    PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
    rois = [F,C,PO,T]
    roi_labels = ['F','C','PO','T']

    list_subjects = []
    for i in range(len(eegs_powers)):
        print(eegs_powers[i])
        with open(eegs_powers[i], 'r') as f:
            data = json.load(f)
        total_channels=np.array(data['channels'])
        bandas = data['bands']
        new_rois = []
        potencias_roi_banda=[]

        for roi in rois:
            channels = set(data['channels']).intersection(roi)
            new_roi = []
            for channel in channels:
                index=data['channels'].index(channel)
                new_roi.append(index)
            new_rois.append(new_roi)

        datos_1_sujeto = {}
        info_bids_sujeto = parse_file_entities(eegs_powers[i])
        datos_1_sujeto['participant_id'] ='sub-'+info_bids_sujeto['subject']
        regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
        if group_regex:
            regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
            datos_1_sujeto['group'] = regex.string[regex.regs[-1][0]:regex.regs[-1][1]]
        else:
            datos_1_sujeto['group'] = 'Control'
        try:
            datos_1_sujeto['visit'] = info_bids_sujeto['session']
        except:
            datos_1_sujeto['visit']='V0'
        datos_1_sujeto['condition'] = info_bids_sujeto['task']
        for b,band in enumerate(bandas):
        
            c_promedio_roi = np.average(np.array(data['sl'][band])[1])
            datos_1_sujeto[f'Coherence_{band.title()}']=c_promedio_roi
            
        list_subjects.append(datos_1_sujeto)
    df = pd.DataFrame(list_subjects)
    df['database']=[name]*len(list_subjects)
    df.to_feather(r'{input_path}\derivatives\data_Coherence_column_norm_{name}.feather'.format(name=name,input_path=input_path))
    print('Done!')

##Para obtener los datos por columnas de SL por sujeto
# get_dataframe_columnsROI_SL(BIOMARCADORES_CE)
# get_dataframe_columnsROI_SL(DUQUE)
# get_dataframe_columnsROI_SL(CHBMP)
# get_dataframe_columnsROI_SL(SRM)

##Para obtener los datos por columnas de coherencia
#get_dataframe_columnsROI_Coherencia(BIOMARCADORES_CE)
#get_dataframe_columnsROI_Coherencia(DUQUE)
get_dataframe_columnsROI_Coherencia(CHBMP)
get_dataframe_columnsROI_Coherencia(SRM)