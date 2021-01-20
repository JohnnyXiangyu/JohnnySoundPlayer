import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

from multiprocessing import Process
import multiprocessing

import ServerRoutine as SR


inputNum = None
outputNum = None

p1 = None
p2 = None


def initializeDevices():
    print('When you encounter invalid device, try to select Windows Directsound API devices!')

    nameKeyWord = input('please provide input device name: ')
    try:
        someDevice = sd.query_devices(device=nameKeyWord, kind='input')
    except ValueError as e:
        print(e)
        inputNum = int(input('please specify number of desired device: '))

    # nameKeyWord = input(
    #     'please provide output device name (will not be used): ')
    # try:
    #     someDevice = sd.query_devices(device=nameKeyWord, kind='output')
    # except ValueError as e:
    #     print(e)
    #     inputNum = int(input('please specify number of desired device: '))


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    p1.send(indata)
    # outdata[:] = indata


def RecordingRoutine():
    sd.Stream(device=inputNum, samplerate=44100,
              callback=callback, latency='low', dtype='int16')


if __name__ == '__main__':
    initializeDevices()

    p1, p2 = multiprocessing.Pipe()

    sd.Stream(device=inputNum, samplerate=44100,
              callback=callback, latency='low', dtype='int16')

    sRoutine = Process(target=SR.ServerRoutine)
    sRoutine.start()
    sRoutine.join()
