import numpy as np
import soundfile as sf
from scipy.signal import correlate


data, fs = sf.read("pikachu.wav")   


if len(data.shape) > 1:
    data = np.mean(data, axis=1)


def delay_signal(signal, delay_sec, fs):
    delay_samples = int(delay_sec * fs)
    return np.concatenate((np.zeros(delay_samples), signal))

sig_0 = delay_signal(data, 0, fs)
sig_1 = delay_signal(data, 1, fs)
sig_2 = delay_signal(data, 2, fs)

# Save them
sf.write("delay_0s.wav", sig_0, fs)
sf.write("delay_1s.wav", sig_1, fs)
sf.write("delay_2s.wav", sig_2, fs)


def compute_corr(x, y):
    # Make same length
    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]
    
    corr = correlate(x, y, mode='full')
    return np.max(corr)

corr_0 = compute_corr(sig_0, sig_1)
corr_1 = compute_corr(sig_1, sig_1)
corr_2 = compute_corr(sig_2, sig_1)

print("Correlation with 1s reference:")
print("0s vs 1s:", corr_0)
print("1s vs 1s:", corr_1)
print("2s vs 1s:", corr_2)


min_len = min(len(sig_0), len(sig_2))
new_ref = sig_0[:min_len] + sig_2[:min_len]

sf.write("new_reference.wav", new_ref, fs)


sig_3 = delay_signal(data, 3, fs)

corr_0_new = compute_corr(sig_0, new_ref)
corr_2_new = compute_corr(sig_2, new_ref)
corr_3_new = compute_corr(sig_3, new_ref)

print("\nCorrelation with NEW reference:")
print("0s vs new_ref:", corr_0_new)
print("2s vs new_ref:", corr_2_new)
print("3s vs new_ref:", corr_3_new)