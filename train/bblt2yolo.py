import os
from os import walk, getcwd
from PIL import Image

classes = ["hocsinh"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]

    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

"""-------------------------------------------------------------------"""

""" Configure Paths"""
mypath = "Labels/"
outpath = "Labels/voc/"

for i in range(len(classes)):
    cls = classes[i]
    cls_id = i + 1

    wd = getcwd()
    list_file = open('%s/%s_%s_list.txt'%(wd, cls, cls_id), 'w')

    """ Get input text file list """
    txt_name_list = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        if (dirpath == (mypath + '%03d'%cls_id)):
            txt_name_list.extend(filenames)
            if not os.path.exists(outpath + '%03d'%cls_id):
                os.makedirs(outpath + '%03d'%cls_id)
    print(txt_name_list)

    """ Process """
    for txt_name in txt_name_list:
        """ Open input text files """
        txt_path = mypath + '%03d'%cls_id + '/' + txt_name
        print("\n")
        print("Input:" + txt_path)
        txt_file = open(txt_path, "r")
        lines = txt_file.read().split('\n')

        """ Open output text files """
        txt_outpath = outpath + '%03d'%cls_id + '/' + txt_name
        print("Output:" + txt_outpath)
        txt_outfile = open(txt_outpath, "w")
        img_path = str('Images/%03d/%s.JPEG'%(cls_id, os.path.splitext(txt_name)[0]))
        im=Image.open(img_path)
        w= int(im.size[0])
        h= int(im.size[1])
        print(w, h, '\n')

        """ Convert the data to YOLO format """
        ct = 0
        for line in lines:
            elems = line.split(' ')
            if(len(elems) == 4):
                ct = ct + 1
                print(line)
                print(elems)
                xmin = elems[0]
                xmax = elems[2]
                ymin = elems[1]
                ymax = elems[3]
                #
                #t = magic.from_file(img_path)
                #wh= re.search('(\d+) x (\d+)', t).groups()

                #w = int(xmax) - int(xmin)
                #h = int(ymax) - int(ymin)
                # print(xmin)
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert((w,h), b)
                print(bb)
                txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

        """ Save those images with bb into list"""
        if(ct != 0):
            list_file.write('Images/%03d/%s.JPEG\n'%(cls_id, os.path.splitext(txt_name)[0]))

    list_file.close()