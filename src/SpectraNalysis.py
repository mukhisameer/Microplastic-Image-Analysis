"""
auth: Judah S.
date: 10/30/2022
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class Spectrum:
    def __init__(self, spectrumPath) -> None:
        self.spectrumPath = spectrumPath
        self.df = self.readSpectrumAsTXT(spectrumPath)
        # self.df = self.readSpectrumAsFWF(spectrumPath)

    # use over fixed-width-file (FWF) method
    def readSpectrumAsTXT(self, spectrumPath):
        cols = ['shift', 'intensity']
        specFile = open(spectrumPath, 'r')
        rows = specFile.readlines()

        df = pd.DataFrame(columns=['shift', 'intensity'])

        for row in rows:
            shift = float(row.split('\t')[0])
            intensity = float(row.split('\t')[1])
            temp_df = pd.DataFrame( [[shift, intensity]], columns=['shift', 'intensity'])
            df = pd.concat([df, temp_df], axis=0)
        
        df.reset_index(drop=True, inplace=True)
        return df.copy()

    # does NOT ALWAYS accurately parse wavelength (shift) and absorbance (intensity) from spectrum file
    # NOTE: since tab is used as the delimiter (instead of spaces)in the spectrum file, this method FAILS 
    # in occasions where the wavelength shift is an int (whole number) and not a float; when shift is a 
    # whole number (say of 4 digits), since we specify field width for each column, the tab is not read 
    # as a delimiter, and some digits from the next col (intensity) are taken to satisfy the specified
    # field width of the prior col
    def readSpectrumAsFWF(self, spectrumPath):
        cols = ['shift', 'intensity']
        df = pd.read_fwf(spectrumPath, header=None, names=cols, colspecs=[(0,8), (8,16)])

        return df.copy()

    def plotSpectrum(self):
        self.fig, self.axs = plt.subplots(1, 2, figsize=(35, 15))
        self.axs = self.axs.flatten()
        self.df.plot.line(x='shift', y='intensity', ax=self.axs[0])
        self.df.plot.scatter(x='shift', y='intensity', ax=self.axs[1])
        plt.show(block=False)

    def printSpectrum(self):
        print(self.df)

    def displayFilePath(self):
        print(self.spectrumPath)

    # can retrieve a specified amount of peaks around a specified wavelength shift
    # performs sort on differences between desired shift and other shifts.
    # so slightly less efficient (runs in O(nlogn) time) than 'B' method 
    # but again, enables us to get 'amount' peaks around the desired shift
    # 
    # since we are computing absolute difference to a the desired shift, if the desired
    # shift is out-of-bounds, it won't break the algo, but we can still allow an arg to
    # determine whether we should warn the user or interprete the shift as the "lowest"
    # or highest in the spectrum
    def findPeakAtShiftA(self, shift, amount, replaceMinMax):
        
        # replaceMinMax is False
        if (shift < self.df['shift'].min() or shift > self.df['shift'].max()) and replaceMinMax==False:
            print("Specified shift is out-of-bounds, and replaceMinMax is set to False!")
            return -1

        # replaceMinMax is True

        peaks = self.df.iloc[(spec.df['shift']-shift).abs().argsort()[:amount]]
        print(peaks)

        return peaks

    # retrieves peak if exact shift exists in spectrum,
    # otherwise retrieves 2 peaks:
    #   - peak at closest shift lower than specified shift, 
    #   - peak at closest shift greater than specified shift
    # more efficient (runs in O(n) time) than 'A' method, but returns exactly 1 or 2 peaks
    #
    # additionally, we check if the desired shift is out-of-bounds and the state of the replaceMinMax boolean flag
    # if shift is out-of-bounds, and replaceMinMax is False, we exit immediately
    # "    "   "   "   "    "     "     "          is True, then we use either the lowest shift or the highest shift in the spectrum
    def findPeakAtShiftB(self, shift, replaceMinMax):

        # replaceMinMax is False
        if (shift < self.df['shift'].min() or shift > self.df['shift'].max()) and replaceMinMax==False:
            print("Specified shift is out-of-bounds, and replaceMinMax is set to False!")
            return -1

        # replaceMinMax is True

        value = self.df[self.df['shift']==shift]
        range = []

        if not value.empty:                                                                     # found exact shift match in spectrum
            peaks = value
        elif shift < self.df['shift'].min():                                                    # "set" shift to be the minimum shift in spectrum
            range.append(self.df['shift'].idxmin())
        elif shift > self.df['shift'].max():                                                    # "set" shift to be the maximum shift in spectrum
            range.append(self.df['shift'].idxmax())
        else:                                                                                   # shift is within bounds, but no exact match in spectrum; get closest lower- and upper-shifts
            range.append(self.df[self.df['shift'] < shift]['shift'].idxmax())
            range.append(self.df[self.df['shift'] > shift]['shift'].idxmin())

        peaks = self.df.iloc[range]
        print(peaks)

        return peaks

    def findMaxPeakInRange(self, lowerBoundShift, upperBoundShift, replaceMinMax):

        # replaceMinMax is False
        if (lowerBoundShift < self.df['shift'].min() or upperBoundShift > self.df['shift'].max()) and replaceMinMax==False:
            print("Specified shifts are out-of-bounds, and replaceMinMax is set to False!")
            return -1
        
        # replaceMinMax is true

        if lowerBoundShift > upperBoundShift:
            print("UpperBoundShift must be greater than or equal to LowerBoundShift!")
            return -1
        

        if lowerBoundShift < self.df['shift'].min(): lowerBoundShift=self.df['shift'].min()     # "set" lowerBoundShift to be the minimum shift in spectrum
        if upperBoundShift > self.df['shift'].max(): upperBoundShift=self.df['shift'].max()     # "set" upperBoundShift to be the maximum shift in spectrum

        # by deduction, if the below is true, and we know that lowerBoundShift was initially less than upperBoundShift before being fixed,
        # it would imply imply upperBoundShift was always less than the min. shift in our spectrum. thus, we can just set upperBoundShift
        # to be the max. shift in our spectrum. if both lowerBoundShift and upperBoundShift are corrected, the resulting peak we retrieve
        # will thus be the greatest peak in the entire spectrum
        if lowerBoundShift > upperBoundShift:                                                   # for situations in which fixing the bounds in prior step cause this condition to hold
            upperBoundShift = self.df['shift'].max()

        maxIntensityIdx = self.df[(self.df['shift'] >= lowerBoundShift) & (self.df['shift'] <= upperBoundShift)]['intensity'].idxmax()

        maxIntensity = self.df.iloc[maxIntensityIdx]
        print(maxIntensity)
        
        return maxIntensity

# NOTE: REPLACE with relevant path
spectrumPath = r"path\to\spectrum\file.txt"
spec = Spectrum(spectrumPath)

# DEBUG/Diagnostics
# spec.displayFilePath()
# spec.printSpectrum()

# DISPLAY
spec.plotSpectrum()

# ANALYSIS
peaks = spec.findPeakAtShiftA(3200, 2, False)
peaks = spec.findPeakAtShiftB(3200.42, True)

maxInt = spec.findMaxPeakInRange(500, 800, True)
plt.show()

