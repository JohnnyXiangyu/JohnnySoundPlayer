from multiprocessing import Process
import multiprocessing
import RecordingRoutine as RR
import ServerRoutine as SR

if __name__ == '__main__':

    pipe1, pipe2 = multiprocessing.Pipe()

    RR.initializeDevices()

    RR.pipeEnd = pipe1
    SR.pipeEnd = pipe2

    rRoutine = Process(target=RR.RecordingRoutine)
    sRoutine = Process(target=SR.ServerRoutine)

    rRoutine.start()
    sRoutine.start()

    rRoutine.join()
    sRoutine.join()
