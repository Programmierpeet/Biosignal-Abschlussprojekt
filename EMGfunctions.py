import Lab3Functions as l3f
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps
import scipy as scipy
# import matplotlib.colors as mcolors
# import matplotlib.gridspec as gridspec

def offset(array):
    '''
    Offset Berechnung dur Substraktion des Mittelwerts von einzelnen Signalen
    '''
    mean = np.mean(array)
    offset_emg = np.zeros(len(array))

    for i in range(len(array)):
        offset_emg[i] = array[i] - mean
    
    return offset_emg, mean

def plot_twotogether(y_1, y_2, time, figname, title1, title2):#figname and titles as strings
    '''
    Zwei plots nebeneinander, in Subplots sind Rasterkoordinaten
    '''

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=False, layout = 'constrained')
    x = [i/1000 for i in time]
    ax1.plot(x, y_1)
    ax2.plot(x, y_2)
    ax1.set_title(title1)
    ax2.set_title(title2)

    ax1.set_xlabel('Time / s')
    ax2.set_xlabel('Time / s')
    ax1.set_ylabel('EMG / mV')
    ax2.set_ylabel('EMG / mV')

    plt.savefig(figname + '.png')
    plt.savefig(figname + '.eps')
    plt.show()


def filter(filter_order, array, Wn_array, btype, fs_int): #Butterworth Tiefpass 4. Ordnung
    '''
    Filtern der Daten mit einem Bandpassfilter
    '''
    b , a = sps.butter (filter_order , Wn_array, btype= btype ,analog = False, fs=fs_int )
    filter_data = sps.filtfilt( b , a , x = array)
    return filter_data

def mean_of_burst(envelope, start, end):
    array = []
    for i in range(len(start)):
            burst = envelope[start[i]:end[i]]
            array.append(np.mean(burst))
    return array

def mean_of_all_bursts(envelope, start, end):
    array = []
    for i in range(len(start)):
            burst = envelope[start[i]:end[i]]
            burst_mean = np.mean(burst)
            array.append(burst_mean)
    return np.mean(array)

def slices_of_bursts(filtered_emg, start_index, end_index):

    start_burst = filtered_emg[start_index:(start_index+250)]
    mid_burst = filtered_emg[(int((end_index+start_index)/2-125)):(int((end_index+start_index)/2+125))]
    end_burst = filtered_emg[(end_index-250):end_index]

    return start_burst, mid_burst, end_burst

def power_and_frequencies(power, frequencies, figname, burst):
    plt.xlabel('Frequency / Hz')
    plt.ylabel('Power / dB')
    plt.title('Power Spectrum ' + burst)
    plt.plot(frequencies, y_power, label = 'unfiltered power')
    filtered_power = filter(4, power, 0.1, 'lowpass', None)
    y_filtered = [i/10 for i in filtered_power]
    y_power = [i/10 for i in power]
    plt.plot(frequencies, y_filtered, linestyle = 'dashdot', label = 'filtered power', color = 'red')
    plt.legend()
    plt.savefig(figname + '.png')
    plt.savefig(figname + '.eps')
    plt.show()

def power_and_frequencies_median(power, frequencies, figname, median):
    
    filtered_power = filter(4, power, 0.1, 'lowpass', None)

    fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=False, layout = 'constrained')
    y_filteredlist = [i/10 for i in filtered_power]
    y_filtered = np.array(y_filteredlist)

    #y_power = [i/10 for i in power]
    ax1.plot(frequencies, y_filtered, label = 'filtered power')
    ax1.vlines(median, 0, y_filtered[y_filtered.argmax(axis=0)], label = 'median frequency', color = 'r', linestyles='dashdot')

    ax1.set_xlabel('Frequency / Hz')
    ax1.set_ylabel('Power / dB')
    plt.legend()
    plt.title('Filtered Power Spectrum with Median')
    plt.savefig(figname + '.png')
    plt.savefig(figname + '.eps')
    plt.show()

def median_freq(power, frequencies):
    area_freq = scipy.integrate.cumtrapz(power, frequencies, initial = 0)
    total_power = area_freq[-1]
    median_freq = frequencies[np.where(area_freq >= total_power/2)[0][0]]
    return median_freq

