import mne
from enum import Enum
import pdb
class TimeClassification(Enum):
        """
        T0 corresponds to rest
        T1 corresponds to onset of motion (real or imagined) of
        the left fist (in runs 3, 4, 7, 8, 11, and 12)
        both fists (in runs 5, 6, 9, 10, 13, and 14)
        T2 corresponds to onset of motion (real or imagined) of
        the right fist (in runs 3, 4, 7, 8, 11, and 12)
        both feet (in runs 5, 6, 9, 10, 13, and 14)
        non ce differenza di time tra sinistra e destra o tra pugni e piedi in task 1 e 2 e task 3 e 4
        """
        T0 = ""
        T1 = ""
        T2 = ""
class Parsing:
    class Runs(Enum):
        """
        1. Baseline, eyes open  R 1
        2. Baseline, eyes closed R 2
        3. Task 1 (open and close left or right fist) R 3, 7, 11
        4. Task 2 (imagine opening and closing left or right fist) R 4, 8, 12
        5. Task 3 (open and close both fists or both feet) R 5, 9, 13
        6. Task 4 (imagine opening and closing both fists or both feet) R 6, 10, 14
        """
        BASELINE_EYES_OPEN = [1]
        BASELINE_EYES_CLOSED = [2]
        TASK_1 = [3 , 7, 11]
        TASK_2 = [4, 8, 12]
        TASK_3 = [5, 9, 13]
        TASK_4 = [6, 10, 14]
    

    def __init__(self):
        pass
    def process_data(self, subject: int, experiment: int) -> mne.io.Raw:
        path: list = mne.datasets.eegbci.load_data(subjects=subject, runs=experiment, path="data")
        raw: list = []
        for path in path:
            raw.append(mne.io.read_raw_edf(path, preload=True))
        return mne.concatenate_raws(raw)
    def process_data_all(self, experiment: int) -> mne.io.Raw:
        raw: list = []
        for subject in range(1, 8):
            raw.append(self.process_data(subject, experiment))
        return raw
    def collect_data(self):
        info: dict = {}
        for experiment in self.Runs:
            info[experiment.name] =  self.process_data_all(experiment.value)
            break
        return info
    
    @property
    def task_1(self) -> list[mne.io.Raw]:
        return self.process_data_all(self.Runs.TASK_1.value)
    @property
    def task_2(self) -> list[mne.io.Raw]:
        return self.process_data_all(self.Runs.TASK_2.value)
    @property
    def task_3(self) -> list[mne.io.Raw]:
        return self.process_data_all(self.Runs.TASK_3.value)
    @property
    def task_4(self) -> list[mne.io.Raw]:
        return self.process_data_all(self.Runs.TASK_4.value)
    @property
    def baseline_eyes_open(self) -> list[mne.io.Raw]:
        return self.process_data_all(self.Runs.BASELINE_EYES_OPEN.value)
    @property
    def baseline_eyes_closed(self) -> list[mne.io.Raw]:
        return self.process_data_all(self.Runs.BASELINE_EYES_CLOSED.value)

class Filtering:
    def __init__(self):
        pass
    def bandpass_filter(self, raw: mne.io.Raw) -> mne.io.Raw:
        return raw.filter(l_freq=8, h_freq=30, n_jobs=4)
    def notch_filter(self, raw: mne.io.Raw) -> mne.io.Raw:
        return raw.notch_filter(freq=50)
    def furrier_transform(self, raw: mne.io.Raw) -> mne.io.Raw:
        return None
    """
    farlo per tutti i 109 pazienti ettireare con raw e concatenare i raw

    """
"""
class Epoching:
    def __init__(self):
        pass
    def epoching(self, raw: mne.io.Raw) -> mne.io.Raw:
       events, _ = mne.events_from_annotations(raw)
       epochs = mne.Epochs(raw, events, event_id=None, tmin=-0.5, tmax=2.5, baseline=(None, 0), preload=True)
       return epochs
"""
    
if __name__ == "__main__":
    try:
        rawData = Parsing()
        print(rawData.baseline_eyes_open)
        print(rawData.baseline_eyes_closed)
        
    except Exception as e:
        print(e)