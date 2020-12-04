import mpmath
import numpy as np
from multiprocessing import Process
import time
import argparse


def cal_zeta(start, end, step):
    #print(f'start={start}, end={end}, step={step}')
    size = int((end - start) / step)
    value = []
    for i in range(size):        
        value.append(mpmath.zeta(1/2 + (start + float(i)*step) * 1j))
    return value


# with bug
def old_cal_zeta(start,end,step):
    size = int((end - start) / step)
    print(size)
    value = np.zeros(size)
    print(np.arange(start,end,step).reshape(1,-1))
    for index, x in enumerate(list(np.arange(start,end,step))):
        print(f'{index}')
        x =float(x[0])        
        value[index] = mpmath.zeta(1/2 + x * 1j)
    return value



def single_cal(args):
    cal_zeta(args.start,args.end, args.step)
    #print(value)

def multi_cal(args):
    onepsize = int((args.end - args.start) / args.pn)

    process_list=[]
    for i in range(args.pn):
        p = Process(target=cal_zeta,args=(args.start+onepsize*i,args.start+onepsize*(i+1), args.step))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()


def main():
    parser = argparse.ArgumentParser(description="cal zetafunction's non-trivial zero")
    parser.add_argument('-p',action='store_true')
    parser.add_argument('-pn', default=5, type=int)

    parser.add_argument('-s', '--start', default=0, type=float)
    parser.add_argument('-e', '--end', default=80, type=float)
    parser.add_argument('-w', '--step', default=0.01, type=float)
    
    args = parser.parse_args()

    print(f'start={args.start}, end={args.end}, step={args.step}')

    start = time.time()
    if args.p == True:
        multi_cal(args)
    else:
        single_cal(args)

    end = time.time()
    print(end-start,"[sec.]")



main()