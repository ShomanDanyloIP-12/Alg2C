from random import randrange as rand
import psutil
import math
import time
from shutil import copyfile as copyf

def default_alg(n, i):
    randomize_file(n)
    time_start = time.time()
    # print("####before - ")
    # print_all()
    # print("####alg - ")

    while (2 ** i <= n):
        # print("@@@ Перед входом в разделение i = ", i, ", n = ", n)
        split_to_files(n, i)
        # print("###Вміст файлів###")
        # print_all()
        # print("###ENDВміст файлів###")
        # print("@@@ Перед входом в слияние i = ", i, ", n = ", n)
        merge(n, i)
        i += 1
        # print("i = ", i)

    time_end = time.time()
    # print("####after - \n")
    # print_all()

    if (is_sorted('A.bin')):
        print("Sorted correctly")
    else:
        print("error")

    print("Default algorting sorting time: " + str(time_end - time_start) + "\n")
    clear_file("A.bin")
    clear_file("B.bin")
    clear_file("C.bin")
    return

def modified_alg(n, i):
    randomize_file(n)
    time_start = time.time()
    i = pre_sort('A.bin')
    # print("i = ", i)
    copyf('preSortedFile.bin', 'A.bin')
    # print("####before - ")

    while(2 ** i <= n):
        split_to_files(n, i)
        merge(n, i)
        i += 1

    time_end = time.time()
    # print("####after - ")
    # print_all()

    if(is_sorted('A.bin')):
        print("Sorted correctly")
    else:
        print("error")

    print("Modified algoritm sorting time: " + str(time_end - time_start) + "\n")
    clear_file("A.bin")
    clear_file("B.bin")
    clear_file("C.bin")
    return

def randomize_file(n):
    fa = open("A.bin", 'wb')
    for i in range(n):
        fa.write(rand(0, 100).to_bytes(32,'big'))
    fa.close()
    return

def print_file(path):
    with open(path, "rb") as file:
        num = file.read(32)
        print("---", path, "---")
        while num:
            num = int.from_bytes(num, 'big')
            print(num, end = ' ')
            num = file.read(32)
    return

def print_all():
    print_file("A.bin")
    print()
    print_file("B.bin")
    print()
    print_file("C.bin")
    print()
    return

def clear_file(path):
    with open(path, "wb") as file:
        file.write(b'')


def split_to_files(n, iteration):
    fa = open('A.bin', 'br')
    fb = open('B.bin', 'wb')
    fc = open('C.bin', 'wb')

    i = 0
    while(i < n):
        k1 = 0
        while(k1 != 2 ** iteration):
            fb.write(fa.read(32))
            # print("Записано у файл б - \n", print_all())
            i += 1
            k1 += 1

        k2 = 0
        while (k2 != 2 ** iteration):
            fc.write(fa.read(32))
            # print("Записано у файл с - \n", print_all())
            i += 1
            k2 += 1

    fa.close()
    fb.close()
    fc.close()
    return


def merge(n, iteration):
    fa = open('A.bin', 'wb')
    fb = open('B.bin', 'rb')
    fc = open('C.bin', 'rb')

    i = 0

    bel1 = fb.read(32)
    el1 = int.from_bytes(bel1, 'big')

    bel2 = fc.read(32)
    el2 = int.from_bytes(bel2, 'big')

    while bel1 and bel2:
        k1 = 1
        k2 = 1
        while (k1 != 2 ** iteration + 1 and k2 != 2 ** iteration + 1):
            if (el1 <= el2):
                # print("Записано у файл значення el1 - ", el1)
                fa.write(bel1)
                bel1 = fb.read(32)
                el1 = int.from_bytes(bel1, 'big')
                k1 += 1
                i += 1
                # print("Тепер el1 - ", el1, ", k1 = ", k1, ", i = ", i)
            else:
                # print("Записано у файл значення el2 - ", el2)
                fa.write(bel2)
                bel2 = fc.read(32)
                el2 = int.from_bytes(bel2, 'big')
                k2 += 1
                i += 1
                # print("Тепер el2 - ", el2, ", k2 = ", k2, ", i = ", i)
        while (k1 != 2 ** iteration + 1):
            # print("У дод циклі записано у файл значення el1 - ", el1)
            fa.write(bel1)
            bel1 = fb.read(32)
            k1 += 1
            i += 1
            el1 = int.from_bytes(bel1, 'big')
            # print("Тепер el1 - ", el1, ", k1 = ", k1, ", i = ", i)

        while (k2 != 2 ** iteration + 1):
            # print("У дод циклі записано у файл значення el2 - ", el2)
            fa.write(bel2)
            bel2 = fc.read(32)
            k2 += 1
            i += 1
            el2 = int.from_bytes(bel2, 'big')
        #     print("Тепер el2 - ", el2, ", k2 = ", k2, ", i = ", i)
        # print("-$----end group----$- i = ", i, ", k1 = ", k1, ", k2 = ", k2)
    for i in range(n-i):
        # print("Надлишково додано елемент - ", el1)
        fa.write(bel1)
        bel1 = fb.read(32)
        i += 1
        el1 = int.from_bytes(bel1, 'big')

    fa.close()
    fb.close()
    fc.close()
    return

def is_sorted(path):
    with open(path, "rb") as file:
        prev = file.read(32)
        num = file.read(32)
        while num:
            if (int.from_bytes(prev, 'big') > int.from_bytes(num, 'big')):
                # print("NO ")
                return False
            prev = num
            num = file.read(32)
            # print("Yes ")
    return True


def pre_sort(path):
    available_ints = int(psutil.virtual_memory()[1]/32)
    clear_file("preSortedFile.bin")

    with open(path, "rb") as file:
        int_list = []
        while True:
            num = file.read(32)
            if num == b'':
                break

            for i in range(available_ints):
                int_list.append(int.from_bytes(num, 'big'))
                num = file.read(32)
                if num == b'':
                    break

            int_list.sort()

            with open('preSortedFile.bin', "ab") as preFile:
                for i in int_list:
                    preFile.write(i.to_bytes(32, 'big'))

    return math.log2(available_ints)