#!/usr/bin/env python
from multiprocessing import Process, Value, Array, Pipe
import statistics
import socket

def f_mean(input_str):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect(('0.0.0.0', 9999))
    sk.send(input_str.encode())
    data = sk.recv(1024).strip().decode()
    print("Mean : %s " % (data))
    sk.close()

def f_median(conn, raw_a):
    numbers = []
    for i in raw_a:
        numbers.append(int(i))
    conn.send(statistics.median(numbers))
    conn.close()

def f_mode(share_value, numbers):
    share_value.value = statistics.mode(numbers)


if __name__ == '__main__':

    # input numbers
    input_str = input("Enter your input: ");
    raw_array = input_str.split()
    numbers = Array('i', len(raw_array))
    for i in range(len(raw_array)):
        try:
            int_value = int(raw_array[i])
        except ValueError:
            print(raw_array[i], "is not a number!") 
            exit()
        else:
            numbers[i] = int(raw_array[i])

    # setup pipe
    parent_conn, child_conn = Pipe()

    # setup shared memory value
    share_value = Value('i',0)

    p1 = Process(target=f_mean, args=(input_str,))
    p2 = Process(target=f_median, args=(child_conn, raw_array))
    p3 = Process(target=f_mode, args=(share_value, numbers))
    
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    print('Median: ', parent_conn.recv())
    print('Mode: ', share_value.value)
