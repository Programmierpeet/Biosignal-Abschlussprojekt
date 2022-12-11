import pandas as pd
import EMGfunctions as emgf
import numpy as np

def txt_to_df(txt):
    df =  pd.read_csv("./Daten/"+txt, sep = '\t', names = ['brust', 'trizeps', 'millis'])
    return df

def data_to_envelope(array):
    #correcting offset
    offset, mean = emgf.offset(array)
    #bandpass
    filtered = emgf.filter(4, offset, [20,450], 'bandpass', 1000)
    #rectified
    rectified = np.abs(filtered) 
    #envelope
    envelope = emgf.filter(4, rectified, 0.01, 'lowpass', None)
    return envelope

def data_to_filtered(array):
    #correcting offset
    offset, mean = emgf.offset(array)
    #bandpass
    filtered = emgf.filter(4, offset, [20,450], 'bandpass', 1000)
    return filtered

def data_to_rectified(array):
        #correcting offset
    offset, mean = emgf.offset(array)
    #bandpass
    filtered = emgf.filter(4, offset, [20,450], 'bandpass', 1000)
    #rectified
    rectified = np.abs(filtered) 
    return rectified

def get_data(Name):
    envelope_brust = []
    envelope_trizeps = []
    millis = []
    for i in range(1,6):
        Probant = txt_to_df(Name+'{0}.txt'.format(i))

        Brust = Probant.loc[:,'brust']
        Trizeps = Probant.loc[:,'trizeps']
        Millis = Probant.loc[:,'millis']

        envelope_brust.append(Brust)
        envelope_trizeps.append(Trizeps)
        millis.append(Millis)

    return envelope_brust, envelope_trizeps, millis

def integral(array, start, end):
    #finding area under the curve
    integral = sum(array[start:end])
    return integral

def find_relation(DataB, DataT, Normal_s, Normal_e, Narrow_s, Narrow_e, Wide_s, Wide_e):
    b_envelope = []
    t_envelope = []
    for i in range(3):
        b_filtered = data_to_envelope(DataB[i])
        t_filtered = data_to_envelope(DataT[i])
        b_envelope.append(b_filtered)
        t_envelope.append(t_filtered)

    area_chest_normal = []
    area_triceps_normal = []
    for i in range(3):
        chestNormal = integral(b_envelope[0], Normal_s[i], Normal_e[i])
        tricepsNormal = integral(t_envelope[0], Normal_s[i], Normal_e[i])
        area_chest_normal.append(chestNormal)
        area_triceps_normal.append(tricepsNormal)

    area_chest_narrow = []
    area_triceps_narrow = []
    for i in range(3):
        chest = integral(b_envelope[1], Narrow_s[i], Narrow_e[i])
        triceps = integral(t_envelope[1], Narrow_s[i], Narrow_e[i])
        area_chest_narrow.append(chest)
        area_triceps_narrow.append(triceps)

    area_chest_wide = []
    area_triceps_wide = []
    for i in range(3):
        chest = integral(b_envelope[2], Wide_s[i], Wide_e[i])
        triceps = integral(t_envelope[2], Wide_s[i], Wide_e[i])
        area_chest_wide.append(chest)
        area_triceps_wide.append(triceps)

    relation_normal = np.array(area_triceps_normal)/np.array(area_chest_normal)
    relation_narrow = np.array(area_triceps_narrow)/np.array(area_chest_narrow)
    relation_wide = np.array(area_triceps_wide)/np.array(area_chest_wide)

    return relation_normal, relation_narrow, relation_wide

def relation3and4(Datab, Datat):
    envelope_chest = []
    envelope_triceps = []
    for i in range(3,5):
        envelope_chest_data = data_to_envelope(Datab[i])
        envelope_triceps_data = data_to_envelope(Datat[i])
        area_chest = sum(envelope_chest_data)
        area_triceps= sum(envelope_triceps_data)
        envelope_chest.append(area_chest)
        envelope_triceps.append(area_triceps)

    relation_3 = np.array(envelope_triceps[0])/np.array(envelope_chest[0])
    relation_4 = np.array(envelope_triceps[1])/np.array(envelope_chest[1])
    return relation_3, relation_4