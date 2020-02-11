"""Simple quantization demo."""
import numpy as np


def quantize(x, n):
    """Apply n-bit quantization to signal."""
    x /= np.ma.max(np.abs(x))  # make sure x in [-1,1]
    bins = np.linspace(-1, 1, 2**n+1, endpoint=True)  # [-1,1]
    qvals = (bins[:-1] + bins[1:]) / 2
    bins[-1] = 1.01  # Include 1 in case of clipping
    return qvals[np.digitize(x, bins)-1]


if __name__ == '__main__':
    import sys
    import soundfile as sf
    if len(sys.argv) < 3:
        print("Usage: python quantize.py /path/to/audio.wav N-bit")
        print("Example: python quantize.py welcome16k.wav 8")
        exit()

    sig, sr = sf.read(sys.argv[1])
    nbit = int(sys.argv[2])
    sig = quantize(sig, nbit)
    sf.write(f"{sys.argv[1].split('.')[0]}_{nbit}bit.wav", sig, sr)
