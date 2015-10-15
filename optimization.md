When using the Raspberry Pi B the allotted RAM and File Swap available is limited.

Installing SciPy has caused my rPi to freeze multiple times forcing me to reboot each time.  
To help eliminate this issue do the following:
    There is a certain amount of RAM dedicated to the GPU. If you are running this headless you will not need this.
      - Check available RAM by sending free -m
                        total       used       free     shared    buffers     cached
          Mem:           466        454         11          0          0         13
        
      - To free up more memory do the following:
          - As su edit /boot/config.txt
	        - Change gpu_mem=128 to gpu_mem=32
	      - This will free up 96 MB of RAM
	      - You could probably go lower than too but a tutorial I read showed 32.
	  
    To add to the file swap size do the following:
      - Edit  /etc/dphys-swapfile
	      - Default is CONF_SWAPFILE=100
	      - Change to CONF_SWAPFILE=1024
	    - /etc/init.d/dphys-swapfile stop
	    - /etc/init.d/dphys-swapfile start

