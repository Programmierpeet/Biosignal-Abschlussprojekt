import Projectfunctions as pfn
import Lab3Functions as l3f
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import EMGfunctions as emgf
import scipy.signal as sps
import scipy as scipy
import os

# #envelope of data.
# envelope_brust1 = pfn.data_to_envelope(Brust1)
# envelope_trizeps1 = pfn.data_to_envelope(Trizeps1)

# #filtered data
# filtered_brust1 = pfn.data_to_filtered(Brust1)
# filtered_trizeps1 = pfn.data_to_filtered(Trizeps1)

# #rectified data
# rec_brust1 = pfn.data_to_rectified(Brust1)
# rec_trizeps1 = pfn.data_to_rectified(Trizeps1)

# plt.figure()
# plt.plot(Millis1, Brust1)
# plt.plot(Millis1, Trizeps1)
# plt.title('45° Jonny')
# plt.savefig('Jonnyraw.png')
# plt.show()

# plt.figure()
# plt.plot(Millis1, filtered_brust1)
# plt.plot(Millis1, filtered_trizeps1)
# plt.title('45° Jonny')
# plt.savefig('Jonnyfiltered.png')
# plt.show()

# plt.figure()
# plt.plot(Millis1, envelope_brust1)
# plt.plot(Millis1, envelope_trizeps1)
# plt.title('45° Jonny')
# plt.savefig('Jonnyenve.png')
# plt.show()

# plt.figure()
# plt.plot(Millis1, rec_brust1)
# plt.plot(P
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
# #Spannung über die Zeit = Vs = Weber?

relation_narrowJ, relation_wideJ, relation_normalJ = pfn.find_relation(Jonnyb, Jonnyt, Jnarrowt_s, Jnarrowt_e, Jwidet_s, Jwidet_e, Jnormalt_s, Jnormalt_e)
relation_normalN, relation_narrowN, relation_wideN = pfn.find_relation(Noahb, Noaht, Nnormalt_s, Nnormalt_e, Nnarrowt_s, Nnarrowt_e, Nwidet_s, Nwidet_e)
relation_wideP, relation_narrowP, relation_normalP = pfn.find_relation(Peterb, Petert, Pwidet_s, Pwidet_e, Pnarrowt_s, Pnarrowt_e, Pnormalt_s, Pnormalt_e)

print('1) normal, 2) narrow, 3) wide')
print('Herr roth')
print(np.mean(relation_normalJ))
print(np.mean(relation_narrowJ))
print(np.mean(relation_wideJ))

print('herr rettenbacher')
print(np.mean(relation_normalN))
print(np.mean(relation_narrowN))
print(np.mean(relation_wideN))

print('herr thurner')
print(np.mean(relation_normalP))
print(np.mean(relation_narrowP))
print(np.mean(relation_wideP))

#Comparison of whole Triceps and Chest Work in Experiment 4 and 5
relation3N, relation4N = pfn.relation3and4(Noahb, Noaht)
relation3P, relation4P = pfn.relation3and4(Peterb, Petert)
relation3J, relation4J = pfn.relation3and4(Jonnyb, Jonnyt)
print(relation3N, relation3P, relation3J)
print(relation4N, relation4P, relation4J)

plt.figure()
plt.plot(Jonnym[1], Jonnyb[1])
plt.plot(Jonnym[1], Jonnyt[1])
plt.title('45° Jonny')
plt.savefig('Grafiken/Jonnyrawr.png')
plt.show()