import wave
from struct import iter_unpack

wfile = wave.open('decodeC.wav', 'rb')

amplitude = 32000
samplesPerBit = 8
channels = wfile.getnchannels() # 2 (stereo)
samp_w = wfile.getsampwidth()   # 2 bytes
frames = wfile.getnframes()

wfile.setpos(0)
w_data = wfile.readframes(frames)

assert(len(w_data) == frames * samp_w * channels)
# 2 bytes * 2 channels * frames == length of our bytestring

FLAG_BITS_1 = []
FLAG_BITS_2 = []

data_1_amp = amplitude / 2
data_2_amp = amplitude / 4

last_frame = -1
for data_frame, timing_frame in iter_unpack("hh", w_data):
    if last_frame != timing_frame:
        last_frame = timing_frame
        FLAG_BITS_1.append(str(int(data_frame / data_1_amp)))
        FLAG_BITS_2.append(str(int(data_frame % data_1_amp / data_2_amp)))

DATA1 = ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(FLAG_BITS_1)] * 8))
DATA2 = ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(FLAG_BITS_2)] * 8))

print(f"Decoded DATA1: {DATA1}, DATA2: {DATA2}")

FLAG = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(DATA1, DATA2))

print(f"Flag decodeC.wav: {FLAG}")

