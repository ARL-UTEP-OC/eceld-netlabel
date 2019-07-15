# ECELD-Netlabel
## Introduction

The purpose of this tool is to develop an annotation standard and augment wireshark to facilitate the tagging of network traffic.

## How to setup (Using fbs freeze on linux)
1. In order for this tool to work you must disable lua in wireshark.
2. Create a virtual environment by running the command 'python3 -m venv venv'
3. Activate a virtual environment by running the command 'source venv/bin/activate'
> The rest of the instructions is assuming the virtual environment is active.
4. Next is to run the command 'pip install fbs PyQt5'
> If you get an error try the command 'pip install wheel' and try the fbs command again to verify that it worked.
5. Once fbs is installed go to the project directory (eceld-netlabel) and run the command 'fbs freeze'
> This should have created a target folder, the terminal should also tell you that you can now run 'target/ECELD-NetLabel/ECELD-NetLabel'
6. Run the command mentioned by the terminal and the program should start up.

## How to use the program
1. On the top it should say to pick a JSON file, under and to the left there is a button that when clicked will make a file chooser window appear. Once you select the appropriate JSON file the window will close and the file location will appear in the text entry.
2. After you have selected the JSON file the next thing to do is to pick a wireshark pcapng file, same as before there will be a button named 'wireshark file'. Once you click the button you will be presented with a file chooser window, select the appropriate pcapng file you want, the window will close and the file location will appear in the text entry.
3. When you have selected the appropriate JSON file and Wireshark file, there will be a button at the bottom named 'Annotate'. Once the button is clicked the program will start the adding comments to the selected wireshark files.
4. While the annotation is taking place another window will appear showing the progress of the annotation. When the progress bar reaches 100% the small window will close and the annotation of the wireshark file will be complete.
5. You can also open up wireshark from within the application by clicking the 'Run Wireshark' which will open up a wireshark window.
> Note that if you annotate and have wireshark open with the same file you are annotating, can in some cases cause the file to become corrupted or unable to open.