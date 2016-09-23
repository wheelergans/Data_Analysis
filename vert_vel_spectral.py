from scipy.signal import butter,lfilter,freqz,csd,welch,periodogram
import pylab
import pandas as pd
import matplotlib.pyplot as plt
plt.interactive(True)


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


gpsdata.columns = [['lat','N/S','long','E/W','SOG','COG','Vert']]
gpsdata = gpsdata.apply(pd.to_numeric,errors ='ignore')

gpsdata.Vert = gpsdata.Vert-gpsdata.Vert.mean()

#resample to ensure even dt
Vert = pd.DataFrame(gpsdata.Vert.resample('200L').mean())
#fill any missing points
Vert.fillna(method ='bfill',inplace=True) #fill nan values does not seem to work within resample function


#Highpass filter
cutoff = 1/40 #cutoff frequency in hertz
order = 6 #filter order
fs = 5 #sample frequency


#Subtract mean and plot






# Get the filter coefficients so we can check its frequency response.
b, a = butter_highpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Highpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()

Vert['filtered']=butter_highpass_filter(Vert.Vert,cutoff,fs,order)



#compute cross spectral density
f,pxx =welch(Vert.filtered.values.flatten(),5)
f1,pxx1 =welch(Vert.Vert.values.flatten(),5)
T = 1/f
ax = plt.plot(f,pxx)
plt.plot(f1,pxx1)
ax.set_yscale('log')

#make sure these are equal
Vert.filtered.std()**2
pxx.sum()*f[1]