def fatigue_frequencies_median(power_1, frequencies_1, power_2, frequencies_2, power_3, frequencies_3 ,figname, median1, median2, median3):
    filtered_power_1 = filter(4, power_1, 0.01, 'lowpass', None) 
    filtered_power_2 = filter(4, power_2, 0.01, 'lowpass', None) 
    filtered_power_3 = filter(4, power_3, 0.01, 'lowpass', None) 
    y_filtered1list = [i/10 for i in filtered_power_1]
    y_filtered2list = [i/10 for i in filtered_power_2]
    y_filtered3list = [i/10 for i in filtered_power_3]

    y_filtered1 = np.array(y_filtered1list)
    y_filtered2 = np.array(y_filtered2list)
    y_filtered3 = np.array(y_filtered3list)

    #y_power = [i/10 for i in power]
    plt.plot(frequencies_1, y_filtered1, label = 'first filtered power', color = 'tab:blue')
    plt.plot(frequencies_2, y_filtered2, label = 'second filtered power', color = 'r', linestyle = 'dashed')
    plt.plot(frequencies_3, y_filtered3, label = 'third filtered power', color = 'g', linestyle = 'dotted')


    plt.vlines(median1, 0, y_filtered1[y_filtered1.argmax(axis=0)], label = 'first median frequency', color = 'tab:blue', linestyles='solid')
    plt.vlines(median2, 0, y_filtered2[y_filtered2.argmax(axis=0)], label = 'second median frequency', color = 'r', linestyles='dashed')
    plt.vlines(median3, 0, y_filtered3[y_filtered3.argmax(axis=0)], label = 'third median frequency', color = 'g', linestyles='dotted')

    plt.xlabel('Frequency / Hz')
    plt.ylabel('Power / dB')
    plt.legend()
    plt.title('Filtered Power Spectrum with Median')
    plt.savefig(figname + '.png')
    plt.savefig(figname + '.eps')
    plt.show()

def plot_all_togethert(time, y_1, y_2, title1, title2, y_4, title4, y_6, title6, y_8, title8, figname):
    
    fig, ax = plt.subplots(5, sharex=True, sharey=False, figsize = (8,8))
    x = [i/1000 for i in time]
    fig.tight_layout(pad = 3)
    ax[0].set_title(title1)
    ax[0].plot(x, y_1)
    #ax[0,0].set_xlabel('Time / s')
    ax[0].set_ylabel('EMG / mV')
    
    ax[1].set_title(title2)
    ax[1].plot(x, y_2)
    #ax[0,1].set_xlabel('Time / s')
    ax[1].set_ylabel('EMG / mV')

    # ax[1,0].set_title(title3)
    # ax[1,0].plot(x, y_3)
    # #ax[1,0].set_xlabel('Time / s')
    # ax[1,0].set_ylabel('EMG / mV')

    ax[2].set_title(title4)
    ax[2].plot(x, y_4)
    #ax[1,1].set_xlabel('Time / s')
    ax[2].set_ylabel('EMG / mV')
        
    # ax[2,0].set_title(title5)
    # ax[2,0].plot(x, y_5)
    # #ax[2,0].set_xlabel('Time / s')
    # ax[2,0].set_ylabel('EMG / mV')

    ax[3].set_title(title6)
    ax[3].plot(x, y_6)
    #ax[2,1].set_xlabel('Time / s')
    ax[3].set_ylabel('EMG / mV')

    # ax[3,0].set_title(title7)
    # ax[3,0].plot(x, y_7)
    # ax[3,0].set_xlabel('Time / s')
    # ax[3,0].set_ylabel('EMG / mV')

    ax[4].set_title(title8)
    ax[4].plot(x, y_8)
    ax[4].set_xlabel('Time / s')
    ax[4].set_ylabel('EMG / mV')

    fig.align_ylabels()
    plt.savefig(figname + '.png')
    plt.savefig(figname + '.eps')
    plt.show()

def power_and_frequencies_median_with_unfitlered(power, frequencies, figname, median):
    
    filtered_power = filter(4, power, 0.1, 'lowpass', None)
    


    fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=False, layout = 'constrained')
    y_filteredlist = [i/10 for i in filtered_power]
    y_filtered = np.array(y_filteredlist)
    y_power = [i/10 for i in power]
    ax1.plot(frequencies, y_filtered, label = 'filtered power', linestyle = 'dashed', color = 'r')
    ax1.plot(frequencies, y_power, label = 'unfiltered power', linestyle = 'solid', color = 'tab:blue')
    ax1.vlines(median, 0, y_filtered[y_filtered.argmax(axis=0)], label = 'median frequency', color = 'g', linestyles='dashdot')

    ax1.set_xlabel('Frequency / Hz')
    ax1.set_ylabel('Power / dB')
    plt.legend()
    plt.title('Filtered Power Spectrum with Median')
    plt.savefig(figname + '.png')
    plt.savefig(figname + '.eps')
    plt.show()