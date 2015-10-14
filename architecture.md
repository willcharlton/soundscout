# Architecture - `soundscout`
This document is here to provide some thoughts on proposed architecture of the `soundscout` product.

## Overview
The `soundscout` project is a multi-phased product that has enormous potential in public health, rural and urban research, and passive surveillance of a home-owner's property.

## Phase 1
Phase 1 is geared towards urban property owners, namely those who live near airports. The `soundscout` will provide 2 points of data. One that is continuously sampling the relative loudness in dB SPL (Decibels Sound Pressure Level), and the second is the output of a hashing / fingerprinting algorithm that does a 'best effort' to guess whether or not a given sound it heard was a commercial aircraft. 

The `soundscout` is currently supported on a Rasperry Pi B+ with Python 3.4.3 as it core programming driver.

## Phase N
Once Phase 1 can be proven and demonstrated, the plan for `soundscout` is to refine its fingerprinting capabilities. Applications I have in mind for Phase 2 are recognizing bird calls, when the garbage truck comes, dogs barking, gunshots and any other sound that might be interesting to the owner of the given `soundscout`. Phase 2 should also serve up a website on the home-owner's WiFi network that displays recent activity and asks the user for input on some recent unknown sounds. A use case can be devised where if the `soundscout` hears the same sound a few times, it will passively notify the owner about it on its local website, asking if the owner cares enough to identify it for the `soundscout` and whether she wants it to continue reporting on the sound.

# Nitty-Gritty
To accomplish all of this, I see the `soundscout` Python application taking on an architecture something like the following.

```
/usr/bin/ss
    > Main-Thread
        > Thread-1
        > Thread-2 (*possibly another thread here)
        > Thread-3
        > Thread-4
```

## /usr/bin/ss
Just the name of the binary running `soundscout`.

## Main-Thread
Not much important stuff here. Probably just logging setups and object instantiations. Interthread messaging systems can be devised at this level as well.

### Thread-1
Handles audio input stream from the microphone.
### Thread-2
#### Possible algorithm #1
Analyzes audio stream from Thread-1 and runs algorithm that determines whether or not a given period of the audio stream can be 'clipped' and saved as a `.wav` file. This algorithm operates a sliding window with the following pseudo routine.

               |snd-a  |   sound-b       |  no-sound      | snd-c | snd-d  |
                           ..       .                       
                  ..      ....  .. ...                      . ..      ..
                 ....    ................                   ......    .....
             .................................................................
*Note: in this drawing, signal amplitude is the Y-axis, time is the X-axis.*

Thread-2's job is to analyze the input audio stream and make a determination on whether or not a given period of time should be identified as a separate sound based on whether or not it was quiet, then loud, then quiet again. This algorithm might work well for airplanes, but maybe not so much on sounds with lower amplitudes and more interesting frequency characteristics.

#### Possible algorithm #1
Analyzes audio stream from Thread-2 and runs algorithm that determines whether or not a given period of of the input audio stream can be clipped and saved as a `.wav` file

               |snd-a  |   sound-b       |  no-sound      | snd-c | snd-d  |
                  .        ..       .                        .
                 ...      ....  .. ...                      . ..      ..
                 ..        ...  ...                         .. ..    . ...
                .....     ......... ..                          .    ..
*Note: in this drawing, signal amplitude is the Y-axis, time is the X-axis.*

#### Possible algorithm #3
Use both, each as their own thread, catalog each `clip` in a clip database with the findings of these analysis threads.

### Thread-3
This thread takes the `clips` that the other threads have preprocessed and analyzes them for their frequency characteristics and creates the fingerprints of each one.

### Thread-4
This is the reporting thread. It reports db SPL every second as well as whether or not it heard a airplane and its maximum db SPL during the airplane event.

#### dB SPL Reporting
A `FIFO` can be set up between threads `1` and `4` for the dB SPL reporting we will do every second. This will be done so we're not making the same dB SPL calculation twice. This report will be performed by the [Exosite HTTP Write API](http://docs.exosite.com/http/#write).

#### Aircraft Overhead Reporting
The same API will be used as the db SLP reports, but these will only get reported when the `soundscout` thinks it 'heard' an airplane.

