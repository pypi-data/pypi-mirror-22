import signal_processing
import numpy as np
from scipy import signal
import mne
import feature_extraction 


class EEGFeatureExtractor(feature_extraction.FeatureExtractor):
    def __init__(self, params):
        self.time_limits = params["time_limits"]
        self.tmin = params["tmin"]
        self.freq = float(params["freq"])
        self.n_channels = int(params["n_channels"])
        self.channels_to_extract_from = list(params["channels_to_extract_from"])
        self.verbose = params["verbose"] if ("verbose" in params) else None
        if self.verbose:
            print params


class RawExtractor(EEGFeatureExtractor):
    def __init__(self, params):
        super(RawExtractor, self).__init__(params)

    def extract(self, trial):
        assert self.n_channels == trial.shape[0], "check trial shape (channels x samples)"
        ti, tf = self.time_limits

        initial_frame = int((ti - self.tmin) * self.freq)
        end_frame = int((tf - self.tmin) * self.freq)
        data = trial[self.channels_to_extract_from, initial_frame:end_frame]
        return data


class TrashExtractor(EEGFeatureExtractor):
    def __init__(self, params):
        super(TrashExtractor, self).__init__(params)

    def extract(self, trial):
        assert self.n_channels == trial.shape[0], "check trial shape (channels x samples)"
        ti, tf = self.time_limits

        initial_frame = int((ti - self.tmin) * self.freq)
        end_frame = int((tf - self.tmin) * self.freq)
        data = trial[self.channels_to_extract_from, initial_frame:end_frame]

        data = np.random.random(data.shape[0])
        return data


class FreqExtractor(EEGFeatureExtractor):
    def __init__(self, params):
        super(FreqExtractor, self).__init__(params)
        self.min_freq = params["min_freq"]
        self.max_freq = params["max_freq"]

    def extract(self, trial):
        assert self.n_channels == trial.shape[0], "check trial shape (channels x samples)"
        ti, tf = self.time_limits

        initial_frame = int((ti - self.tmin) * self.freq)
        end_frame = int((tf - self.tmin) * self.freq)
        data = trial[self.channels_to_extract_from, initial_frame:end_frame]

        freqs_by_channel = []

        for ch in self.channels_to_extract_from:
            x = data[ch, :]
            freqs, Pxx = signal.welch(x, fs=self.freq)
            idx_30hz = np.argmax(freqs > self.max_freq)  # No more than x hz
            idx_1hz = np.argmin(freqs < self.min_freq)  # No less than y Hz

            freqs = freqs[idx_1hz:idx_30hz]
            presence_of_freq = Pxx[idx_1hz:idx_30hz]

            freqs_by_channel.extend(presence_of_freq)
        res = np.array(freqs_by_channel)
        return res

    def mapping(self):
        trial = np.zeros((self.n_channels, 1075))  # (channels x samples)
        montage = mne.channels.read_montage('/home/pbrusco/projects/montages/LNI.sfp')

        ti, tf = self.time_limits

        initial_frame = int((ti - self.tmin) * self.freq)
        end_frame = int((tf - self.tmin) * self.freq)
        data = trial[self.channels_to_extract_from, initial_frame:end_frame]
        res = {}

        i = 0
        for ch in self.channels_to_extract_from:
            x = data[ch, :]
            freqs, Pxx = signal.welch(x, fs=self.freq)
            idx_30hz = np.argmax(freqs > self.max_freq)  # No more than x hz
            idx_1hz = np.argmin(freqs < self.min_freq)  # No less than y Hz

            freqs = freqs[idx_1hz:idx_30hz]
            for freq in freqs:
                res[i] = dict(channel=ch,
                              channel_name=montage.ch_names[ch],
                              freq=freq,
                              channel_position=montage.pos[ch],
                              name="c{}|{}Hz)".format(ch, round(freq, 2))
                              )
                i = i + 1

        return res


class WaveletsExtractor(EEGFeatureExtractor):
    def __init__(self, params):
        super(WaveletsExtractor, self).__init__(params)

    def extract(self, trial):
        pass


class WindowedExtractor(EEGFeatureExtractor):
    def __init__(self, params):
        super(WindowedExtractor, self).__init__(params)
        self.window_sizes = params["window_sizes"]
        self.step_in_frames = params["step_in_frames"]

    def extract(self, trial):
        # Trial shape: (channels x samples)
        assert self.n_channels == trial.shape[0], "check trial shape (channels x samples)"
        features = []
        for window_size_in_secs in self.window_sizes:
            ws_frames = int(window_size_in_secs * self.freq)
            if self.verbose:
                print "ws frames: ", ws_frames
            for starting_sample, chunk in signal_processing.sliding_window(trial,
                                                                               window_size_in_frames=ws_frames,
                                                                               step_in_frames=self.step_in_frames,
                                                                               time_limits=self.time_limits,
                                                                               t0=self.tmin,
                                                                               freq=self.freq,
                                                                               debugging=self.verbose,
                                                                               ):
                window_coefficients = []
                for ch in self.channels_to_extract_from:
                    y = chunk[ch, :]
                    window_coefficients.append(y.mean())
                features.extend(window_coefficients)

        features = np.array(features)
        return features

    def mapping(self):
        i = 0
        dummy_epoch = np.zeros((self.n_channels, 1075))  # (channels x samples)
        montage = mne.channels.read_montage('/home/pbrusco/projects/montages/LNI.sfp')

        res = {}
        for window_size_in_secs in self.window_sizes:
            ws_frames = int(window_size_in_secs * self.freq)
            for starting_sample, chunk in lib.signal_processing.sliding_window(dummy_epoch,
                                                                               window_size_in_frames=ws_frames,
                                                                               step_in_frames=self.step_in_frames,
                                                                               time_limits=self.time_limits,
                                                                               t0=self.tmin,
                                                                               freq=self.freq,
                                                                               ):
                for ch in self.channels_to_extract_from:
                    t0, t1 = lib.signal_processing.frame_time_limits(starting_sample, self.freq, self.tmin, ws_frames)
                    res[i] = dict(
                        channel=ch,
                        channel_name=montage.ch_names[ch],
                        starting_sample=starting_sample,
                        window_size=window_size_in_secs,
                        starting_time=round(t0, 3),
                        end_time=round(t1, 3),
                        channel_position=montage.pos[ch],
                        name="(w{}|c{}|{}|{})".format(round(window_size_in_secs, 2), ch, round(t0, 2), round(t1, 2))
                    )
                    i = i + 1
        return res
