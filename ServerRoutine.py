from os import name
from flask import Flask, Response, render_template
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
# import pyaudio

app = Flask(__name__)


inputNum = None
outputNum = None


# FORMAT = pyaudio.paInt16
# CHANNELS = 2
# RATE = 44100
# CHUNK = 1024
# RECORD_SECONDS = 5


# audio1 = pyaudio.PyAudio()

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    # (4byte) Marks file as RIFF
    o = bytes("RIFF", 'ascii')
    # (4byte) File size in bytes excluding this and RIFF marker
    o += (datasize + 36).to_bytes(4, 'little')
    # (4byte) File type
    o += bytes("WAVE", 'ascii')
    # (4byte) Format Chunk Marker
    o += bytes("fmt ", 'ascii')
    # (4byte) Length of above format data
    o += (16).to_bytes(4, 'little')
    # (2byte) Format type (1 - PCM)
    o += (1).to_bytes(2, 'little')
    # (2byte)
    o += (channels).to_bytes(2, 'little')
    # (4byte)
    o += (sampleRate).to_bytes(4, 'little')
    o += (sampleRate * channels * bitsPerSample //
          8).to_bytes(4, 'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,
                                                  'little')               # (2byte)
    # (2byte)
    o += (bitsPerSample).to_bytes(2, 'little')
    # (4byte) Data Chunk Marker
    o += bytes("data", 'ascii')
    # (4byte) Data size in bytes
    o += (datasize).to_bytes(4, 'little')
    return o


@app.route('/audio')
def audio():
    # start Recording
    def sound():
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        first_run = True
        with sd.InputStream(device=inputNum, samplerate=44100,
              latency=0.1, dtype='int16', blocksize=2) as st:
            while True:
                newData, someBool = st.read(2)
                newData = newData.tobytes()
                if first_run:
                    data = wav_header + newData
                    first_run = False
                else:
                    data = newData
                yield(data)

    return Response(sound())


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def initializeDevices():
    global inputNum
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


if __name__ == '__main__':
    initializeDevices()
    app.run(host='0.0.0.0', debug=True, threaded=True,
            port=5000, use_reloader=False)
