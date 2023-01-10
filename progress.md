# Monday QA Board Automation Project
Center for Instructional Design and Innovation - Utah State University
* Created by Emma Lynn (a02391851@usu.edu)
* Supervised by Neal Legler, CIDI Director (neal.legler@usu.edu)
* On request from Neal Legler, CIDI Director & Christopher Phillips, Electronic & Information Technology Accessibility Coordinator


**_Documentation of progress on the project_**

## Project Goals
Automate updating the QA monday board from Meghan's data and the Ally accessibility report
### Objectives
1. Combine Meghan’s spreadsheet (Course Summary on Box) and the Ally report (from the Ally Institution Report on canvas -> export by term)
   * Format with the monday board headers
   * Meghan's data will have them, so just insert the Ally information
2. Given a monday board id, load the spreadsheet generated from step 1 into monday
   * Courses loaded into correct section of board based off enrollments
3. Create update process
   * Run steps one and two on a board already populated with data
   * Match and skip courses already on the board
   * Think about updating
     * If a course gets cross listed or changed some other way later, we don't know how we'd match to the old course
     * So we may run into duplication concerns
     * Possibly remedied in phase 4 - active data lake gives us information that allows us to match former and newly cross listed courses
4. Import everything straight from the data lake into monday
   * _Assumes that we have an active data lake_
   * ON HOLD
_Notes:_
   * Phases 2 & 3 could continue to be done manually if automating them would be too hard (hmm is that a challenge?? :/)
   * Phase 4 cannot be completed until the data lake is finished- on hold pending Meghan and her team

### Steps
#### Phase 1
* Maybe do a little research on combining .csv files
* Write the program
  * Figure out pulling Ally data from their API for just one term
* Create temporary usage documentation
* Share progress with team
* _Notes:_
  * Not anticipating this to be too difficult
    * Okay well so I wrote this before I knew we'd have to get the Ally data from their API so it is proving to be a bit more complicated than I was thinking, oops
* Phase 1 completed 12.15.22
#### Phase 2
* Changing this to keep using the import excel/csv tool, this phase will now be creating a spreadsheet that is formatted correctly for import to monday
#### Phase 3
* 
#### Phase 4
* ON HOLD


## Progress Report

### 12.2.2022
* Began researching the monday API
* Requested a demonstration of how the board is manually updated
* Requested access to a "practice" monday board
* Did research on the monday app development framework
* I'm not exactly sure what the best course of action to start this will be until I can meet with Neal and get some more clarification on exactly what I need to be doing. I will set up a meeting with him for clarification on the project requirements and then return to the project.

### 12.6.22
* Met with Neal and Jenn and went over the manual process of updating the monday board
* Meeting notes:
  * Pull data for columns up to images in use 
  * Download course summary – Meghan's 
  * Export template from monday board 
  * Remove logo and hyperlink 
  * Manually sort into groups of number of students 
  * Remove all QA rubric categories (after images in use but KEEP item id)
  * Look into Ally api?? Neal forwarded email 
  * Ally report – the one we downloaded from canvas - Neal slacked
1. Combine Meghan’s and the ally report 
   * With monday board headers 
   * Maybe we’ll get Meghan to get her output to match monday – yes write it like that
2. Given board id, script will load the data into monday
   * Manual option could be done if necessary 
   * Items go into group by number of students 
3. Create update process 
   * Doing steps one and two with match & update or skip 
   * Maybe just match and skip? Weird exceptions with updating 
   * If a course gets cross listed later and is all different idk how we’d match 
   * Hmmmmm
4. Generate a spreadsheet or JSON or something to import to monday from the data lake 
   * _Assumes that we have an active data lake_
   * ON HOLD
* Updated project documentation based off meeting
* Began working on phase 1 - read in .xlsx file

### 12.7.22
* Created mock up of program for small test data
* Moving on to the actual format
* Which Ally report will we be using? Can we get one with just the specified term or do we need to use the one with all the data for all time?
* Talked with Christopher about using the Ally API to get data from just one semester
    * I think this is the API call I want: `GET /api/v1/:clientId/reports/terms/:termId/csv`
    * Christopher is going to show me the other project that is using it, as well as helping me get authenticated
    
### 12.8.22
* Working on getting Ally data from their API
* Got search and match functionality working for the small test data
* Talked with Christopher about using OAth, maybe going to set up a meeting with Tyler for this afternoon
* Read over OAuth python library docs
* Tyler said he'd try to figure out the Ally API, I'm going to look at it as well and see if I can come up with my own jumping off point
* Looked at it a little more- I think mostly what I'm confused about it all the urls- the walkthrough of requests-outhlib from the documentation is talking about all sorts of URLS and idk which one is for what
  * Feeling kind of stuck - I might just wait and see what Tyler comes up with
