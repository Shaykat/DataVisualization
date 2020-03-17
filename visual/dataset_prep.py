import urllib
import csv
import os.path as pth
import xml.etree.ElementTree as ET


data = []
try:
    with open('/Users/mutalabshaykat/Downloads/covid_19_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) > 0:
                data.append(row)
except IOError:
    print("File 'annotations.csv' is no exist")

# images = np.zeros((len(files) * len(files[0]), 1650, 1275), float)
for row in data:
    pass
print(len(data))