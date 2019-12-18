##Siddharth Jain

import csv
from datetime import datetime
import glob
import h5py
import matplotlib.pyplot as plt
import os
import pytz
from scipy.signal import medfilt

## function for traversing the directory tree
def traverse(name, group, groups):
    for key in list(group.keys()):
        if (isinstance(group[key], h5py._hl.group.Group)):
            try:
                traverse(name+'/'+key, group[key], groups)
            except TypeError as err:
                # print('TypeError for group %s' %(key))
                # print(err)
                pass
        elif (isinstance(group[key], h5py._hl.dataset.Dataset)):
            try:
                dataset = group[key]
                groups.append([name, key, dataset.size, dataset.shape, dataset.dtype])
            except TypeError as err:
                # print('TypeError for dataset %s, %s, %d, %s' %(name, key, dataset.size, str(dataset.shape)))
                # print(err)
                pass

os.chdir("./")
for file in glob.glob("*.h5"):
    with h5py.File(file, 'r') as f:
        ## part 1
        timestamp = int(file.split('_')[0])
        dt = datetime.fromtimestamp(timestamp/10**9)
        utcdt = dt.astimezone(pytz.utc)
        cerndt = dt.astimezone(pytz.timezone('CET'))

        ## part 2
        groups=[['Group', 'Dataset', 'Size', 'Shape', 'Type']]
        for key in list(f.keys()):
            traverse(key, f[key], groups)
        with open('datasets.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(groups)

        ## part 3
        streakImageData = f['AwakeEventData']['XMPP-STREAK']['StreakImage']['streakImageData'][()]
        height = f['AwakeEventData']['XMPP-STREAK']['StreakImage']['streakImageHeight'][()][0]
        width = f['AwakeEventData']['XMPP-STREAK']['StreakImage']['streakImageWidth'][()][0]
        image = medfilt(streakImageData.reshape(height, width), 3)
        plt.imshow(image)
        plt.savefig('image.png')