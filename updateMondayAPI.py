# Copyright (C) 2023  Emma Lynn
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
import json
import sys
import dotenv
import os
from time import time

def writeToReport(label, object):
    f = open("performanceReport3850265.txt", "a")
    f.write(f"{label}: {object}\n")
    f.close()

def splitLine(line):

    newLine = line.replace("Animal, Dairy & Vet Sciences", "Animal Dairy & Vet Sciences")
    newLine = newLine.replace("Plants, Soils and Climate", "Plants Soils and Climate")
    newLine = newLine.replace("Nutrition, Dietetics &Food Sci", "Nutrition Dietetics &Food Sci")
    newLine = newLine.replace("Humanities, Arts & Social Scie", "Humanities Arts & Social Scie")
    newLine = newLine.replace("Technology, Design & Technical", "Technology Design & Technical")

    newLine = newLine.replace("Study Abroad", "Supervised")
    newLine = newLine.replace("Disability Resource Center", "CPD")

    splitData = newLine.split(",")

    if (splitData[NUM_STU_INDEX - 2] == '"Animal Dairy & Vet Sciences"'):
        splitData[NUM_STU_INDEX - 2] = "Animal, Dairy & Vet Sciences"
    elif (splitData[NUM_STU_INDEX - 2] == '"Plants Soils and Climate"'):
        splitData[NUM_STU_INDEX - 2] = 'Plants, Soils and Climate'
    elif (splitData[NUM_STU_INDEX - 2] == '"Nutrition Dietetics &Food Sci"'):
        splitData[NUM_STU_INDEX - 2] = "Nutrition, Dietetics &Food Sci"
    elif (splitData[NUM_STU_INDEX - 3] == '"Humanities Arts & Social Scie"'):
        splitData[NUM_STU_INDEX - 3] = "Humanities, Arts & Social Scie"
    elif (splitData[NUM_STU_INDEX - 3] == '"Technology Design & Technical"'):
        splitData[NUM_STU_INDEX - 3] = "Technology, Design & Technical"

    return splitData

def findGroupID(numStu):
    for lowerLimit in GROUP_IDS:
        if int(numStu) >= lowerLimit:
            writeToReport("Group ID", GROUP_IDS[lowerLimit])
            return GROUP_IDS[lowerLimit]
    writeToReport("Group ID", GROUP_IDS[0])
    return GROUP_IDS[0]

def updateRow(itemID, rowInfo):
    query = f'mutation ($columnVals: JSON!) {{ change_multiple_column_values (board_id:{BOARD_ID}, item_id: {itemID}, column_values:$columnVals) {{ name id }} }}'
    writeToReport("Attempting query", query)
    colVals = dict(zip(COL_IDS, rowInfo[1:]))
    vars = {
        'columnVals': json.dumps(colVals)
    }

    data = {'query': query, 'variables': vars}

    try:
        r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
        writeToReport("Response", r.json())
        return r.json()["data"]["change_multiple_column_values"]["id"]
    except Exception as e:
        writeToReport("Exception in API call/JSON", e)
        return None

def createNewItem(rowInfo):
    groupID = findGroupID(rowInfo[NUM_STU_INDEX])
    query = f'mutation ($myItemName: String!, $columnVals: JSON!) {{ create_item (board_id:{BOARD_ID}, group_id:{groupID}, item_name:$myItemName, column_values:$columnVals) {{ id }} }}'
    writeToReport("Attempting query", query)
    colVals = dict(zip(COL_IDS, rowInfo[1:]))
    vars = {
        'myItemName': rowInfo[0],
        'columnVals': json.dumps(colVals)
    }

    data = {'query': query, 'variables': vars}

    try:
        r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
        writeToReport("Response", r.json())

        #print(r.json())
        return r.json()["data"]["create_item"]["id"]
    except Exception as e:
        writeToReport("Exception in API call/JSON", e)
        return None

def makeSureInRightGroup(itemID, newNumStu, OGNumStu):
    writeToReport("in makeSureInRightGroup", "")

    if newNumStu != int(OGNumStu):
        writeToReport("the numbers don't match, moving it", '')
        groupID = findGroupID(newNumStu)

        mutation = f'mutation {{move_item_to_group (item_id: {itemID}, group_id: "{groupID}") {{ id }} }}'
        writeToReport("Attempting mutation", mutation)
        data = {'query': mutation}

        try:
            r = requests.post(url=apiUrl, json=data, headers=headers)
            writeToReport("Response", r.json())
            #print(r.json())

            return True
        except Exception as e:
            writeToReport("Exception in API call/JSON", e)
            return None

    return True

