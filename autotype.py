#===================================== AutoType =======================================#

'''
Disclamer: this script is used for educational purposes,
as part of a clinical application project at TUM.

Simulates keyboard input that types bash commands to write the contents of a folder.
Tested on Windows using Thonny. Best to execute this from an IDE, it would be tricky
to stop the process in a terminal as the keyboard will be constantly typing.

    1. Prepare the folder you want to copy.
    2. On the target machine, navigate to where you want to put the typed folder.
    3. Run this script, give it a name for future typed folder,
       and the path to the prepared folder.
    4. During the count-down, switch back to where you want the keyboard to type.
       After count-down, the script will start typing.
       Don't touch anything while the script is running.
       Best to keep the typing location windowed.
       To terminate the script, press 'escape'.
       In an emergency, switch back to your IDE and stop the process manually.

'''

import pyautogui # Source: pyautogui.readthedocs.io
import keyboard # For simulating keyboard input.
import time # For the count down.
import os # For decoding file paths and aborting.
import re # For escaping special characters in strings.

#================================== Helper Functions ==================================#

# Typing speed in key strokes per second.
speed = 0 # Default: 0

# Number of files in the source directory. No need to set manually.
fileNumber = 0
finishedFiles = 0

# Characters that cannot be typed by the keyboard.
problemChars = ""

# Type text with keyboard.
def type(text):
    if not speed:
        keyboard.write(text)
    else:
        for c in text:
            keyboard.write(c)
            time.sleep(1 / speed)

# Enter a terminal command.
def cmd(command):
    type(command)
    pyautogui.press('enter')
    
# Create a new directory.
def mkdir(path):
    cmd("mkdir -p \"" + path + "\"")

# Create new file (and potentially its directory) and open it.
def nano(path, fileName):
    cmd("nano -L \"" + path + "/" + fileName + "\"")
    
# Save and quit.
def q():
    with pyautogui.hold('ctrl'):
        time.sleep(2)
        pyautogui.press('s')
        time.sleep(2)
        pyautogui.press('x')
    time.sleep(3)

# Create new file at given path with given content.
def typeFile(path, fileName, content):
    nano(path, fileName)
    type(content)
    q()
    
# Append a line to a file. Create a new file if none exists.
def echoLine(path, fileName, line):
    cmd("echo \"" + line + "\" >> " + path + "/" + fileName)
    
# Count the files in the directory.
def countDir(srcDir):
    global fileNumber
    for file in os.listdir(srcDir):
        srcPath = os.path.join(srcDir, file)
        if os.path.isfile(srcPath):
            fileNumber += 1
        else:
            countDir(srcPath)
   
# Find out which characters in a file cannot be typed.
def testFile(srcPath, content):
    global problemChars
    for c in content:
        try:
            type(c)
        except UnicodeDecodeError:
            print("Failed to type \"" + re.escape(c) + "\" in " + srcPath + "\n")
            problemChars += c
            
# Find out which characters cannot be typed.
def testDir(srcDir):
    global finishedFiles
    for file in os.listdir(srcDir):
        srcPath = os.path.join(srcDir, file)
        if os.path.isfile(srcPath):
            try:
                testFile(str(srcPath), open(srcPath, 'r').read())
            except UnicodeDecodeError:
                print("Failed to type " + str(srcPath))
            finishedFiles += 1
            print("Testing... " + str(int((finishedFiles / fileNumber) * 100)) + "%        ", end='\r')
        else:
            testDir(srcPath)

# Loop over contents of a directory and type them. [2]
def typeDir(srcDir, dstDir):
    global finishedFiles
    mkdir(dstDir)
    for file in os.listdir(srcDir):
        srcPath = os.path.join(srcDir, file)
        fileName = os.fsdecode(file)
        if os.path.isfile(srcPath): 
            typeFile(dstDir, fileName, open(srcPath, 'r').read())
            finishedFiles += 1
            print("Typed " + str(finishedFiles) + " out of " + str(fileNumber) + " files (" + str(int((finishedFiles / fileNumber) * 100)) + "%)        ", end='\r')
        else:
            typeDir(srcPath, dstDir + "/" + fileName)
            
# Loop over contents of a directory and echo them into destination files. [2]
def echoDir(srcDir, dstDir):
    global finishedFiles
    mkdir(dstDir)
    for file in os.listdir(srcDir):
        srcPath = os.path.join(srcDir, file)
        fileName = os.fsdecode(file)
        if os.path.isfile(srcPath):
            #for line in open(srcPath, 'r').readlines():
            #    echoLine(dstDir, fileName, line)
            echoLine(dstDir, fileName, open(srcPath, 'r').read())
            finishedFiles += 1
            print("Typed " + str(finishedFiles) + " out of " + str(fileNumber) + " files (" + str(int((finishedFiles / fileNumber) * 100)) + "%)        ", end='\r')
        else:
            typeDir(srcPath, dstDir + "/" + fileName)
            
# Abort the script. [3]
def abort():
    print("Aborting...             ")
    keyboard.unhook_all()
    os._exit(0)
    

#======================================= Script =======================================#

# Settings
root = str(input("Enter the name of the destination directory to type the files in:\n"))
countDown = 5 # Seconds to wait after running the script before it starts typing..
sourceDir = str(input("Enter the path to the source directory to type:\n"))

# Listen for escape. [4]
keyboard.on_press_key('escape', lambda _:abort())

# Count down before starting the script.
for t in range(countDown, 0, -1):
    print("Starting in " + str(t) + "... ", end='\r') # [1]
    time.sleep(1)

# Count the files in the directory to calculate progress.
print("Counting...         ", end='\r')
countDir(os.fsencode(sourceDir))
print(str(fileNumber) + " files found.        ")

# Test the files for characters that cannot be typed.
#testDir(os.fsencode(sourceDir))
#print("Problem characters: " + re.escape(problemChars))
#finishedFiles = 0

# Type the files.
print("Typing...         ", end='\r')
start = time.time()
typeDir(os.fsencode(sourceDir), root)
#echoDir(os.fsencode(sourceDir), root)
end = time.time()
print("Done. Time: " + str(end-start) + " s.                         ")

#====================================== Sources =======================================#

# [1] https://stackoverflow.com/a/5291396
# [2] https://stackoverflow.com/a/10378012
# [3] https://stackoverflow.com/a/1489838
# [4] https://stackoverflow.com/a/57644349