# Copyright 2025 n-squared LAB @ FAU Erlangen-Nürnberg

"""
EMG Signal Processing Exercise

Students should complete the TODO sections.
Do not change function names unless instructed.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal


def load_emg_data(filename: str):
    """
    Load EMG data from a pickle file and extract:
    - the raw biosignal
    - the sampling rate

    Expected structure:
        data["biosignal"]
        data["device_information"]["sampling_frequency"]
    """

    # TODO: load the pickle file with pandas
    data = pd.read_pickle(filename)

    print("Data structure:")
    print("-" * 50)
    print(f"Data type: {type(data)}")
    print(f"Data shape: {data.shape if hasattr(data, 'shape') else 'N/A'}")
    print("\nAvailable keys in data:")
    print("-" * 50)
    for key in data.keys():
        print(f"- {key}")
    print("-" * 50)

    # TODO: extract the EMG signal
    emg_signal = data["biosignal"]

    # TODO: extract the sampling rate
    sampling_rate = data["device_information"]["sampling_frequency"]


    print("\nEMG Signal information:")
    print("-" * 50)
    print(f"Signal shape: {emg_signal.shape}")
    print(f"Number of channels: {emg_signal.shape[0]}")
    print(f"Window size: {emg_signal.shape[1]}")
    print(f"Number of windows: {emg_signal.shape[2]}")
    print(f"Sampling rate: {sampling_rate} Hz")

    return emg_signal, sampling_rate


def restructure_emg_data(emg_signal: np.ndarray):
    """
    Convert EMG from:
        (channels, window_size, n_windows)
    to:
        (channels, total_samples)
    """

    # TODO: determine the number of channels
    num_channels = emg_signal.shape[0]

    # TODO: transpose and reshape so each row is one continuous channel
    channel_data = np.transpose(emg_signal, (0, 2, 1)).reshape(num_channels, -1)

    print("\nRestructured EMG Data:")
    print("-" * 50)
    print(f"Original shape: {emg_signal.shape}")
    print(f"New shape: {channel_data.shape}")
    print(f"Number of channels: {num_channels}")
    print(f"Total samples per channel: {channel_data.shape[1]}")

    return channel_data, num_channels


def bandpass_filter_emg(channel_data: np.ndarray, sampling_rate: float, low_cut: float = 20, high_cut: float = 450,):
    """
    Apply a Butterworth bandpass filter to each channel.
    """
    # TODO: compute the Nyquist frequency
    nyquist = sampling_rate / 2

    # TODO: validate low_cut and high_cut
    # Raise ValueError if the frequencies are invalid.
    if high_cut >= nyquist:
        raise ValueError("high_cut must be below the Nyquist frequency")
    if low_cut >= high_cut:
        raise ValueError("low_cut must be below high_cut")

    # TODO: normalize the cutoff frequencies
    low = low_cut / nyquist
    high = high_cut / nyquist

    print("\nFilter Design Parameters:")
    print("-" * 50)
    print(f"Sampling rate: {sampling_rate} Hz")
    print(f"Nyquist frequency: {nyquist} Hz")
    print(f"Low cutoff: {low_cut} Hz ({low:.4f} normalized)")
    print(f"High cutoff: {high_cut} Hz ({high:.4f} normalized)")

    # TODO: design a 4th order Butterworth bandpass filter
    a, b = signal.butter(4, [low, high], btype='bandpass')

    # TODO: pre-allocate filtered array
    filtered_channels = np.zeros(channel_data.shape)

    # TODO: apply filtfilt to every channel
    for channel in range(channel_data.shape[0]):
        filtered_channels[channel] = signal.filtfilt(b,a, channel_data[channel])

    print("\nFiltered Signal Information:")
    print("-" * 50)
    print(f"Shape of filtered_channels: {filtered_channels.shape}")
    print(f"Type of filtered_channels: {type(filtered_channels)}")
    print(f"Filter cutoff frequencies: {low_cut} Hz to {high_cut} Hz")

    return filtered_channels


def compute_rms(filtered_channels: np.ndarray, sampling_rate: float, window_ms: float = 100):
    """
    Compute RMS envelope using a moving window.
    """

    # TODO: convert window size from ms to samples
    window_size = int(sampling_rate * (window_ms / 1000))

    # TODO: pre-allocate RMS array
    rms_signals = np.zeros(filtered_channels.shape)

    # TODO: compute RMS for each channel
    # Hint:
    # 1. square the signal
    # 2. moving average with np.convolve(..., mode="same")
    # 3. square root
    half_window = window_size // 2
    for channel_index in range(len(filtered_channels)):
        for i in range(len(filtered_channels[channel_index])):
            start = max(0, i - half_window)
            end = min(len(filtered_channels[channel_index]), i + half_window)
            window = filtered_channels[channel_index][start:end]

            rms_signals[channel_index, i] = np.mean(window**2)**0.5


    print("\nRMS Signal Information:")
    print("-" * 50)
    print(f"Number of channels: {filtered_channels.shape[0]}")
    print(f"Shape of RMS signals: {rms_signals.shape}")
    print(f"Window size: {window_size} samples ({window_size / sampling_rate * 1000:.1f} ms)")

    return rms_signals


def plot_emg_processing(
    channel_data: np.ndarray,
    filtered_channels: np.ndarray,
    rms_signals: np.ndarray,
    sampling_rate: float,
    selected_channel: int = 0,
):
    """
    Plot raw, filtered, and RMS signal for one channel.
    """

    t = np.arange(channel_data.shape[1]) / sampling_rate

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    ax1.plot(t, channel_data[selected_channel, :])
    ax1.set_title(f"Original EMG Signal - Channel {selected_channel + 1}")
    ax1.set_ylabel("Amplitude (V)")

    ax2.plot(t, filtered_channels[selected_channel, :])
    ax2.set_title(f"Bandpass Filtered Signal - Channel {selected_channel + 1}")
    ax2.set_ylabel("Amplitude (V)")

    ax3.plot(t, rms_signals[selected_channel, :])
    ax3.set_title(f"RMS Signal - Channel {selected_channel + 1}")
    ax3.set_ylabel("Amplitude (V)")
    ax3.set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()


def main():
    # TODO: get the filepath of the pkl file (Use / not \)
    filename = '/Users/jannis/Documents/Uni auf MB/Applied-Programming-2026/recording.pkl'

    emg_signal, sampling_rate = load_emg_data(filename)
    channel_data, _ = restructure_emg_data(emg_signal)
    filtered_channels = bandpass_filter_emg(channel_data, sampling_rate)
    rms_signals = compute_rms(filtered_channels, sampling_rate)

    # Change the channel index if needed
    plot_emg_processing(
        channel_data,
        filtered_channels,
        rms_signals,
        sampling_rate,
        selected_channel=0,
    )


if __name__ == "__main__":
    main()
