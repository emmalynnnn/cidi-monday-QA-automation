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

import pandas as pd
import os
from time import time
import sys
import dotenv

def writeToReport(label, object):
    f = open("performanceReport3850265.txt", "a")
    f.write(f"{label}: {object}\n")
    f.close()

if __name__ == "__main__":
    print("Combining the course report with the Ally report...")
    writeToReport("combineSheets.py", "")

    dotenv.load_dotenv(dotenv.find_dotenv())
    COURSE_REPORT_FILENAME = os.environ.get('COURSE_REPORT_FILENAME')
    ALLY_FILENAME = "courses.csv"
    beginTime = time()

    meghanDataObj = pd.read_excel(COURSE_REPORT_FILENAME)
    meghanData = pd.DataFrame(meghanDataObj)

    allyDataObj = pd.read_csv(ALLY_FILENAME)
    allyData = pd.DataFrame(allyDataObj)
    allyDict = {}

    allyCourses = allyData["Course name"]
    for i in range(0, len(allyCourses)): #through Ally data
        courseInfo = [allyData["Overall score"][i], allyData["Files score"][i], allyData["WYSIWYG score"][i],
                      allyData["Scanned:1"][i], allyData["ImageDescription:2"][i]]
        allyDict[allyCourses[i]] = courseInfo

    shouldCompare = False

    try:
        oldFileObj = pd.read_csv("Old-FilledInFile.csv")
        oldFile = pd.DataFrame(oldFileObj)
        oldFileData = {}

        oldCourses = oldFile["Course"]
        for i in range(0, len(oldCourses)):  # through old data
            oldFileData[oldCourses[i]] = oldFile.iloc[i]
            #print(oldFileData[oldCourses[i]])
        shouldCompare = True
    except FileNotFoundError as e:
        print(e)
        print("Old-FilledInFile.csv not found")

    courseNames = meghanData["Course"]

    for i in range(0, len(courseNames)): #through Meghan's data
        try:
            allyInfo = allyDict[courseNames[i]]
            if shouldCompare:
                if allyInfo == oldFileData[courseNames[i]]:
                    meghanData.drop()
                    continue
            meghanData.loc[i, ["Overall Ally", "Files Ally", "WYSIWYG Ally", "PDF no OCR", "Images no Alt"]] = allyInfo
            # print(f"Successfully matched {courseNames[i]}")
            writeToReport("Successfully matched", courseNames[i])
        except KeyError:
            print(f"{courseNames[i]} could not be matched in the ally file.")
            writeToReport("Not found in ally file", courseNames[i])
        except Exception as e:
            print(f"Error in {courseNames[i]}: {e}")
            writeToReport(f"Error in {courseNames[i]}", e)

    meghanData.to_csv("FilledInFile.csv", index=False) #line causing RuntimeWarning :/

    print(f"\nDone in {time() - beginTime:.3f} seconds!", file=sys.stderr)
    writeToReport(f"Done in {time() - beginTime:.3f} seconds!", "")

    os.system('open FilledInFile.csv')