* In the meantime, beginning to do research for step 2
* So it looks like there's not a specific API call that completes the import process from a .csv, we pay for a third party app
  * If I could have their code that would be great but that is not happening
  * So I'm thinking maybe I build our own monday app?? That is compatible with the import script I'm writing
  * Although that might be a lot a lot of work just to eliminate like literally just selecting a file to upload... so maybe it's not worth it... or it could be something that gets worked on slowly over time and is an eventual goal
* Looked at the monday app SDK, built a little hello world app

### 12.9.22
* Continued looking at OAuth requests, figured out how to make the API call to get the Ally data!!!
* Added dotenv dependencies for secure information
* Talked through a new plan with Neal:
    * Merge Meghan’s Course Report CSV and the Ally report. Since we’ll fiddle with so many CSVs, we can give them fancy sounding names for shorthand. I’ll call the result of this the Merged Active Course Report (MACR).
    * Get a clean CSV with the existing names, course URLs (which will have the course ID) and the item IDs out of Monday.com. I’ll call it the Monday Item Match File (MIMF).
    * Match, to the extent possible, the courses in the MACR with the corresponding items in the MIMF to get the Monday item IDs for the courses we have already added to our board. Add the item IDs to the MACR to get the Importable Merged Active Course Report (IMACR).
    * Then we can manually load the IMACR into the Monday board using the Update With CSV tool.
* Script written to download ally data and move to current project directory
    * We can't have the command to download the zip and the commands to manipulate the zip file in the same shell script- it moves too fast and the zip isn't ready by the time the shell script is finished
    * Current commands to run:
      * `$ python3 getAllyData.py`
      * `$ bash generateFile.sh`
* Next steps: figure out what format Meghan's data is going to be in, begin writing merge process
    * I'm guessing we'll need two or three merges depending on if Meghan's data is formatted correctly already:
        * Merge Meghan's data in with a blank sheet with monday headers (If it is not already done)
        * Merge the Ally report with Meghan's report
        * Download the current monday board, merge in with existing data (get monday item ids)
    * To download the current monday board I'll need to figure out the monday API

### 12.13.22
* Talked with Meghan, she's going to try to get her data formatted correctly and sent over tomorrow
* Found descriptions of where information in the final report comes from in the monday heading sources key (linked in sources below)

### 12.14.22
* Meghan sent over her new data and it looks great!
    * Merge 0 can be skipped
* Started figuring out merge 1: running into `Incompatible indexer with Series` error- hmm....

### 12.15.22
* Continued working on merge 1
    * Resolved `Incompatible indexer with Series` error
    * Files are being combined successfully, removed several extra unnecessary searches
    * Tested with full data, works great!
* Fixed a problem with the Ally report pending
* Connected the merge process with the process to get the Ally data
* Shell script is being weird - figure that out later
    * Program is ran with:
        * `$ python3 getAllyData.py`
        * `$ python3 combineSheets.py`
* Merge 1 complete, moving on to merge 2 - pausing for a minute to work on other project
* Phase 1 complete

### 12.16.22
* Time stamp for ally report - add to the end of url: `&token=2022-12-16-8-18`
* Began working on merge with monday template
    * For each line in the FilledInFile, add to the correct list by number of students (100+, 50-99, 20-49, 10-19, 1-9, None)
    * Grab monday header rows, insert at top of each section
* Merge almost complete, just need to clean up I think

### 12.19.22
* Program is ran with:
  * `$ python3 getAllyData.py`
  * `$ python3 combineSheets.py`
  * `$ python3 mergeWithMonday.py`
* Cleaned up mergeWithMonday and tested with whole data
* getAllyData's not working?? I'm wondering is it because I'm not on USU's network? So the API call fails? But also idk hmm
  * Maybe try setting up the VPN later to see if that helps
* mergeWithMonday is basically done, I need to do more testing possibly, make it so bad data just gets skipped and doesn't crash the program
* Tested an import to monday, went fairly smoothly
  * Problems with `"Humanities Arts & Social Scie"`, `Agriculture & Applied Sciences`, I guess maybe all the things I changed? Check that

### 12.20.22
* Wrote shell script that will install all the dependencies
* Wrote usage documentation
* Updated performance report
* Figured out commas in data - mostly...
  * Quotation marks have to stay
* Added time stamp to Ally API call

### 12.26.22
* Fixed `Humanities, Arts & Social Scie`'s comma not getting merged back in
  * `Humanities, Arts & Social Scie` is a college not a department, in column 6 not 7 smh
