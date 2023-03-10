# Monday QA Board Automation Project
Center for Instructional Design and Innovation - Utah State University
* Created by Emma Lynn (a02391851@usu.edu)
* Supervised by Neal Legler, CIDI Director (neal.legler@usu.edu)
* On request from Neal Legler, CIDI Director & Christopher Phillips, Electronic & Information Technology Accessibility Coordinator

This repository contains a script that will:
* Pull an institution's accessibility report from Blackboard's Ally API
* Combine the accessibility report with other data generated from an institution's Canvas
* Use that data to automatically update a QA board on monday.com

_Note: This program has only been tested on Macs up to this point. If you want to use this on another OS, you are welcome to try it and if there are issues please follow the Bug Report instructions at the bottom of this page to indicate your interest in better support for other Operating Systems._

## Start here!
In these instructions, I will walk you through the process of running this program.
We will be running the program using the Command Line. When I give you a command to run, it will look like this:
```commandline
COMMAND
```
Press enter on your keyboard to run the commands once they have been entered.

Commands may or may not output text. Do not worry if some commands do not display anything.

* _A note: the terminal is an entirely text based application, so you won't be able to navigate the text with your mouse, you will need to use the arrows on the keyboard._


### Instructions

First you will need to get a copy of this project onto your computer.

_If you have experience with git/GitHub, feel free to simply clone the project onto your computer in the normal way. Then skip to setting up your environment._

_If you do not have experience with git/GitHub and would like to try cloning the project instead of downloading the project, follow the instructions in the Cloning a Repository section closer to the bottom of this page. 
The benefit of this method is that as maintenance is performed on the program, you will be able to easily access the updated version of the project._

Navigate to the Launchpad and open the Terminal application on your computer.

On GitHub, click the green Code button. In the dropdown, click Download ZIP.

Unwrap the ZIP file.

----------

**Important:**
There are two ways to run this script. The faster way involves a required file structure and for Box to be set up on your computer. To run the
script in this way, continue following the instructions from here. 
To run the script without the required file structure/Box access, see [**Run Manually**](doc/runManuallyDocs.md)).


The required file structure looks like this:

```commandline
root
????????? Desktop
    ????????? CIDI
         ????????? qa-automation
```

You must have a folder on your Desktop called `CIDI` which must contain the folder holding this project (that you downloaded as a .zip or 
cloned from GitHub.) The folder needs to be renamed to be called `qa-automation`. Naming and locations must be exactly correct, or the script will not work.

Additionally, all old `.zip` files in your Downloads folder beginning with `ally` must be removed before program execution.

You must also have access to Box from your computer. If you have not set up Box Drive, see https://usu.service-now.com/aggies?id=kb_article_view&sysparm_article=KB0012596&sys_kb_id=383c6c1974d2a100cfa6824750f7d4bd#BoxDrive.

Open a command line window and navigate to the project file with the following command:
```commandline
cd Desktop/CIDI/qa-automation
```

Verify that the required file structure is in place with the following command:
```commandline
bash verifyFileStruct.sh
```

You should receive the message `Required file structure verified successfully.` If you do, continue following these instructions. If you do not, 
make the changes to comply with the file structure or see instructions to [**Run Manually**](doc/runManuallyDocs.md).

Now we need to set up your environment with your specific settings.

Run the following command:
```commandline
nano .env
```

Your command line has now been turned into a simple text editor. Copy the text below and paste into the file, replacing the filler text with your information.
  ```commandline
CLIENT_ID=[Your Ally institutional ID]
CONSUMER_KEY=[Your Ally consumer key]
CONSUMER_SECRET=[Your Ally consumer secret]
TERM_CODE=[Semester/term code]
MONDAY_API_KEY=[Your API key for monday.com]
BOARD_ID=[Your monday.com board id]
COURSE_REPORT_FILENAME='course-report-file.xlsx'
```

* [Your Ally institutional ID] should be replaced with your unique Ally institutional ID
* [Your Ally consumer key] should be replaced with your Ally consumer key
* [Your Ally consumer secret] should be replaced with your Ally consumer secret
* [Semester/term code] should be replaced with the code for the term/semester you would like to pull data on (usually a three-digit number)
* [Your API key for monday.com] should be replaced with your API key for monday.com (See https://developer.monday.com/api-reference/docs/authentication)
* [The id for the monday board you're updating] should be replaced with the board id for the monday.com board you're updating (See https://support.monday.com/hc/en-us/articles/360000225709-Board-item-column-and-automation-or-integration-ID-s)
* The last line does not need to be changed.

Once you have correctly filled in the text, press `CTRL + X` on your keyboard, followed by the `y` key, and then the `enter` key.

Download `Python` if you have not already. See https://www.python.org/downloads/.

Now, run the following command in the terminal:
```commandline
bash installDepend.sh
```

_If you receive an error here that says something like:_
```commandline
xrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
```
_Run:_
```commandline
xcode-select --install
```
_And try the previous command again._


Your environment has now been set up!

### <a name="run">**Running the program**</a>

To fill in a blank monday board (at the beginning of a new semester), run:
```commandline
bash runScript.sh -new
```

OR

To update a monday board that already contains content (done throughout the semester), run:
```commandline
bash runScript.sh -update
```

When the script finishes running, the board will have been updated automatically on monday.com.

### Rerunning the Program

Make sure you're in the correct folder in the terminal. Run the following command:
```commandline
pwd
```
The resulting path should look like this: `/Users/username/Desktop/CIDI/qa-automation`

Run the following command  to verify that the required file structure is still in place.
```commandline
bash verifyFileStruct.sh
```

Run the following command to update the term id or other information if necessary:
```commandline
nano .env
```
Once you have correctly filled in the text, press `CTRL + X` on your keyboard, followed by the `y` key, and then the `enter` key.

Now restart these instructions beginning at [**Running the program**](#run)



### Cloning a GitHub repository:
Run the following commands one at a time:
```commandline
cd Desktop
mkdir CIDI
git clone https://github.com/elynn-usu/cidi-monday-QA-automation.git qa-automation
cd qa-automation
```
_If you receive an error that says something like:_
```commandline
xrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
```
_Run:_
```commandline
xcode-select --install
```
_And try the previous command again._

You should now have a copy of the project on your computer. To get the latest changes before running the program in the future, run the following commands 
(after opening a new terminal window):
```commandline
cd Desktop/CIDI/qa-automation
git pull origin main
```
The project should update with any changes and bug fixes.

_If you are having issues with cloning the project, feel free to go back and try downloading the zip as is instructed in the original instructions. You can also email me (a02391851@usu.edu) and I can help you set everything up if you would prefer._

You can now return to the original instructions. Begin at the section on setting up your environment.

## Bug Reports
If something behaves unexpectedly, or you run into a problem with the program, please let me know.

Send bug reports to a02391851@usu.edu with the subject line "Bug Report - Monday QA Automation".

Please include:
* What you expected to happen
* What actually happened
* As much output from the terminal as possible - copy and pasted, not in a screenshot
* Look in the project folder. The file performanceReport0000000.txt may have been created (where `0000000` is a generated 7 digit number). Please attach this file to your bug report if it has been created.
* What OS you're using (Windows, Mac)
* If you are running the program manually or fully automatically
* Any other information that you think could be useful

I will get back to you promptly with an update. Thank you.