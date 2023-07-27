# Summer 2023
# Mitsuru Watanabe
# This file will compile discharged gas particles into data set
# Make sure to run particletracking.py {sim} {haloid} to track particles before running
# make sure to connect to quirm then activate anaconda environment


import tqdm
import time
from compiler import *


start = time.time()
# keys = ['h148_13','h148_28','h148_37','h148_45','h148_68','h148_80','h148_283',
#         'h148_278','h148_329','h229_20','h229_22','h229_23','h229_27','h229_55',
#         'h242_24','h242_41','h242_80','h329_33','h329_137','h242_12','h242_30',
#         'h242_44','h148_3','h148_14','h148_36']


### These are Leo's original dataset
# keys = ['h148_12','h148_27','h148_34','h148_38','h148_55','h148_65','h148_249',
#         'h148_251','h148_282','h229_14','h229_18','h229_20','h229_22',
#         'h229_49','h242_21','h242_38','h242_69','h329_29','h329_117']

### Used SUmmer 2023 (exclude 'h242_401')
# keys = ['h148_10', 'h148_12', 'h148_2', 'h148_249', 'h148_251', 'h148_27', 'h148_282', 'h148_3', 'h148_34', 'h148_38', 'h148_4', 'h148_55',
#         'h148_6', 'h148_65', 'h229_14', 'h229_18', 'h229_20', 'h229_22', 'h229_49', 'h242_10', 'h242_21', 'h242_30', 'h242_38',
#         'h242_69', 'h242_8', 'h329_117', 'h329_29', 'h329_7']

keys = []        
print('Compiling sim gas into sets for the following keys:', keys)

for key in keys:
    sim = str(key[:4])
    haloid = int(key[5:])

    # #skipping the one I already have
    # if key == 'h148_10':
    #     continue
    
    # note that predischarged, discharged, etc. are automatically concatenated.
    predischarged, discharged, accreted = calc_discharged(sim, haloid, save=True, verbose=False)
    hotpredischarged = calc_hot_predischarged(sim, haloid, save=True, verbose=False)
    reaccreted = calc_reaccreted(sim, haloid, save=True, verbose=False)

end = time.time()
print("Program finished execution: ", end - start, " s")

# 'h148_2' took 39 hrs to execute