def getOGNumStu(itemID):
    query = f'{{ items (ids: [{itemID}]) {{column_values {{id text}} }} }}'
    writeToReport("Attempting query", query)
    data = {'query': query}

    try:
        r = requests.post(url=apiUrl, json=data, headers=headers)
        jsonObj = json.loads(r.content)
        writeToReport("Response", r.json())
        OGNumStu = jsonObj["data"]["items"][0]["column_values"][NUM_STU_INDEX - 1]["text"]
        return OGNumStu
    except Exception as e:
        writeToReport("Exception in API call/JSON", e)
        return None


if __name__ == "__main__":
    beginTime = time()

    writeToReport("in updateMondayAPI", "")

    dotenv.load_dotenv(dotenv.find_dotenv())

    API_KEY = os.environ.get('MONDAY_API_KEY')
    apiUrl = "https://api.monday.com/v2"
    headers = {"Authorization": API_KEY}
    BOARD_ID = os.environ.get('BOARD_ID')
    NUM_STU_INDEX = 9
    DEL_MET_INDEX = 4

    COL_IDS = ["text8", "text67", "text83", "text", "text6", "status4", "status35", "status8", "__of_students",
               "__content_in_use",
               "files_total", "files_with_link", "files___in_use", "wysiwyg_content", "wysiwyg_in_use", "videos",
               "kaltura_vids", "youtube", "flash_content", "broken_links", "navigation_items", "status48",
               "overall_a11y_score",
               "files_ally_score", "wysiwyg_ally_score", "__of_pdf_files", "pdf_files_in_use", "pdf_scanned_not_ocr_d",
               "images", "images_wo_alt_text", "numbers"]

    GROUP_IDS = {100: "new_group659", 50: "new_group84060", 20: "new_group63769", 10: "new_group69712", 1: "new_group", 0: "new_group7956"}

    getIdsQuery = f'{{ boards(ids:{BOARD_ID}) {{ name items {{ name id }} }} }}'
    data = {'query': getIdsQuery}

    r = requests.post(url=apiUrl, json=data, headers=headers)
    jsonObj = json.loads(r.content)

    currBoard = {}
    for theRow in jsonObj["data"]["boards"][0]["items"]:
        currBoard[theRow["name"]] = theRow["id"]

    writeToReport("currentBoard", currBoard)

    filledFileObj = open("FilledInFile.csv")
    line = filledFileObj.readline()
    line = filledFileObj.readline()  # skip first line (header)

    numNew = 0
    numUpdated = 0

    while line:  # through filledInFile
        data = splitLine(line)
        writeToReport("line data", data)
        newNumStudents = data[NUM_STU_INDEX]
        if newNumStudents.isdigit():
            newNumStudents = int(newNumStudents)
        else:
            print(f"Error in {data}, the number of students is not an integer")
            writeToReport(f"Error, {data[NUM_STU_INDEX]} (numStudents) is not an integer", data)
            line = filledFileObj.readline()
            continue
        writeToReport("numStudents", data[NUM_STU_INDEX])

        if data[DEL_MET_INDEX] == "Study Abroad":
            data[DEL_MET_INDEX] = "Supervised"

        if data[0] in currBoard:
            writeToReport("Updating if needed", "")
            itemID = currBoard[data[0]]
            ogNumStu = getOGNumStu(itemID)
            if ogNumStu == None:
                line = filledFileObj.readline()
                continue
            if updateRow(currBoard[data[0]], data) == None:
                line = filledFileObj.readline()
                continue
            if makeSureInRightGroup(itemID, newNumStudents, ogNumStu) == None:
                line = filledFileObj.readline()
                continue
            numUpdated += 1
            print(f"{data[0]} matched and updated if needed")
        else:
            itemID = createNewItem(data)
            if itemID == None:
                line = filledFileObj.readline()
                continue
            writeToReport("Adding new row", data[0])
            numNew += 1
            print(f"{data[0]} added as new row")

        line = filledFileObj.readline()

    filledFileObj.close()

    print(f"\n{numUpdated} rows were matched and updated if necessary. {numNew} new rows were created.")
    print(f"\nDone in {time() - beginTime:.3f} seconds!")
    writeToReport(f"Done in {time() - beginTime:.3f} seconds!", "")
