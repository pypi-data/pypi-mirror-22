import unittest
import os
import numpy as np
import neurokit as nk



class Test(unittest.TestCase):


    # If running from travis:
    data_path = os.getcwd() + r"/tests/test_bio_data.acq"
    # If running in local:
#    data_path = "test_bio_data.acq"

    def test_read_acqknowledge(self):
        # Read data
        df = nk.read_acqknowledge(self.data_path)
        # Resample to 100Hz
        df = df.resample("10L").mean()
        df.columns = ['ECG', 'EDA', 'PPG', 'Photosensor', 'RSP']
        # Check length
        self.assertEqual(len(df), 35645)
        return(df)

    def test_bio_process(self):
        df = self.test_read_acqknowledge()
        bio = nk.bio_process(ecg=df["ECG"], rsp=df["RSP"], eda=df["EDA"], sampling_rate=100, add=df["Photosensor"])
        self.assertEqual(len(bio), 3)
        self.assertEqual(len(bio["ECG"]["R_Peaks"]), 499)
        self.assertEqual(len(bio["EDA"]["SCR_Onsets"]), 5)
        return(bio)

# Not working for some reasons...
#    def test_complexity(self):
#        np.random.seed(666)
#        signal = np.sin(np.log(np.random.sample(100)))
#        complexity = nk.complexity(signal, lyap_r=False, lyap_e=False)
#        self.assertEqual("%.2f" %complexity["DFA"], "0.64")
#        self.assertEqual("%.2f" %complexity["Fractal_Dimension"], '1.13')
#        self.assertEqual("%.2f" %complexity["Hurst"], '0.60')
#        self.assertEqual("%.2f" %complexity["Multiscale_Entropy"], '1.70')
#        self.assertEqual("%.2f" %complexity["Sample_Entropy_Chebychev"], '2.07')
#        self.assertEqual("%.2f" %complexity["Sample_Entropy_Euclidean"], '2.25')
#        self.assertEqual("%.2f" %complexity["Shannon_Entropy"], '6.64')

if __name__ == '__main__':
    unittest.main()