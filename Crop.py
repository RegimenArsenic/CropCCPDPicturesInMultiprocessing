#-*-coding:GBK -*- 
import cv2
import os
import time
import datetime
import multiprocessing
from multiprocessing import Process
from multiprocessing import Queue

basePath="H:/CCPD/CCPD2019/ccpd_base/"
outputPath="H:/CCPD/images/"
filename="./train.txt"
threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5"]
workQueue = Queue()
threads = []
exitFlag= multiprocessing.Value('i', 0)

def new_label(old_label):
    provinces = ["��", "��", "��", "��", "��", "��", "��", "��", "��", "��", "��", "��",
                 "��", "��", "��", "³", "ԥ", "��", "��", "��", "��",
                 "��", "��", "��", "��", "��", "��", "��", "��", "��", "��", "��", "ѧ",
                 "O"]

    ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
           'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']

    # code 2
    char_dict = {"��": 0, "��": 1, "��": 2, "��": 3, "��": 4, "��": 5, "��": 6, "��": 7, "��": 8, "��": 9, "��": 10,
                 "��": 11, "��": 12, "��": 13, "��": 14, "³": 15, "ԥ": 16, "��": 17, "��": 18, "��": 19, "��": 20,
                 "��": 21, "��": 22, "��": 23, "��": 24, "��": 25, "��": 26, "��": 27, "��": 28, "��": 29, "��": 30,
                 "0": 31, "1": 32, "2": 33, "3": 34, "4": 35, "5": 36, "6": 37, "7": 38, "8": 39, "9": 40,
                 "A": 41, "B": 42, "C": 43, "D": 44, "E": 45, "F": 46, "G": 47, "H": 48, "J": 49, "K": 50,
                 "L": 51, "M": 52, "N": 53, "P": 54, "Q": 55, "R": 56, "S": 57, "T": 58, "U": 59, "V": 60,
                 "W": 61, "X": 62, "Y": 63, "Z": 64}


    car_code2 = ""
    for i, number in enumerate(old_label.split("_")):
        if i == 0:
            car_origin_number = provinces[int(number)]
        else:
            car_origin_number = ads[int(number)]
        # car_code2.append(char_dict[car_origin_number])
        car_code2+=str(car_origin_number)
    return car_code2

def process_data(threadName, q):
    while exitFlag.value==0:
        if not q.empty():
            data = q.get()
            txt,count=data.split('|')
            path_new=os.path.join(basePath,txt)
            img=cv2.imread(path_new)
            img_name = path_new
            iname = img_name.rsplit('/', 1)[-1].rsplit('.', 1)[0].split('-')
            old_label=iname[-3]
            old_label=new_label(old_label)
            [leftUp, rightDown] = [[int(eel) for eel in el.split('&')] for el in iname[2].split('_')]
            cropped=img[leftUp[1]:rightDown[1],leftUp[0]:rightDown[0]]

            pic = cv2.resize(cropped, (240, 80), interpolation=cv2.INTER_CUBIC)
            imagename = outputPath + str(old_label) + ".jpg"
            # cv2.imwrite(imagename, cropped)
            cv2.imencode('.jpg', pic)[1].tofile(imagename)
            print("%s processing %s" % (threadName, count))
        else:
            exitFlag.value=1


if __name__ == '__main__':
    data = os.listdir(basePath)
    file = open(filename,'w')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#ȥ��[],�����а����ݲ�ͬ������ѡ��
        s = s.replace("'",'').replace(',','') +'|%d'%(i) +'\n'   #ȥ�������ţ����ţ�ÿ��ĩβ׷�ӻ��з�
        file.write(s)
    file.close()
    print("�����ļ��ɹ�");

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        print(outputPath + ' �����ɹ�')
    f=open('train.txt', encoding="utf-8")
    for line in f:
        workQueue.put(line.strip())
    start=time.time()
    print ("��ʼ��:%s" %datetime.datetime.now())
    for tName in threadList:
        p = Process(target=process_data, args=(tName,workQueue ))
        p.start()
    
    process_data("Main",workQueue)

    end=time.time()
    print ("������:%s" %datetime.datetime.now())
    print("��ʱ:%f��" % ((end-start)/60))
