# ECELD-Netlabel
## Introduction

The purpose of this tool is to develop an annotation standard and augment wireshark to facilitate the tagging of network traffic.

## How to setup (Using fbs freeze on linux, python3)
1. In order for this tool to work you must run wireshark as a non-root user (or make changes to init.lua -- not recommended).
2. Create a virtual environment by running the command 'python3 -m venv venv'
> If you havent installed python's virtual environment you will need to run the command 'apt-get install python3-venv'
3. Activate a virtual environment by running the command 'source venv/bin/activate'
> The rest of the instructions is assuming the virtual environment is active.
4. Next is to run the command 'pip install fbs PyQt5'
> If you get an error try the command 'pip install wheel' and try the fbs command again to verify that it worked.
5. Once fbs is installed go to the project directory (eceld-netlabel) and run the command 'fbs freeze'
> This should have created a target folder, the terminal should also tell you that you can now run 'target/ECELD-NetLabel/ECELD-NetLabel'
6. Run the command mentioned by the terminal and the program should start up.

## How to use the program
1. Start by clicking on the Log Data button and select a folder with log files (this expects parsed ECEL files). Once you select the folder, the window will close and the folder location will appear in the text entry.
2. After you have selected the folder the next thing to do is to pick a wireshark pcapng file, same as before there will be a button named 'wireshark file'. Once you click the button you will be presented with a file chooser window, select the appropriate pcapng file you want, the window will close and the file location will appear in the text entry.
3. Below the wireshark button there will be two boxes from which you can select the range of time the annotator will look for when an nmap is found.
> If you leave the boxes alone the default values will be 0 second before the packet and 2 seconds after the initial packet.
4. When you have selected the appropriate log folder and Wireshark file, there will be a button at the bottom named 'Inject Data'. Once the button is clicked the program will generate lua dissectors that will who up in the Wireshark capture.
5. While the process is taking place another window will appear showing the progress of the lua file generation. When the progress bar reaches 100% the small window will close and the annotation of the wireshark file will be complete.
6. Afterwards, you can open the pcapng specified in (1) with the injected data (lua_dissectors) by clicking on the 'Run Wireshark' button.
