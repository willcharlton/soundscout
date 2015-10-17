from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi, zeros
#from scipy.io.wavfile import read,write
import scipy.io.wavfile, scipy.io, sys, glob, numpy 
import time, recorder

samples = 50000
freqrange = 25000
samplerate = 22500
def to_fft(y, Fs): 
 n = len(y) 
 Y = fft(y)/n # fft computing and normalization
 Y = Y[range(n/2)]
 return Y

Fs = samplerate;  # sampling rate



def do_check():
   Ys = zeros(freqrange)
   rate,data=scipy.io.wavfile.read('tempfile.wav')
   if rate != 22500:
      print "Rate REALLY NEEDS to be 22500"
      sys.exit(1)
   y=data[:samples]
   Y = to_fft(y, Fs)
   Ys += abs(Y)

   norm=numpy.loadtxt('airplane_model')

   #timp=len(Ys)/float(samplerate)
   #t=linspace(0,timp,len(Ys))

   k = arange(freqrange)
   T = 1
   frq = k/T # two sides frequency range
   Ys = Ys / sum(Ys)
   Ys = Ys[1:]
   norm = norm[1:]
   norm = norm / sum(norm)
   #plot(arange(25000), abs(norm))
   print sum(norm), sum(Ys)
   airplane_ness = sum((Ys-norm)**2)
   amplitude = sum(abs(y))/samples
   print sum(abs(y))/samples, airplane_ness
   if amplitude > 1000 and airplane_ness < 0.00025:
      print "PROBABLY AN AIRPLANE"
   #plot(arange(24999), abs(Ys-norm)*1000)
   #show()

while True:
   recorder.record()
   do_check()
