import Projectfunctions as pfn
import Lab3Functions as l3f
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import EMGfunctions as emgf
import scipy.signal as sps
import scipy as scipy
import os

'''
    Noah 1,2,3:
        0 = Normal
        1 = Narrow
        2 = Wide
    Peter 1,2,3:
        0 = Wide
        1 = Narrow
        2 = Normal
    Jonny 1,2,3:
        0 = Narrow
        1 = Wide
        2 = Normal
'''
Noahb, Noaht, Noahm = pfn.get_data('Noah')
Peterb, Petert, Peterm = pfn.get_data('Peter')
Jonnyb, Jonnyt, Jonnym = pfn.get_data('Jonny')


# Nnarrowt_s, Nnarrowt_e, Nwidet_s, Nwidet_e,Pnormalt_s, Nnormalt_e = l3f.get_bursts(Jonnyt[0], Jonnyt[1], Jonnyt[2]) 
# print(Nnarrowt_s)
# print(Nnarrowt_e)
# print(Nwidet_s)
# print(Nwidet_e)
# print(Pnormalt_s)
# print(Nnormalt_e)

#Finding the indices of array to integrate over right interval
#becuase the relative strength of chest and triceps to eachother are measured, exact values are not important

#Noah
Nnormalt_s = [386, 1158, 1993]
Nnormalt_e = [1153, 1968, 2774]
Nnarrowt_s = [858, 1630, 2499]
Nnarrowt_e = [1519, 2462, 3270]
Nwidet_s = [350, 1057, 1895]
Nwidet_e = [1050, 1851, 2481]

#peter
Pwidet_s = [156,  885, 1463]
Pwidet_e = [850, 1453, 2327]
Pnarrowt_s = [175,  900, 1761]
Pnarrowt_e = [848, 1684, 2468]
Pnormalt_s = [215,  692, 1358]
Pnormalt_e = [ 677, 1334, 2129]

#Jonny
Jnarrowt_s = [ 390,  831, 1472]
Jnarrowt_e = [811, 1449, 2216]
Jwidet_s = [154, 1126, 1701]
Jwidet_e = [1075, 1644, 2206]
Jnormalt_s = [375,  900, 1462]
Jnormalt_e = [ 809, 1437, 2127]

#For integration envelope is needed
# #Spannung über die Zeit = Vs = Weber? -> mV, only addition done

relation_narrowJ, relation_wideJ, relation_normalJ = pfn.find_relation(Jonnyb, Jonnyt, Jnarrowt_s, Jnarrowt_e, Jwidet_s, Jwidet_e, Jnormalt_s, Jnormalt_e)
relation_normalN, relation_narrowN, relation_wideN = pfn.find_relation(Noahb, Noaht, Nnormalt_s, Nnormalt_e, Nnarrowt_s, Nnarrowt_e, Nwidet_s, Nwidet_e)
relation_wideP, relation_narrowP, relation_normalP = pfn.find_relation(Peterb, Petert, Pwidet_s, Pwidet_e, Pnarrowt_s, Pnarrowt_e, Pnormalt_s, Pnormalt_e)

# print('1) normal, 2) narrow, 3) wide')
# print('Herr roth')
# print(np.mean(relation_normalJ))
# print(np.mean(relation_narrowJ))
# print(np.mean(relation_wideJ))

# print('herr rettenbacher')
# print(np.mean(relation_normalN))
# print(np.mean(relation_narrowN))
# print(np.mean(relation_wideN))

# print('herr thurner')
# print(np.mean(relation_normalP))
# print(np.mean(relation_narrowP))
# print(np.mean(relation_wideP))

#Comparison of whole Triceps and Chest Work in Experiment 4 and 5
# relation3N, relation4N= pfn.relation3and4(Noahb, Noaht)
# relation3P, relation4P = pfn.relation3and4(Peterb, Petert)
# relation3J, relation4J = pfn.relation3and4(Jonnyb, Jonnyt)
# print('Noah: ',relation3N,'Peter: ', relation3P,'Jonny: ',  relation3J)
# print('Noah ROM: ',relation4N, 'Peter ROM: ',relation4P, 'Jonny ROM: ', relation4J)

#Um Amplituden zu vergleichen, sollen Zeitbereiche ignoriert werden, indem der Durchschnitt aus den Werten berechnet wird
# amp_chest_Noah, amp_triceps_Noah = pfn.get_mean_ampliude(Noahb, Noaht)
# amp_chest_Jonny, amp_triceps_Jonny = pfn.get_mean_ampliude(Jonnyb, Jonnyt)
# amp_chest_Peter, amp_triceps_Peter = pfn.get_mean_ampliude(Peterb, Petert)

# print(amp_chest_Noah, amp_triceps_Noah)
# print(amp_chest_Jonny, amp_triceps_Jonny)
# print(amp_chest_Peter, amp_triceps_Peter)

# pfn.barplot(amp_chest_Noah, amp_triceps_Noah, 'Noah_comparison', 'Normal', 'Narrow', 'Wide')
# pfn.barplot(amp_chest_Jonny, amp_triceps_Jonny, 'Jonny_comparison', 'Narrow', 'Wide', 'Normal')
# pfn.barplot(amp_chest_Peter, amp_triceps_Peter, 'Peter_comparison', 'Wide', 'Narrow', 'Normal')

#Cross correlation after adding bandpass to raw data and deleting offset
#pfn.cross_correlation(Noahb[1], Noaht[1], Noahm[1], 'Noah_cross_correlation')

# pfn.fft_plot(Noahb[0], Noaht[0], 'Noah_fft_plot_normal')
# pfn.fft_plot(Noahb[1], Noaht[1], 'Noah_fft_plot_narrow')
# pfn.fft_plot(Noahb[2], Noaht[2], 'Noah_fft_plot_wide')
# pfn.fft_plot(Noahb[3], Noaht[3], 'Noah_fft_plot_normalrom')
# pfn.fft_plot(Noahb[4], Noaht[4], 'Noah_fft_plot_widerom')

#plot change of median frequency over time
# chest_med_freq_normalrom, triceps_med_freq_normalrom = pfn.fatigue_data_median_freq(Peterb[3], Petert[3])
# chest_med_freq_rom, triceps_med_freq_rom = pfn.fatigue_data_median_freq(Peterb[4], Petert[4])
# print('chest_freq: ', chest_med_freq_normalrom)
# print('triceps_freq: ', triceps_med_freq_normalrom)


# pfn.plot_fatigue(triceps_med_freq_normalrom, 'Peter_triceps_fatigue')
# pfn.plot_fatigue(triceps_med_freq_rom, 'Peter_triceps_fatigue_rom')

# pfn.plot_fatigue(chest_med_freq_normalrom, 'Peter_chest_fatigue')
# pfn.plot_fatigue(chest_med_freq_rom, 'Peter_chest_fatigue_rom')

# enveb= pfn.data_to_envelope(Noahb[4])
# envet= pfn.data_to_envelope(Noaht[4])


# plt.figure()
# plt.plot(Noahm[4]/1000, enveb, color = '#21B2DE', label='Chest')
# plt.plot(Noahm[4]/1000, envet, color = '#DE4D21', label= 'Triceps')
# plt.xlabel('Time / s')
# plt.ylabel('Amplitude / µV')
# plt.legend(loc= 'upper right')
# plt.savefig('Noah_Comparison_bigROM.eps')

# plt.show()

#pfn.plot_comparison(Noahb, Noaht, Noahm, 'Noah_Comparison')
