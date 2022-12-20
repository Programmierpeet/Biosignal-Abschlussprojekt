for i in range(15):
    print(i)

import Projectfunctions as pfn
import numpy as np

# envelope_brust = []
# envelope_trizeps = []
# millis = []
# for i in range(1,4):
#     Probant = pfn.txt_to_df('Noah'+'{0}.txt'.format(i))
#     #1484, 1514, 1447
#     brust = Probant.loc[:, 'millis']
#     envelope_brust.append(brust)
    
# print(envelope_brust)
a = np.array([1,2,3,4,5])
print(a[-3:])