#from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi, zeros
#from scipy.io.wavfile import read,write
import scipy.io.wavfile, scipy.io, sys, glob, numpy 
import time, recorder

import urllib, urllib3, urllib.parse, json
import pyonep
url = "http://m2.exosite.com/onep:v1/stack/alias"
cik = "d9b359e0f00295d2e607471ac5797dde62528736"

samples = 50000
freqrange = 25000
samplerate = 22500

amplitude_threshold = 1000
airplane_ness_threshold = 0.00023

def upload(amplitude, airplane_ness):
#   data = {'soundscout': '666'}
    data= json.dumps(
         {'version':1,'amplitude':amplitude,'airplane_ness':airplane_ness})
#   headers={"X-Exosite-CIK":cik,
#            'Accept':'application/x-www-form-urlencoded; charset=utf-8' }
#  http = urllib3.PoolManager()
#  req = http.request_encode_body('POST', fields=data,url=url,headers=headers)
#   print(req.fields, req.url, req.headers)
#req = urllib3.Request(url, data, headers)
#   content = req.read() #urllib2.urlopen(req).read()
#   print(content, req.status)
    o = pyonep.OnepV1()
    o.write(cik, {'alias':'soundscout'}, data)

def to_fft(y, Fs): 
   n = len(y) 
   Y = fft(y)/n # fft computing and normalization
   #print len(
   Y = Y[:freqrange] #range(freqrange)]
   return Y

Fs = samplerate;  # sampling rate

def do_check():
   Ys = zeros(freqrange)
   rate,data=scipy.io.wavfile.read('tempfile.wav')
   if rate != 22500:
      #print "Rate REALLY NEEDS to be 22500"
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
   #print sum(norm), sum(Ys)
   airplane_ness = sum((Ys-norm)**2)
   amplitude = sum(abs(y))/samples
   #print sum(abs(y))/samples, airplane_ness
   print(amplitude, airplane_ness)
   upload(amplitude,airplane_ness)
   if amplitude > amplitude_threshold and airplane_ness < airplane_ness_threshold:
      print("PROBABLY AN AIRPLANE")
   #plot(arange(24999), abs(Ys-norm)*1000)
   #show()

while True:
   #print "RECORD"
   recorder.record()
   #print "CHECK"
   do_check()
