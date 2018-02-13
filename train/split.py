import glob, os
from os import walk, getcwd

classes = ["hocsinh"]

# Directory where the data will reside, relative to 'darknet.exe'
path_data = 'Images/'

# Percentage of images to be used for the test set
percentage_test = 20

# Create and/or truncate train.txt and test.txt
file_train = open('train.txt', 'w')
file_test = open('test.txt', 'w')

# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)

for i in range(len(classes)):
    cls = classes[i]
    cls_id = i + 1

    txt_name_list = []
    for (dirpath, dirnames, filenames) in walk(path_data):
        if (dirpath != (path_data + '%03d'%cls_id)):
            continue
        for fname in filenames:
            if (os.path.splitext(fname)[1] != '.JPEG'):
                continue
            if counter == index_test:
                counter = 1
                file_test.write('Images/%03d/%s.JPEG\n'%(cls_id, os.path.splitext(fname)[0]))
            else:
                file_train.write('Images/%03d/%s.JPEG\n'%(cls_id, os.path.splitext(fname)[0]))
                counter = counter + 1
