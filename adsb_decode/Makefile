CFLAGS=-O2 -g -Wall -W `pkg-config --cflags librtlsdr`
LIBS=-lrtlsdr -lusb -lpthread -lm
CC=gcc
PROGNAME=dump1090

all: dump1090

%.o: %.c
	$(CC) $(CFLAGS) -c $<

dump1090: dump1090.o anet.o
	$(CC) -g -o dump1090 dump1090.o anet.o $(LIBS)

clean:
	rm -f *.o dump1090
