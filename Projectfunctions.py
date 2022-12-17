import pandas as pd
import EMGfunctions as emgf
import numpy as np
import matplotlib.pyplot as plt
import Lab3Functions as l3f
import seaborn as sns
import Projectfunctions as pfn

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

def get_mean_ampliude(Datab, Datat):
    envelope_chest = []
    envelope_triceps = []
    for i in range(5):
        envelope_chest_data = data_to_envelope(Datab[i])
        envelope_triceps_data = data_to_envelope(Datat[i])

        area_chest = sum(envelope_chest_data)/len(envelope_chest_data)
        area_triceps= sum(envelope_triceps_data)/len(envelope_chest_data)

        envelope_chest.append(area_chest)
        envelope_triceps.append(area_triceps)
        
    return envelope_chest, envelope_triceps   

def barplot(envelope_chest, envelope_triceps, Name, first, second, third):
    # j = {x: [random.choice(["ASB", "Violence", "Theft", "Public Order", "Drugs"]
    #                    ) for j in range(300)] for x in s}
    # df = pd.DataFrame(j)
    chest_activation = envelope_chest
    triceps_activation = envelope_triceps
    index = np.arange(5)
    bar_width = 0.35

    fig, ax = plt.subplots()
    ax.bar(index, chest_activation, bar_width,
                    label="chest activation", color = '#21B2DE', edgecolor= '#12627A')

    ax.bar(index+bar_width, triceps_activation, bar_width, label="triceps activation", color = '#DE4D21', edgecolor = '#7A2A12')
    max = np.max(triceps_activation)
    plt.yticks(np.arange(0, max+25, 10)) 
    ax.set_xlabel('Excersice')
    ax.set_ylabel('Mean of Amplitude / mV')
    #ax.set_title('Crime incidence by season, type')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels([first, second, third, "Normal ROM", "Higher ROM"])
    ax.legend(loc = 'upper right')
    plt.savefig('Grafiken/'+ Name + '.png')
    plt.savefig('Grafiken/'+ Name + '.eps')
    plt.show()

def cross_correlation(Chest, Triceps, Time, Name):
    dt = 0.01
    fig, axs = plt.subplots(2, 1)

    offset_chest, mean= emgf.offset(Chest)
    offset_triceps, mean= emgf.offset(Triceps)

    chest_filtered = emgf.filter(4, offset_chest, [20,450], 'bandpass', 1000)
    triceps_filtered = emgf.filter(4, offset_triceps, [20,450], 'bandpass', 1000)

    x = [(i/1000) for i in Time]
    axs[0].plot(x, triceps_filtered, color = '#DE4D21', linestyle = '-')
    axs[0].plot(x, chest_filtered, color = '#21B2DE')
    axs[0].set_xlim(0, int(max(x)), 10)
    axs[0].set_xlabel('Time / s')
    axs[0].set_ylabel('Chest and Triceps / mV')
    axs[0].grid(True)

    cxy, f = axs[1].cohere(chest_filtered, triceps_filtered, 256, 1. / dt, color = '#040404')

    axs[1].set_ylabel('Coherence')
    axs[1].set_xlabel('Frequenzy / Hz')
    fig.tight_layout()
    plt.savefig('Grafiken/'+ Name + '.png')
    plt.savefig('Grafiken/'+ Name + '.eps')
    plt.show()

def fft_plot(Chest, Triceps, Name):


    chest_p, chest_f = l3f.get_power(Chest, 500)
    triceps_p, triceps_f = l3f.get_power(Triceps, 500)

    median_chest = emgf.median_freq(chest_p, chest_f)
    median_triceps = emgf.median_freq(triceps_p, triceps_f)

    low_c = emgf.filter(4, chest_p, 0.05, 'lowpass', None)
    low_t = emgf.filter(4, triceps_p, 0.05, 'lowpass', None)

    dB_adjust_c = [i/10 for i in low_c]
    dB_adjust_t = [i/10 for i in low_t]

    fig, axs = plt.subplots(2, 1, sharex= True)
    axs[0].plot(chest_f, dB_adjust_c, color = '#DE4D21', linestyle = '-', label = 'Chest')
#    axs[0].set_xlabel('Frequency / Hz')
    axs[0].set_ylabel('Power Spectrum / dB')
    axs[0].legend(loc = 'upper right')
    #axs[0].set_xlim(0,300)
    axs[0].vlines(median_chest, 0, dB_adjust_c[np.array(dB_adjust_c).argmax(axis=0)], label = 'median frequency', color = 'r', linestyles='dashdot')

    axs[1].plot(triceps_f, dB_adjust_t, color = '#21B2DE', label = 'Triceps')
    axs[1].set_ylabel('Power Spectrum / dB')
    axs[1].set_xlabel('Frequenzy / Hz')
    axs[1].legend(loc = 'upper right')
    axs[1].vlines(median_triceps, 0, dB_adjust_t[np.array(dB_adjust_t).argmax(axis=0)], label = 'median frequency', color = 'r', linestyles='dashdot')
    #axs[1].set_xlim(0,300)

    fig.tight_layout()
    plt.savefig('Grafiken/'+ Name + '.png')
    plt.savefig('Grafiken/'+ Name + '.eps')
    plt.show()

def fatigue_data_median_freq(DataB, DataT):
    chest_frequency_median = []
    triceps_frequency_median = []
    timepoint = 0
    for i in range(15):
        #print(i)
        chest_p, chest_f = l3f.get_power(DataB[timepoint:(int(len(DataB)/15)+timepoint)], 500)
        triceps_p, triceps_f = l3f.get_power(DataT[timepoint:(int(len(DataB)/15)+timepoint)], 500)

        median_chest = emgf.median_freq(chest_p, chest_f)
        median_triceps = emgf.median_freq(triceps_p, triceps_f)

        chest_frequency_median.append(median_chest)
        triceps_frequency_median.append(median_triceps)

        timepoint = int(len(DataB)/15+timepoint)

    return chest_frequency_median, triceps_frequency_median

def plot_fatigue(freq_median_triceps, Name):

    x = np.linspace(1,15, 15)

    y_t = freq_median_triceps

    df_t = pd.DataFrame({'x':x,'y':y_t})
    sns.lmplot(x='x',y='y', data=df_t, order=2)

    plt.xlabel('Samples')
    plt.ylabel('Frequenzy / Hz')
    plt.savefig('Grafiken/'+ Name + '.png')
    plt.savefig('Grafiken/'+ Name + '.eps')
    plt.show()

def plot_comparison(chest, triceps, time, name):
    for i in range(5):
        Chest= pfn.data_to_envelope(chest[i])
        Triceps= pfn.data_to_envelope(triceps[i])


        plt.figure()
        plt.plot(time[i]/1000, Chest, color = '#21B2DE', label='Chest')
        plt.plot(time[i]/1000, Triceps, color = '#DE4D21', label= 'Triceps')
        plt.xlabel('Time / s')
        plt.ylabel('Amplitude / µV')
        plt.legend(loc= 'upper right')
        plt.savefig('Grafiken/'+ name + '.eps')

        plt.show()