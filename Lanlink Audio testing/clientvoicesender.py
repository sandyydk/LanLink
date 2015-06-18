__author__ = 'Sandyman'

"""
This module handles the voice chat. Here the voice is first recorded in the user using the inbuilt mic or the default
mike. This is saved in .wav format and then sent in chunks or bits to the server. The filename adopted is that of the
target client.
"""
import wave
import pyaudio
import socket
import sys
import clientlist
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10

def voicerecorder(title):

    host = socket.gethostname()
    nameframe = host+","+title
    WAVE_OUTPUT_FILENAME = title+".wav"
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    try:
        sendingsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendingsock.connect((clientlist.serverip,20007))
        print nameframe
        sendingsock.sendall(nameframe)
        f = open(title+".wav",'rb')
        l = f.read(1024)
        while l:
            sendingsock.send(l)
            l = f.read(1024)
        sendingsock.close()
        f.close()
    except Exception,e:
        print e.args

