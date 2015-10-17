


from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi, zeros
#from scipy.io.wavfile import read,write
import scipy.io.wavfile
import scipy.io
import sys
import glob
import numpy 

def to_fft(y, Fs):
   n = len(y) 
   Y = fft(y)/n # fft computing and normalization
   Y = Y[range(n/2)]
   return Y

Fs = 22500;  # sampling rate

Ys = zeros(25000)
n=0
y=None
for file in glob.glob('airplane_noises/*'):
   print file
   rate,data=scipy.io.wavfile.read(file)
   y=data[:50000]
   print file, len(y)
   Y = to_fft(y, Fs)
   Ys += abs(Y)
   n +=1 

timp=len(Ys)/22500.
t=linspace(0,timp,len(Ys))

k = arange(25000)
T = 1
frq = k/T # two sides frequency range
print T, len(frq), len(Ys)
plot(k,abs(Ys),'r') # plotting the spectrum
numpy.savetxt('airplane_model',Ys)
show()

