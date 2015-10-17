import sys, csv, os, pyonep, json
url = "http://m2.exosite.com/onep:v1/stack/alias"
cik = "d9b359e0f00295d2e607471ac5797dde62528736"

def upload(planes):
    data= json.dumps({'version':1,'planes':planes})
    o = pyonep.OnepV1()
    o.write(cik, {'alias':'adsb'}, data)

def capture_planes():
   os.system("(./dump1090 > out & (sleep 30 && killall dump1090))")

def read_planes():
   lines=open('out').readlines()
   s=[]
   for line in lines: 
      if line.startswith("  ICAO Address: "):
          s+=[line.split(':')[1][1:-1]]
   return list(set(s))

def correlate_planes(planes):
   out=[]
   for plane in planes:
      with open('aircrafts_dump.csv','rb') as csvfile:
         myreader = csv.reader(csvfile, delimiter=',', quotechar='"')
         for row in myreader: 
            if row[0].upper()==plane.upper():
               out+=[row[7]+" "+row[6]]
   return out

def upload_planes(planes):
   upload(planes)

last_planes=[]
while True:
   capture_planes()
   planes=read_planes()
   planes=correlate_planes(planes)
   if planes==[]:
      print("There are no planes :(")
   if planes != last_planes and planes != []:
      print("FOUND NEW PLANES", planes, last_planes)
      upload_planes(planes)
      last_planes = planes