* Figured out clean up- running more than once
* Tried to see if the USU VPN would fix getAllyData's authentication problem - did not seem to help at all :(
* Started drafting something asking what I should do about the absolute path thing
* Added license as prep for moving to public repo

### 12.29.22
* Asked Neal about how streamlined the process should be, absolute paths and stuff
* Got Hayden to try running the getAllyData file on USU's network to see if that's really the problem
  * Apparently he's getting the same error as me... so it's not the network hmm :/
* Asked Neal about licenses, he says the GNU GPL works just fine
* Updated license for 2023
* Added more robust exception handling
* Figuring out what's going on with missing values in the `FilledInFile`? (Overall Ally, Files Ally, WYSIWYG Ally)
  * Not a problem, no Ally data available- probably mostly from testing with the less recently updated Ally data
* Began working on phase 3 tasks since there's nothing left I can do on phase 2 until I'm back in the office
* Started working on script to match courses in an existing monday board - update process
  * Merge with existing board in progress
    
### 1.3.23
* Back in the office, problems with `getAllyData` resolved
    * Authentication was copied down wrong
* Figured out getAllyData's issues - updated README
  * Checked my authentication
  * VPN did not seem to help - but the VPN could just have network restrictions
  * Not a network problem
* Tested the whole process - phase 2
* Cleaned up and moved to public repository
* Continuing with phase 3
* Merge just about finished I think
    * Testing with monday import but it's taking a really long time ?? :(
* Added to report
* Researched options to download the current board with the monday API
* Finished set up for everything in phase 3 besides getting the current board from the monday API
    * Pushed to public repo
    
### 1.4.23
* Worked with a script I found that will download a monday board as a csv, not sure if it's gonna pan out
    * I maybe should just write my own
* Sooo I've realized that I've been doing about this the wrong way..
    * I've been trying to follow the manual update process which has been really holding the project back :/
    * I should change it so that I'm just doing the update using the API

### 1.5.22
* Kept working on using the monday API
```commandline
def slowCreateNewItem(itemName):
    newItemQuery = f'mutation{{ create_item(board_id: {BOARD_ID}, item_name: "{itemName}") {{ id name }} }}'
    data = {'query': newItemQuery}

    r = requests.post(url=apiUrl, json=data, headers=headers)

    jsonObj = json.loads(r.content)
    jsonPretty = json.dumps(jsonObj, indent=2)

    print(jsonPretty)

    return jsonObj["data"]["create_item"]["id"]

def slowUpdateRow(itemID, rowInfo):
    index = 0
    for col in COL_IDS:
        index += 1
        updateItemQuery = f'mutation{{ change_simple_column_value (board_id: {BOARD_ID}, item_id: {itemID}, ' \
                          f'column_id: {col}, value: "{rowInfo[index]}") {{ name id }}}}'
        data = {'query': updateItemQuery}

        r = requests.post(url=apiUrl, json=data, headers=headers)
```
* It's working great, I've got it mostly figured out now except for the groups which I'm looking at now
* Okay I think it's done, haven't really tested it but we're in a super great place

### 1.6.23
* Testing the new script
* Ran into JSON error - probably should add some try-except blocks for some of the API calls
* Fixed a problem with moving rows to the correct group where the original number of students is not recorded until after the data is updated
* Added to report in updateMondayAPI.py
* Added exception handling
* Updated docs
* Tested with a full FilledInFile - success!! Took a while though... 
* Figured out Study Abroad delivery methods

### 1.9.23
* Tested the whole update process
* Pushed changes to public repo
    * Changes:
        * `generateUpdateFile.sh`
        * `progress.md`
        * `README.md`
        * Delete `mergeExistingBoard.py` and replace with `updateMondayAPI.py`
* Added `fillNewBoard.py` on branch `fix-intial-upload`

### 1.10.23
* Changed populating an empty board to use the new method
  * Updated docs again
  * Pushed to `main` branch
* Tried to see if I can improve runtime
    * Worked on trying to limit the number of repeat courses that show up in the `FilledInFile`
* Demonstrated usage to Neal and Jenn, helped Jenn with set up

### TODO:
Phase 4
* ON HOLD
Misc
* `/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/internals/blocks.py:2323: RuntimeWarning: invalid value encountered in cast
  values = values.astype(str)`?

## Dependencies:
* pandas: `pip3 install pandas`
* openpyxl: `pip3 install openpyxl`
* Requests-OAuthlib: `pip3 install requests-oauthlib`
* dotenv: `pip3 install python-dotenv --user`

## Sources & References:
* monday heading sources key: https://docs.google.com/spreadsheets/d/1omE1g2X3PZ_4EnKb5MrIxgp5HzXU-8NgndnksSC_x5A/edit#gid=1453652472
* monday API playground: https://cidi-gang.monday.com/apps/playground
* monday app docs: https://developer.monday.com/apps/docs/intro
* monday API docs: https://developer.monday.com/api-reference/docs
* monday API docs (graphQL): https://developer.monday.com/api-reference/docs/introduction-to-graphql
* monday board ids: https://support.monday.com/hc/en-us/articles/360000225709-Board-item-column-and-automation-or-integration-ID-s
* monday apps: https://developer.monday.com/apps/docs/quickstart-integration
* CIDI QA board update documentation: https://usu-accessibility.kbee.app/page/10CD2AmsWRlH7cmSNiqGi3xDgX_cWBinKfLFlJ18f_2A/Canvas-Course-Summary-Update
* Ally accessibility API docs: https://usergroup.ally.ac/file/file/download?guid=64b06a7b-2eb4-4ee0-899c-6ad07768b2cc
* Reading excel files: https://linuxhint.com/read-excel-file-python/#:~:text=The%20read_excel()%20function%20of,in%20the%20variable%20named%20data.
* monday header template: https://docs.google.com/spreadsheets/d/1gI74H1U4iMm95gjg6i8RZO4OXesYZBh2EsNH0yLsph4/edit#gid=0
* Editing .csv file: https://www.geeksforgeeks.org/update-column-value-of-csv-in-python/
* Read .csv file: https://www.geeksforgeeks.org/python-read-csv-columns-into-list/
* Access project already using Ally API: https://github.com/usu-access/file_to_page/blob/master/action.php
* OAth python library: https://pypi.org/project/oauthlib/
* OAuthLib docs: https://oauthlib.readthedocs.io/en/latest/index.html
* Requests-OAuthlib: https://github.com/requests/requests-oauthlib
  * https://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html
* Requests docs: https://requests.readthedocs.io/en/latest/
* monday app quickstart guide: https://developer.monday.com/apps/docs/quickstart-view
* monday apps marketplace listing for Update with Excel / CSV ADF Tech tool: https://monday.com/marketplace/90
  * Docs: https://adftech.net/monday/update-with-excel-csv
* Help with requests_oauthlib: https://stackoverflow.com/questions/11085341/simple-python-oauth-1-0-example-with-consumer-key-and-secret
* Byte strings: https://www.geeksforgeeks.org/effect-of-b-character-in-front-of-a-string-literal-in-python/#:~:text=In%20python%2C%20the%20'b',I%20am%20a%20byte%20String'
* OAuth requests explanation: https://testdriven.io/blog/oauth-python/
* Pandas dtyping: https://www.roelpeters.be/solved-dtypewarning-columns-have-mixed-types-specify-dtype-option-on-import-or-set-low-memory-in-pandas/
* Pandas loc: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
* More Pandas loc: https://sparkbyexamples.com/pandas/pandas-select-multiple-columns-in-dataframe/
* Insert row into pandas dataframe: https://www.geeksforgeeks.org/insert-row-at-given-position-in-pandas-dataframe/
* Citing code: https://uark.libguides.com/CSCE/CitingCode
* USU VPN: https://usu.service-now.com/aggies?id=kb_article_view&sys_kb_id=6f0283fe30f0d100817928f01ee68460
* Links in markdown: https://stackoverflow.com/questions/2822089/how-to-link-to-part-of-the-same-document-in-markdown
* Python exit codes: https://linuxhint.com/python-exit-codes/#:~:text=Python%20has%20only%20two%20standard,process%20exited%20with%20a%20failure.
* About open source licenses: https://gist.github.com/nicolasdao/a7adda51f2f185e8d2700e1573d8a633
* Search dataframe column: https://thispointer.com/how-to-check-if-a-pandas-column-contains-a-value/
* Pandas read_excel: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
* Dataframe header rows: https://www.geeksforgeeks.org/how-to-add-header-row-to-a-pandas-dataframe/
* Simple column values - monday API: https://community.monday.com/t/introducing-simple-column-values-for-api/12831
* Changing column values - monday API: https://developer.monday.com/api-reference/docs/change-column-values
* Monday API python: https://support.monday.com/hc/en-us/articles/360013483119-API-Quickstart-Tutorial-Python
* Items - monday API: https://developer.monday.com/api-reference/docs/items-queries
* Column values - monday API: https://developer.monday.com/api-reference/docs/column-values
* Git branching: https://gitlab.cs.usu.edu/erik.falor/fa22-cs1440-lecturenotes/-/blob/master/Module4/Advanced_Git.md






