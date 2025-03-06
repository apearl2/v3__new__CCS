#Imports----------------------------------------------------------------------------------------------------------------
from flask import Flask, render_template, request

import requests
from bs4 import BeautifulSoup

try:
    from googlesearch import search
except ImportError:
    pass
    #print("No module named 'google' found")

from prettytable import PrettyTable
#import os
import time
import random

from selenium import webdriver
import re

#-----------------------------------------------------------------------------------------------------------------------
#Bugs 12/31 v
#If '...' appears below the confirm button on the results page, there was an error in processing the input string
#Intended Major appearing when not selected in final report

#2/4-> Updated Again for new design on Asus, post independent study presentation
#2/6-> Test Commit to pass through to PA

#Global Variables-------------------------------------------------------------------------------------------------------
newrankList = []
finalList = []
finalListCollegesOnlyP = []
finalListCollegesOnlyC = []
finalListCollegesOnlyU = []
reportfinalListP = []
reportfinalListC = []
reportfinalListU = []
customList = []
fullListU = []
fullListP = []
fullListC = []
tfullListC = []
specificsList = []
preattList = []

aImportance = 0
numPcalls = 0
numCcalls = 0
TICKER = 0

baseList = [25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
baseList2 = [25, 24.5, 24, 23.5, 23, 22.5, 22, 21.5, 21, 20.5, 20, 19.5, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15.5, 15, 14.5, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1]

stl = ''
atl = ""

aRateDict = {'University Of Pennsylvania': 6,
'Harvard University': 4,
'Northwestern University': 7,
'Johns Hopkins University': 8,
'Georgetown University': 12,
'Duke University': 6,
'Massachusetts Institute Of Technology': 4,
'Cornell University': 9,
'Stanford University': 4,
'New York University': 13,
'Dartmouth College': 6,
'Carnegie Mellon University': 14,
'Columbia University In The City Of New York': 4,
'University Of California Berkeley': 14,
'University Of Chicago': 6,
'Yale University': 5,
'Vanderbilt University': 7,
'University Of Southern California': 13,
'Boston College': 19,
'Pepperdine University': 53,
'University Of Michigan Ann Arbor': 20,
'The University Of Texas At Austin': 29,
'Georgia Institute Of Technology Main Campus': 16,
'University Of Virginia Main Campus': 21,
'Villanova University': 25,
'University Of Oklahoma Norman Campus': 85,
'Brown University': 6,
"Saint Mary'S College Of California": 70,
'University Of Notre Dame': 15,
'Washington University In St Louis': 13,
'George Mason University': 91,
'Arizona State University Tempe': 88,
'Thomas Aquinas College': 83,
'University Of North Carolina At Chapel Hill': 20,
'Drexel University': 83,
'University Of South Florida Main Campus': 49,
'University Of Iowa': 86,
'California Institute Of Technology': 4,
'Harvey Mudd College': 10,
'Southern Methodist University': 53,
'California State University Sacramento': 94,
'Butler University': 81,
'University Of California Los Angeles': 11,
'North Carolina State University': 47,
'Boston University': 19,
'Claremont Mckenna College': 11,
'University Of Georgia': 40,
'Suny At Binghamton': 44,
'Angelo State University': 70,
'University Of Wisconsin Green Bay': 91,
'Virginia Tech': 56,
'University Of Washington Seattle Campus': 53,
'College Of William And Mary': 37,
'The New School': 66,
'George Washington University': 50,
'Purdue University Main Campus': 69,
'Valencia College': 8,
"Auburn University": 70,
'Tulane University': 10,
'Princeton University': 4,
'Pennsylvania State University Main Campus': 55,
    "University Of California San Diego": 23.7,
    "University Of Illinois At Urbana Champaign": 60.1,
    "University Of Florida": 29.4,
    "Michigan State University": 76.0,
    "Indiana University Bloomington": 77.0,
    "University Of Arizona": 87.0,
    "Ohio State University Main Campus": 57.8,
    "Texas A&M University College Station": 63.0,
    "University Of Minnesota Twin Cities": 70.6,
    "University Of Maryland College Park": 52.0,
    "Rutgers University New Brunswick": 67.0,
    "University Of Pittsburgh": 64.0,
    "University Of Colorado Boulder": 80.0,
    "University Of Wisconsin Madison": 60.0,
    "University Of Massachusetts Amherst": 65.0,
    "University Of Utah": 83.1,
    "University Of Connecticut": 56.1,
    "University Of Alabama": 85.0,
    "University Of Kentucky": 95.0,
    "University Of Nevada Reno": 88.2,
    "University Of Missouri Columbia": 78.9,
    "University Of Oregon": 84.0,
    "Oregon State University": 82.0,
    "University Of South Carolina": 64.2,
    "The University Of Tennessee": 75.0,
    "University Of Mississippi": 88.0,
    "University Of Kansas": 91.0,
    "University Of Nebraska Lincoln": 81.0,
    "University Of Hawaii Manoa": 84.0,
    "University Of Idaho": 74.0,
    "Colorado State University": 90.5,
    "University Of Vermont": 67.3,
    "San Diego State University": 40.0,
    "California State University Long Beach": 47.0,
    "California Polytechnic State University San Luis Obispo": 30.0,
    "Arizona State University": 88.2,
    "University Of North Texas": 81.1,
    "University Of Houston": 63.0,
    "Temple University": 72.6,
    "University Of Central Florida": 44.4,
    "Florida State University": 33.0,
    "Clemson University": 49.2,
    "University Of Arkansas": 81.1,
    "University Of Rhode Island": 76.0,
    "University Of New Hampshire": 84.0,
    "University Of Maine": 96.7,
    "University Of Montana": 94.5,
    "University Of Alaska Fairbanks": 77.2,
    "University Of Wyoming": 94.5,
    "Tufts University": 11,
    "Bentley University": 61,
    "Rice University": 9,
    "Emory University": 13,
    "Kansas State University": 96,
    "Brigham Young University Provo": 59,
    "Williams College": 9,
    "Northeastern University": 18,
    "Lehigh University": 46,
    "Rollins College": 49,
    "Bryn Mawr College": 39,
    "Amherst College": 9,
    "Pomona College": 7,
    "Hampden Sydney College": 2,
    "University Of California Santa Barbara": 29,
    "Washington State University": 86,
    "University Of California Davis": 49,
    "University Of California Irvine": 29,
    "Massachusetts College Of Pharmacy And Health Sciences": 98,
    "University Of Miami": 28,
    "Texas A And M University College Station": 2,
    "Wake Forest University": 25,
    "Santa Clara University": 54,
    "Colgate University": 17,
    "Georgia Institute Of Technology": 16,
    "El Centro College": 2,
}


sizeDict = { 'University Of Pennsylvania': 9960, 'Harvard University': 5699, 'Northwestern University': 8095, 'Johns Hopkins University': 5766, 'Georgetown University': 6610, 'Duke University': 6572, 'Massachusetts Institute Of Technology': 4500, 'Cornell University': 14693, 'Stanford University': 5752, 'New York University': 25854, 'Dartmouth College': 4169, 'Carnegie Mellon University': 6341, 'Columbia University In The City Of New York': 8900, 'University Of California Berkeley': 29300, 'University Of Chicago': 7020, 'Yale University': 4696, 'Vanderbilt University': 6983, 'University Of Southern California': 18560, 'Boston College': 9571, 'Pepperdine University': 0, 'University Of Michigan Ann Arbor': 29851, 'The University Of Texas At Austin': 37404, 'Georgia Institute Of Technology Main Campus': 14485, 'University Of Virginia Main Campus': 16319, 'Villanova University': 6793, 'University Of Oklahoma Norman Campus': 18564, 'Brown University': 6605, "Saint Mary'S College Of California": 2308, 'University Of Notre Dame': 8833, 'Washington University In St Louis': 7077, 'George Mason University': 21603, 'Arizona State University Tempe': 57485, 'Thomas Aquinas College': 0, 'University Of North Carolina At Chapel Hill': 18505, 'Drexel University': 13156, 'University Of South Florida Main Campus': 29650, 'University Of Iowa': 20227, 'California Institute Of Technology': 1000, 'Harvey Mudd College': 915, 'Southern Methodist University': 6616, 'California State University Sacramento': 24068, 'Butler University': 4347, 'University Of California Los Angeles': 31068, 'North Carolina State University': 22929, 'Boston University': 16026, 'Claremont Mckenna College': 1240, 'University Of Georgia': 27888, 'Suny At Binghamton': 13889, 'Angelo State University': 0, 'University Of Wisconsin Green Bay': 4826, 'Virginia Tech': 29112, 'University Of Washington Seattle Campus': 29350, 'College Of William And Mary': 6131, 'The New School': 5658, 'George Washington University': 11387, 'Purdue University Main Campus': 33575, 'Valencia College': 16488, 'Auburn University': 22458, 'Tulane University': 7851, 'Princeton University': 4900, 'Pennsylvania State University Main Campus': 42000, "University Of California San Diego": 31900,"University Of Illinois At Urbana Champaign": 34779,"University Of Florida": 34931,"Michigan State University": 38500,"Indiana University Bloomington": 33084,"University Of Arizona": 36503,"Ohio State University Main Campus": 46984,
    "Texas A&M University College Station": 57204,
    "University Of Minnesota Twin Cities": 35895,
    "University Of Maryland College Park": 30875,
    "Rutgers University New Brunswick": 36039,
    "University Of Pittsburgh": 19200,
    "University Of Colorado Boulder": 31317,
    "University Of Wisconsin Madison": 31780,
    "University Of Massachusetts Amherst": 24209,
    "University Of Utah": 24835,
    "University Of Connecticut": 18567,
    "University Of Alabama": 32795,
    "University Of Kentucky": 20011,
    "University Of Nevada Reno": 18000,
    "University Of Missouri Columbia": 23417,
    "University Of Oregon": 18604,
    "Oregon State University": 24233,
    "University Of South Carolina": 26733,
    "The University Of Tennessee": 24254,
    "University Of Mississippi": 17000,
    "University Of Kansas": 19000,
    "University Of Nebraska Lincoln": 19552,
    "University Of Hawaii Manoa": 14000,
    "University Of Idaho": 7790,
    "Colorado State University": 25365,
    "University Of Vermont": 10585,
    "San Diego State University": 33845,
    "California State University Long Beach": 32477,
    "California Polytechnic State University San Luis Obispo": 22287,
    "Arizona State University": 63124,
    "University Of North Texas": 32486,
    "University Of Houston": 37394,
    "Temple University": 27374,
    "University Of Central Florida": 58913,
    "Florida State University": 33486,
    "Clemson University": 21653,
    "University Of Arkansas": 23218,
    "University Of Rhode Island": 14539,
    "University Of New Hampshire": 12202,
    "University Of Maine": 9365,
    "University Of Montana": 6000,
    "University Of Alaska Fairbanks": 8600,
    "University Of Wyoming": 9875,
    "Tufts University": 5938,
    "Bentley University": 4008,
    "Rice University": 4520,
    "Emory University": 6814,
    "Kansas State University": 14497,
    "Brigham Young University Provo": 30039,
    "Williams College": 1917,
    "Northeastern University": 15131,
    "Lehigh University": 5070,
    "Rollins College": 2456,
    "Bryn Mawr College": 1297,
    "Amherst College": 1745,
    "Pomona College": 1465,
    "Hampden Sydney College": 78000,
    "University Of California Santa Barbara": 22480,
    "Washington State University": 22315,
    "University Of California Davis": 30186,
    "University Of California Irvine": 28990,
    "Massachusetts College Of Pharmacy And Health Sciences": 3705,
    "University Of Miami": 10737,
    "Texas A And M University College Station": 70400,
    "Wake Forest University": 5367,
    "Santa Clara University": 5478,
    "Colgate University": 3023,
    "Georgia Institute Of Technology": 14485,
    "El Centro College": 79000,
}



#Regular Functions------------------------------------------------------------------------------------------------------
#Creates final list with all schools and all points (no averages yet, must be used after every CF or P Call)
def listA(order, funkName):
    #Global Variables
    global finalList
    global newrankList
    global baseList
    global finalListCollegesOnlyP
    global finalListCollegesOnlyC
    global finalListCollegesOnlyU
    global baseList2
    global aImportance
    global TICKER
    ###global finalConversionList

    #First, increments TICKER
    TICKER += 1

    #Reset baseList
    baseList = [25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    baseList2 = [25, 24.5, 24, 23.5, 23, 22.5, 22, 21.5, 21, 20.5, 20, 19.5, 19, 18.5, 18, 17.5, 17, 16.5, 16, 15.5, 15,
                 14.5, 14, 13.5, 13, 12.5, 12, 11.5, 11, 10.5, 10, 9.5, 9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5, 4, 3.5,
                 3, 2.5, 2, 1.5, 1]

    lennrl = len(newrankList)
    if lennrl > 25:
        lennrl = 25
    i = 0
    i2 = 0
    i3 = 0
    g = 0
    alreadyExists = False

    #If Princeton Review is called
    if funkName == "P":
        #Multiples baseList by User-Selected Importance Value
        while g < len(baseList):
            baseList[g] *= aImportance
            g += 1
        #Determines if it is first attribute or not
        if order == 1:
            #First attribute process
            while i < lennrl:
                finalList.append(newrankList[i])
                finalList.append(baseList[i])
                finalListCollegesOnlyP.append(newrankList[i])

                i += 1
        else:
            #Second Attribute Process
            while i2 < lennrl:
                #Repeats for every element in newrankList
                alreadyExists = False
                i3 = 0

                while i3 < len(finalList):
                    #If college already exists in final list
                    if newrankList[i2] == finalList[i3]:
                        finalList.insert((i3 + 1), baseList[i2])
                        alreadyExists = True
                        ##print(alreadyExists)
                        break

                    i3 += 1
                ##print(alreadyExists)
                if alreadyExists == False:
                    finalList.append(newrankList[i2])
                    finalList.append(baseList[i2])

                    # Adds requisite zeros
                    itp = 0
                    while itp < (TICKER - 1):
                        finalList.append(0)
                        itp += 1

                    ###finalconversionlist.append
                    finalListCollegesOnlyP.append(newrankList[i2])
                else:
                    pass

                i2 += 1
    #If CollegeFactual Function is Called
    elif funkName == "C":
        ##print(lennrl)
        #TODO

        # Multiples baseList by User-Selected Importance Value
        ##print(type(aImportance))
        while g < len(baseList):
            ##print(baseList[g])
            baseList[g] *= aImportance
            ##print(baseList[g])
            baseList2[g] *= aImportance
            g += 1
        ##print(baseList2)
        # Determines if it is first attribute or not
        if order == 1:
            # First attribute process
            while i < lennrl:
                finalList.append(newrankList[i])
                if lennrl < 50:
                    finalList.append(baseList[i])
                else:
                    finalList.append(baseList2[i])

                finalListCollegesOnlyC.append(newrankList[i])
                i += 1
        else:
            # Second Attribute Process
            while i2 < lennrl:
                # Repeats for every element in newrankList
                alreadyExists = False
                i3 = 0

                while i3 < len(finalList):
                    # If college already exists in final list
                    if newrankList[i2] == finalList[i3]:
                        if lennrl < 50:
                            finalList.insert((i3 + 1), baseList[i2])
                        else:
                            finalList.insert((i3 + 1), baseList2[i2])

                        alreadyExists = True
                        # #print(alreadyExists)
                        break

                    i3 += 1
                # #print(alreadyExists)
                if alreadyExists == False:
                    finalList.append(newrankList[i2])
                    if lennrl < 50:
                        finalList.append(baseList[i2])
                    else:
                        finalList.append(baseList2[i2])

                    # Adds requisite zeros
                    it = 0
                    while it < (TICKER - 1):
                        finalList.append(0)
                        it += 1

                    finalListCollegesOnlyC.append(newrankList[i2])
                else:
                    pass

                i2 += 1

    """If USNews function is called
    elif funkName == "U":
        ##print(lennrl)
        #TODO

        # Multiples baseList by User-Selected Importance Value
        ##print(type(aImportance))
        while g < len(baseList):
            ##print(baseList[g])
            baseList[g] *= aImportance
            ##print(baseList[g])
            baseList2[g] *= aImportance
            g += 1
        ##print(baseList2)
        # Determines if it is first attribute or not
        if order == 1:
            # First attribute process
            while i < lennrl:
                finalList.append(newrankList[i])
                if lennrl < 50:
                    finalList.append(baseList[i])
                else:
                    finalList.append(baseList2[i])

                finalListCollegesOnlyC.append(newrankList[i])
                i += 1
        else:
            # Second Attribute Process
            while i2 < lennrl:
                # Repeats for every element in newrankList
                alreadyExists = False
                i3 = 0

                while i3 < len(finalList):
                    # If college already exists in final list
                    if newrankList[i2] == finalList[i3]:
                        if lennrl < 50:
                            finalList.insert((i3 + 1), baseList[i2])
                        else:
                            finalList.insert((i3 + 1), baseList2[i2])

                        alreadyExists = True
                        # #print(alreadyExists)
                        break

                    i3 += 1
                # #print(alreadyExists)
                if alreadyExists == False:
                    finalList.append(newrankList[i2])
                    if lennrl < 50:
                        finalList.append(baseList[i2])
                    else:
                        finalList.append(baseList2[i2])

                    # Adds requisite zeros
                    it = 0
                    while it < (TICKER - 1):
                        finalList.append(0)
                        it += 1

                    finalListCollegesOnlyC.append(newrankList[i2])
                else:
                    pass

                i2 += 1
    #Now adds zeros to colleges not in most recent list------------------------
    if order > 1:
        previousZeros()

    ##print(finalList)"""

#Average-creating function, (must run twice for C and P)
def averageA(funkName2):
    global finalList
    global numPcalls
    global numCcalls
    global finalListCollegesOnlyP
    global finalListCollegesOnlyC
    global reportfinalListP
    global reportfinalListC
    global fullListP

    #To split string to isolate each college and their points
    i4 = 1
    i5 = 1
    totalPts = 0
    totalAvgPts = 0
    i6 = 0
    i7 = 1
    i8 = 0
    i9 = 1

    ##print(finalListCollegesOnly)
    if funkName2 == "P":
        tfinalList = finalList
        tfnLLength = len(tfinalList)
        while i9 < tfnLLength:
            if i8 > (len(finalListCollegesOnlyP) - 1):
                break
            else:
                if type(finalList[i4]) == str:
                    #Adds college to fullList first:
                    fullListP.append(finalListCollegesOnlyP[i8])

                    #Adds all the numbers together between first string and second string
                    totalPts = 0
                    i7 = 1
                    ##print(i4)

                    while i7 < i4:
                        totalPts += int(finalList[i7])

                        fullListP.append(int(finalList[i7]))

                        i7 += 1
                    ##print(totalPts)
                    totalAvgPts = totalPts / numPcalls
                    totalAvgPts = round(totalAvgPts, 2)

                    ##print(finalListCollegesOnlyP[i8])
                    reportfinalListP.append(finalListCollegesOnlyP[i8])
                    reportfinalListP.append(totalAvgPts)
                    ##print(reportfinalList)



                    del finalList[0]
                    while type(finalList[0]) != str:
                        del finalList[0]

                    ##print(finalList)


                    i8 += 1
                    i4 = 1
                else:
                    i4 += 1

                    pass

            i9 += 1
    elif funkName2 == "C":
        tfinalList = finalList
        tfnLLength = len(tfinalList)
        while i9 < tfnLLength:
            if type(finalList[i4]) == str:
                # Adds all the numbers together between first string and second string
                totalPts = 0
                i7 = 1
                # #print(i4)

                while i7 < i4:
                    totalPts += int(finalList[i7])
                    i7 += 1
                # #print(totalPts)
                totalAvgPts = totalPts / numCcalls
                totalAvgPts = round(totalAvgPts, 2)

                reportfinalListC.append(finalListCollegesOnlyC[i8])
                reportfinalListC.append(totalAvgPts)
                # #print(reportfinalList)

                del finalList[0]
                while type(finalList[0]) != str:
                    del finalList[0]

                # #print(finalList)

                i8 += 1
                i4 = 1
            else:
                i4 += 1

                pass

            i9 += 1

#Function to combines reportfinalListP and reportfinalListC
def joinA():
    global finalListCollegesOnlyC
    global finalListCollegesOnlyP
    global reportfinalListP
    global reportfinalListC

    # -------------------------------------------------------------------------------
    # First, Goes through all colleges in finalListCollegesOnlyC and divides them by 2 if they do not exist in P list
    i = 0
    while i < (len(reportfinalListC) - 1):
        now = reportfinalListC[i]

        try:
            trialI = finalListCollegesOnlyP.index(now)
        except ValueError:
            reportfinalListC[i + 1] /= 2

        i += 2

    #Loop through all colleges in final P list (e1)
    e1 = 0
    e2 = 0
    alreadyExists = False
    while e1 < len(reportfinalListP):
        alreadyExists = False
        ##print("\n" + reportfinalListP[e1])
        #Loops through all colleges in final CF list (e2)
        e2 = 0
        while e2 < len(reportfinalListC):
            ##print(reportfinalListC[e2])
            if reportfinalListP[e1] == reportfinalListC[e2]:
                #New point value for found college = existing value + value from P list    all over 2
                reportfinalListC[e2 + 1] = (reportfinalListC[e2 + 1] + reportfinalListP[e1 + 1])/2

                alreadyExists = True
                break

            e2 += 2

        if alreadyExists == False:
            reportfinalListC.append(reportfinalListP[e1])
            reportfinalListC.append((reportfinalListP[e1 + 1])/2)
        else:
            pass

        e1 += 2

#Function sorts reportfinalListC into order based on total points
def bestSort():
    global reportfinalListC
    global customList

    customList = []

    e3 = 1
    largest = reportfinalListC[1]

    #Main loop that finds top 10 of rfList
    i = 0
    rflC = (len(reportfinalListC) / 2)
    while i < rflC:
        #Resets
        largest = reportfinalListC[1]
        e3 = 1

        #Finds largest integer in list and then #prints the corresponding school value
        while e3 < len(reportfinalListC):
            if reportfinalListC[e3] > largest:
                largest  = reportfinalListC[e3]

            e3 += 2

        realI = reportfinalListC.index(largest)

        topSchool = reportfinalListC[realI - 1]

        #Appends to final custom list
        ntopSchool = topSchool.replace("-", " ")
        customList.append(ntopSchool)
        #customList.append(reportfinalListC[realI])
        customList = [x.title() for x in customList]

        #Deletes elements from rfList
        del reportfinalListC[realI]
        del reportfinalListC[realI - 1]

        i += 1


#College Factual Function
def collegeFactual(pChoice, pImportance):
    global newrankList
    newrankList = []

    # Global Importance value
    global aImportance
    aImportance = int(pImportance)

    # Searches Google to find URL of Attribute Ranking Site
    query2 = "College Factual 2024/25 Best Colleges for " + pChoice

    for j in search(query2, tld="co.in", num=1, stop=1, pause=2):
        goodURL2 = j

    ##print("Hello: " + goodURL2)
    # Gets HTML Data from URL
    r = requests.get(goodURL2)
    soup = BeautifulSoup(r.text, 'html.parser')
    j = soup.find_all('a', class_="rankListHeaderText")


    # Appends colleges to newrankList
    #TODO Emory University/Oxford College of Emory special case

    for element in j:
        if element.get_text() == 'oxford-college-of-emory-university':
            newrankList.append('emory-university')
        else:
            newrankList.append(element.get_text())

    #List Comprehension to convert all to lowercase
    newrankList = [x.lower() for x in newrankList]
    newrankList = [z.replace(' - ', ' ') for z in newrankList]
    newrankList = [y.replace(' ', '-') for y in newrankList]

    ##print("\n CollegeFactual call done")
    ##print(newrankList)

# Princeton Review Function
def princetonReview(pChoice, pImportance):
    global conversionList
    global newrankList
    newrankList = []
    conversionList = []
    # Global Importance value
    global aImportance
    aImportance = int(pImportance)

    #Bypasses Google Search Process to Save Time
    VmanualV = True

    attributesList = ["Their Students Love these colleges", "Students love their school teams",
                      "Campus Beauty", "Cities", "Lots of race_class interaction", "Dorms", "Food",
                      "Public school value top 50", "Private school value top 50", "Internships Public",
                      "Internships Private"]
    #Pre-Made Lists--------------------------------------------------
    #----------------------Updated 11/27/2024----------------------------------------
    tpChoice = pChoice.replace(" ", "")

    if VmanualV:
        if tpChoice == 'TheirStudentsLovethesecolleges':
            newrankList = [' UniversityofDenverDenver,', 'EmoryUniversity', 'LehighUniversity', 'FloridaState',
                           'VirginiaTech', 'WashingtonState', ' Auburn', ' WashingtonUniversityin', 'KansasState',
                           'RiceUniversity', 'TulaneUniversity', 'Hampden-Sydney', 'AngeloState', 'FranklinW.',
                           'ClaremontMc', 'UniversityofWisconsin-', 'CollegeoftheAtlantic', 'TheUniversityof',
                           'ThomasAquinas', 'Hamilton', 'Amherst', 'UniversityofCincinnatiCincinnati,',
                           ' VanderbiltUniversity']
        elif tpChoice == 'Studentslovetheirschoolteams':
            newrankList = [' GonzagaUniversity', 'ArizonaState', 'Syracuse', ' Clemson', 'KansasState', 'BrighamYoung',
                           'FloridaState', 'TheOhio', 'UniversityofWisconsin-', 'MichiganState', 'UniversityofTex',
                           ' Auburn', 'ButlerUniversity', 'Wabash', 'UniversityofCincinnatiCincinnati,',
                           'UniversityofNotre', 'Hampden-Sydney', 'UniversityofDaytonDayton,', 'UniversityofTennessee-',
                           'UnitedStates', 'XavierUniversity(', ' UniversityofNebraska—', 'IowaState',
                           ' BryantUniversity']
        elif tpChoice == 'CampusBeauty':
            newrankList = ['UniversityofSan', 'BrynMawr', 'Lewis&', ' FloridaSouthern', 'MountHolyoke',
                           ' WashingtonUniversityin', 'RiceUniversity', ' VanderbiltUniversity', ' SalveRegina',
                           'ThomasAquinas', ' ReedCollege', 'LehighUniversity', ' RhodesCollege', 'RollinsCollege',
                           ' HighPoint', 'TexasChristian', 'UniversityofPuget', 'UniversityofCalifornia—',
                           'PepperdineUniversity', ' LoyolaMarymount', ' UniversityofDenverDenver,']
        elif tpChoice == 'Cities':
            newrankList = ['AmericanUniversity', ' SalveRegina', 'SimmonsUniversity', 'RollinsCollege',
                           'EmersonCollege', 'ColumbiaUniversity', 'CityUniversityof', 'EugeneLang',
                           ' SuffolkUniversity', ' NortheasternUniversity', ' GeorgeWashington', 'TulaneUniversity',
                           ' UniversityofDenverDenver,', 'KansasState', ' VanderbiltUniversity', 'EmoryUniversity',
                           'TheCooper', 'UniversityofVermont', 'UniversityofTex', 'UniversityofSan', 'LoyolaUniversity',
                           'UniversityofWisconsin-', 'NewYork']
        elif tpChoice == 'Lotsofrace_classinteraction':
            newrankList = ['RiceUniversity', 'LoyolaUniversity', ' DruryUniversity', 'LehighUniversity',
                           'ThomasAquinas', 'JuniataCollege', 'EmoryUniversity', 'WashingtonState', 'UnitedStates',
                           'AngeloState', ' ReedCollege', "St.John's", 'Hampden-Sydney', 'DenisonUniversity',
                           'UnitedStates', ' WashingtonUniversityin', 'ClaremontMc', 'CaliforniaState', 'Wellesley',
                           ' DrewUniversity', 'UniversityofCincinnatiCincinnati,', 'AgnesScott', 'St.Bonaventure',
                           'UnitedStates']
        elif tpChoice == 'Dorms':
            newrankList = ['Bowdoin', ' WashingtonUniversityin', 'EmoryUniversity', 'BrynMawr', 'Scripps', ' HighPoint',
                           'Pitzer', 'KansasState', 'TexasChristian', 'FranklinW.', ' ReedCollege', 'MountHolyoke',
                           'WashingtonState', 'UniversityofKentucky', 'WheatonCollege(', 'Amherst', 'Skidmore',
                           ' ChristopherNewport', 'RiceUniversity', 'Elon', 'UniversityofDaytonDayton,', 'BrighamYoung']
        elif tpChoice == 'Food':
            newrankList = ['UniversityofMassachusetts-', ' WashingtonUniversityin', 'Bowdoin', 'CornellUniversity',
                           'BatesCollege', 'Pitzer', 'JamesMadison', 'CollegeoftheAtlantic', 'VirginiaTech',
                           'RollinsCollege', ' MuhlenbergCollege', 'UniversityofDaytonDayton,', 'KansasState', 'Elon',
                           ' St.Olaf', ' Gettysburg', ' HighPoint', 'WheatonCollege(', 'Scripps', 'WashingtonState',
                           'ColumbiaUniversity', ' ReedCollege', 'BrynMawr']
        elif tpChoice == 'Publicschoolvaluetop50':
            newrankList = ['GeorgiaInstituteof', 'UniversityofCalifornia—', 'UniversityofVirginia', 'TheUniversityof',
                           'UniversityofCalifornia—', 'UniversityofCalifornia—', 'UniversityofMichigan—',
                           'UniversityofCalifornia—', 'NorthCarolina', 'UniversityofTex', 'UniversityofWashington',
                           'UniversityofCalifornia—', 'UniversityofGeorgia', 'UniversityofIllinois',
                           ' StateUniversityof', 'FloridaState', 'MissouriUniversityof', 'William&',
                           'PurdueUniversity—', 'NewCollegeof', 'TexasA&', 'UniversityofWisconsin-', 'NewJersey',
                           'CityUniversityof']
        elif tpChoice == 'Privateschoolvaluetop50':
            newrankList = ['MassachusettsInstituteof', 'Princeton', 'Stanford', 'HarveyMudd', 'CaliforniaInstituteof',
                           'DartmouthCollege', 'Harvard', 'Williams', 'YaleUniversity', 'TheCooper', 'RiceUniversity',
                           'JohnsHopkins', 'CarnegieMellon', 'Universityof', 'BrownUniversity', 'Duke', 'FranklinW.',
                           'ColumbiaUniversity', 'ColgateUniversity', 'Pomona', 'CornellUniversity', 'ClaremontMc',
                           'TheUniversityof', 'Amherst']
        elif tpChoice == 'InternshipsPublic':
            newrankList = ['UniversityofMichigan—', 'MichiganTechnological', 'PennState', 'GeorgiaInstituteof', ' The',
                           'PurdueUniversity—', 'MissouriUniversityof', 'William&', 'WashingtonState',
                           'UniversityofWashington', 'UniversityofTex', 'MiamiUniversity', ' Clemson', 'FloridaState',
                           'NorthCarolina', 'UniversityofGeorgia', 'VirginiaTech', 'TheUniversityof', 'OregonState']
        else:
            newrankList = [' NortheasternUniversity', 'Wabash', 'Hampden-Sydney', 'HarveyMudd', ' St.Lawrence',
                           'Stanford', 'FranklinW.', 'Rose-Hulman', 'BrighamYoung', 'WakeForest', 'Marquette',
                           'AustinCollege', ' HobartandWilliam', ' CollegeofWoosterWooster,', ' RhodesCollege',
                           'DartmouthCollege', 'WorcesterPolytechnic', 'Universityof']

    else:
        # Searches Google to find URL of Attribute Ranking Site

        # to search
        query = "The Princeton Review Best College " + pChoice

        for j in search(query, tld="co.in", num=1, stop=1, pause=2):
            goodURL = j

        # #print("Hello: " + goodURL)
        # Gets HTML Data from URL
        r = requests.get(goodURL)
        soup = BeautifulSoup(r.text, 'html.parser')
        j = soup.find('main', class_="col-lg-8 col-md-12 col-sm-12").get_text(strip=True)
        # #print(j)

        rank1 = j.find("#1")
        # #print(rank1)
        # ------------------------------------------------------------------------------------------------------------#

        # Number for iterations v (testing purposes)
        if pChoice == "Internships Public" or pChoice == "Internships Private":
            testTimes = 20
        elif pChoice == "Public School value top 50" or pChoice == "Private School value top 50":
            testTimes = 25
        else:
            testTimes = 25
        # Loop to put top 25 in ordered list
        loop = 1
        rankList = []

        while loop < testTimes:
            # #print(loop)
            loopS = str(loop)
            finder = '#' + loopS
            # #print(finder)

            rank = j.find(finder)
            # #print(rank)

            strnew = j.split(finder)
            # #print(strnew)

            firstU = strnew[1]
            finalStr = ""
            i = 0
            x = 0

            while x < 4:
                while firstU[i] != ' ':
                    finalStr = finalStr + firstU[i]
                    i += 1

                # #print(finalStr)
                i += 1
                x += 1

            # --------Editing the Final String
            upperList = []
            f = finalStr.find("Featured")
            if f == 0:
                finalStr = finalStr.replace("Featured", " ")
            for c in finalStr:
                if c.isupper() == True:
                    upperList.append(c)
            # #print(upperList)
            # #print(finalStr)

            UnivExists = False
            CollegeOfExists = False

            if finalStr[0] == "U" and finalStr[10] == "o" or finalStr[11] == "o":
                UnivExists = True
            if finalStr[0] == "C" and finalStr[7] == "o":
                CollegeOfExists = True

            # #print(finalStr)
            if UnivExists or CollegeOfExists:
                # Specific School Exception
                if finalStr == "UniversityofPuget":
                    endCap = upperList[3]
                if finalStr == "UniversityofTexasat" or finalStr == "UniversityofIllinoisat":
                    endCap = "a"
                else:
                    if upperList[1] == upperList[2]:
                        endCap = upperList[3]
                    else:
                        endCap = upperList[2]

                endCap_find = finalStr.find(endCap)
                newFinalStr = finalStr.split(finalStr[endCap_find])

                rankList.append(newFinalStr[0])
            else:
                if len(upperList) > 2:
                    if upperList[0] == upperList[2]:
                        endCap = upperList[1]
                    else:
                        endCap = upperList[2]
                    endCap_find = finalStr.find(endCap)
                    newFinalStr = finalStr.split(finalStr[endCap_find])
                    rankList.append(newFinalStr[0])
                else:
                    rankList.append("____ERROR____")

            # #print(rankList)
            i = 0
            loop += 1

        # For loop to put error in missing colleges
        for num in range(testTimes - 1):
            if rankList[num] == ' ' or rankList[num] == '':
                rankList[num] = "____ERROR____"

        # #printout of final ranking list (with errors included)
        # #print(rankList)

        # Removes ____Error____'s from List
        i1 = 0
        while i1 < (testTimes - 1):
            # #print(i1)
            if rankList[i1] != "____ERROR____":
                newrankList.append(rankList[i1])
            i1 += 1

        # #print("\nFinal Ranking: ")
        # #print(newrankList)

    # #print("\nPrincetonReview call done")
    #print("nrl \n\n")
    #print(newrankList)

#College Vine Function------------------------------------------------------------------------------------------------------
def cVine(pChoice, pImportance):
    global newrankList
    newrankList = []
    global aImportance
    aImportance = int(pImportance)

    query2 = "CollegeVine 2024/25 Best Colleges for " + pChoice

    for j in search(query2, tld="co.in", num=1, stop=1, pause=2):
        goodURL2 = j

        #print("Hello: " + goodURL2)
        # Gets HTML Data from URL
        r = requests.get(goodURL2)
        soup = BeautifulSoup(r.text, 'html.parser')
        j = soup.find_all('div', class_="d-flex align-items-start justify-content-between")

        for element in j:
            #Determines how to deal with extra hyphen
            special = False

            newJ = element.get_text(strip=True)

            #Formats cV string to CF format
            tJ = newJ.replace(",", "")
            tgj = tJ.replace(".", "")
            ttJ = tgj.lower()

            if ttJ.find("|") != -1:
                oneJ = ttJ.split("|")
                eJ = oneJ[0]
                special = True
            else:
                eJ = ttJ

            maxnum = 0
            count = eJ.count(" ")

            ##print(count)
            ##print(special)

            if special == True:
                maxnum = count - 1
                fJ = eJ.replace(" ", "-", maxnum)
                ultiJ = fJ.replace(" ", "")
            else:
                maxnum = count
                ultiJ = eJ.replace(" ", "-", maxnum)

            ##print(ultiJ)

            #Special formatting cases
            if ultiJ == "columbia-university":
                ultiJ = ultiJ + "-in-the-city-of-new-york"

            if ultiJ == "university-of-michigan":
                ultiJ = ultiJ + "-ann-arbor"

            if ultiJ == "university-of-virginia":
                ultiJ = ultiJ + "-main-campus"

            if ultiJ == "university-of-texas-at-austin":
                ultiJ = "the-university-of-texas-at-austin"


            newrankList.append(ultiJ)

    #print("nrl \n\n")
    #print(newrankList)

#USNews Function------------------------------------------------------------------------------------------------------------
def usNews(pChoice, pImportance):
    global newrankList
    global aImportance
    aImportance = int(pImportance)

    if pChoice == "Campus":
        newrankList = [
    "Aurora University",
    "Baylor University",
    "Berry College",
    "Denison University",
    "Duke University",
    "Flagler College",
    "Georgia Institute of Technology",
    "Harvard University",
    "Indiana University—Bloomington",
    "Kenyon College",
    "Mercer University",
    "Pepperdine University",
    "Princeton University",
    "Salve Regina University",
    "San Diego State University",
    "Spelman College",
    "Stanford University",
    "Swarthmore College",
    "Texas Christian University",
    "University of Colorado Boulder",
    "University of Notre Dame",
    "University of Vermont",
    "University of Virginia",
    "University of Washington",
    "Villanova University"]

    elif pChoice == "Diversity":
        newrankList = [
    "Andrews University",
    "Johns Hopkins University",
    "Stanford University",
    "University of San Francisco",
    "University of Hawaii at Hilo",
    "University of Nevada--Las Vegas",
    "New York University",
    "Seattle University",
    "University of Hawaii at Manoa",
    "University of Maryland Baltimore County",
    "University of Massachusetts--Boston",
    "George Mason University",
    "Harvard University",
    "Rice University",
    "Rutgers University--Newark",
    "University of California--Los Angeles",
    "University of Chicago",
    "University of Southern California",
    "Yale University",
    "California Institute of Technology",
    "Massachusetts Institute of Technology",
    "New Jersey Institute of Technology",
    "Rutgers University--Camden",
    "San Francisco State University",
    "Seattle Pacific University",
    "University of California, Santa Cruz",
    "Virginia Commonwealth University",
    "Brown University",
    "Cornell University",
    "Emory University",
    "Georgia State University",
    "Northwestern University",
    "Nova Southeastern University",
    "Texas Woman's University",
    "University at Albany--SUNY",
    "University of California, Davis",
    "University of Houston",
    "University of Illinois--Chicago",
    "University of Pennsylvania",
    "The University of Texas--Arlington",
    "Azusa Pacific University",
    "CUNY--City College",
    "Duke University",
    "Illinois Institute of Technology",
    "Loyola Marymount University",
    "Marymount University",
    "Princeton University",
    "Roosevelt University",
    "Rutgers University--New Brunswick",
    "Santa Clara University",
    "University of California, San Diego",
    "University of California, Santa Barbara",
    "University of North Texas",
    "The University of Texas--Austin",
    "University of the Pacific",
    "Boston University",
    "Carnegie Mellon University",
    "Case Western Reserve University",
    "Kean University",
    "Lamar University"]

    elif pChoice == "Food":
        newrankList = ["Bowdoin College", "Cornell University", "Duke University", "Hendrix College", "James Madison University", "University of Massachusetts--Amherst", "University of Oregon", "University of San Diego", "University of South Carolina", "Virginia Tech"]

    elif pChoice == "Internships":
        newrankList = [
    "Northeastern University",
    "Drexel University",
    "Berea College",
    "Georgia Institute of Technology",
    "University of Cincinnati",
    "Rochester Institute of Technology",
    "Massachusetts Institute of Technology",
    "Purdue University--Main Campus",
    "Carnegie Mellon University",
    "Elon University",
    "Clemson University",
    "Duke University",
    "Cornell University",
    "Agnes Scott College",
    "Arizona State University",
    "Embry-Riddle Aeronautical University -- Daytona Beach",
    "Harvard University",
    "Worcester Polytechnic Institute",
    "American University",
    "Endicott College",
    "George Mason University",
    "Kettering University"]
    elif pChoice == "Study Abroad":
        newrankList = [
    "New York University",
    "Elon University",
    "Middlebury College",
    "American University",
    "Georgetown University",
    "Agnes Scott College",
    "Goucher College",
    "Michigan State University",
    "Syracuse University",
    "Kalamazoo College",
    "Duke University",
    "Pepperdine University",
    "Dartmouth College",
    "Macalester College",
    "Northeastern University",
    "Arcadia University",
    "St. Olaf College",
    "Abilene Christian University",
    "Boston College",
    "Boston University",
    "Indiana University--Bloomington",
    "Centre College",
    "Texas A&M University",
    "Butler University",
    "Carleton College",
    "The University of Texas--Austin",
    "Dickinson College",
    "George Washington University",
    "Georgia State University",
    "University of Michigan--Ann Arbor"]

    else:
        # Set the path to the Chromedriver
        DRIVER_PATH = '/path/to/chromedriver'

        # Initialize the Chrome driver
        driver = webdriver.Chrome()

        query2 = "USNews 2024/25 Best Colleges for major in " + pChoice

        for k in search(query2, tld="co.in", num=1, stop=1, pause=2):
            goodURL2 = k

        # print("Hello: " + goodURL2)

        # Navigate to the URL
        selURL = goodURL2

        """     Major test URLS
                English: https://www.usnews.com/best-graduate-schools/top-humanities-schools/english-rankings'
                IE: 'https://www.usnews.com/best-graduate-schools/top-engineering-schools/industrial-engineering-rankings'
                Biology: 'https://www.usnews.com/best-graduate-schools/top-science-schools/biological-sciences-rankings'
                Psychology: 'https://www.usnews.com/best-graduate-schools/top-humanities-schools/psychology-rankings'

                MechE: 'https://www.usnews.com/best-colleges/rankings/engineering-doctorate-mechanical?_sort=rank&_sortDirection=asc'
                Hospitality: 'https://www.usnews.com/best-colleges/hospitality-management-major-5209?_sort=rank&_sortDirection=asc'
                Econ: 'https://www.usnews.com/best-colleges/rankings/economics-overall?_sort=rank&_sortDirection=asc'
            """
        driver.get(selURL)

        # TODO Might have to alter for different computers--------------------------------------------------
        time.sleep(5)

        # Output full page HTML
        # print(driver.page_source)
        ut = driver.page_source
        t = str(ut)
        # print(t)

        # Determmines if page is table or traditional rank...determines which method to use
        # Each school's score reflects its average rating on a scale from 1 (marginal) to 5 (outstanding)
        firstmatch = re.search("Span-sc-19wk4id-0 gqvMPj", t)
        # print("firstmatch:")
        # print(firstmatch)
        if firstmatch != None:

            # Method 1 (table style 0-5.0 rankings)---------------------------------------------------------------------------------------------
            x = firstmatch
            print(x)

            nx = str(x)
            # find first index full number
            firstin = ""
            nxi = 24
            while nxi < 30:
                firstin = firstin + nx[nxi]
                nxi += 1
            firstinint = int(firstin)
            print(firstinint)
            endii = firstinint + 40000

            # New string starting at first school to last loaded school (still ~150,000 characters)
            newt = t[firstinint:endii]
            print(newt)

            # Now parse string using beautifulsoup
            newrankList = []

            soup = BeautifulSoup(newt, 'html.parser')
            j = soup.find_all('div', class_="Box-w0dun1-0 bihhZB")
            print(j)
            for element in j:
                tempej = element['name']

                # print(tempej)
                newrankList.append(tempej)

            # Special formatting cases
            for elemt in newrankList:
                # TODO not picking up 3/2
                if elemt == 'columbia-university':
                    elemt = elemt + '-in-the-city-of-new-york'

                if elemt == "university-of-michigan":
                    elemt = elemt + "-ann-arbor"

                if elemt == "university-of-virginia":
                    elemt = elemt + "-main-campus"

                if elemt == "university-of-texas-at-austin":
                    elemt = "the-university-of-texas-at-austin"

            print(newrankList)


        else:
            # Method 2 (traditional rank boxes)------------------------------------------------
            # y = re.search("List__ListItem-rhf5no-1 jYdEtR", t)
            newrankList = []

            soup = BeautifulSoup(t, 'html.parser')
            j = soup.find_all('li', class_="List__ListItem-rhf5no-1 jYdEtR")
            # print(j)
            for element in j:
                tempej2t = element.get_text()

                # print(tempej2t)
                char = "("
                if char in tempej2t:
                    charind = tempej2t.index(char)
                    # print(charind)
                    tempej2 = tempej2t[:charind - 1]
                else:
                    tempej2 = tempej2t

                newrankList.append(tempej2)

            # print(newrankList)

    # It's a good practice to close the browser when done
    try:
        driver.quit()
    except:
        pass

    # List Comprehension to convert all to lowercase
    newrankList = [x.lower() for x in newrankList]
    newrankList = [w.replace(',', '') for w in newrankList]
    newrankList = [z.replace('--', ' ') for z in newrankList]
    newrankList = [y.replace(' ', '-') for y in newrankList]

    print(newrankList)





#P to CF variable conversions list:--------------------------------------------------------------------------
def conversions():
    global finalListCollegesOnlyP

    finalPlist = [' UniversityofDenverDenver,', 'EmoryUniversity', 'LehighUniversity', 'FloridaState', 'VirginiaTech', 'WashingtonState', ' Auburn', ' WashingtonUniversityin', 'KansasState', 'RiceUniversity', 'TulaneUniversity', 'Hampden-Sydney', 'AngeloState', 'FranklinW.', 'ClaremontMc', 'UniversityofWisconsin-', 'CollegeoftheAtlantic', 'TheUniversityof', 'ThomasAquinas', 'Hamilton', 'Amherst', 'UniversityofCincinnatiCincinnati,', ' VanderbiltUniversity', ' GonzagaUniversity', 'ArizonaState', 'Syracuse', ' Clemson', 'BrighamYoung', 'TheOhio', 'MichiganState', 'UniversityofTex', 'ButlerUniversity', 'Wabash', 'UniversityofNotre', 'UniversityofDaytonDayton,', 'UniversityofTennessee-', 'UnitedStates', 'XavierUniversity(', ' UniversityofNebraska—', 'IowaState', ' BryantUniversity', 'UniversityofSan', 'BrynMawr', 'Lewis&', ' FloridaSouthern', 'MountHolyoke', ' SalveRegina', ' ReedCollege', ' RhodesCollege', 'RollinsCollege', ' HighPoint', 'TexasChristian', 'UniversityofPuget', 'UniversityofCalifornia—', 'PepperdineUniversity', ' LoyolaMarymount', 'AmericanUniversity', 'SimmonsUniversity', 'EmersonCollege', 'ColumbiaUniversity', 'CityUniversityof', 'EugeneLang', ' SuffolkUniversity', ' NortheasternUniversity', ' GeorgeWashington', 'TheCooper', 'UniversityofVermont', 'LoyolaUniversity', 'NewYork', ' DruryUniversity', 'JuniataCollege', "St.John's", 'DenisonUniversity', 'CaliforniaState', 'Wellesley', ' DrewUniversity', 'AgnesScott', 'St.Bonaventure', 'Bowdoin', 'Scripps', 'Pitzer', 'UniversityofKentucky', 'WheatonCollege(', 'Skidmore', ' ChristopherNewport', 'Elon', 'UniversityofMassachusetts-', 'CornellUniversity', 'BatesCollege', 'JamesMadison', ' MuhlenbergCollege', ' St.Olaf', ' Gettysburg', 'GeorgiaInstituteof', 'UniversityofVirginia', 'UniversityofMichigan—', 'NorthCarolina', 'UniversityofWashington', 'UniversityofGeorgia', 'UniversityofIllinois', ' StateUniversityof', 'MissouriUniversityof', 'William&', 'PurdueUniversity—', 'NewCollegeof', 'TexasA&', 'NewJersey', 'MassachusettsInstituteof', 'Princeton', 'Stanford', 'HarveyMudd', 'CaliforniaInstituteof', 'DartmouthCollege', 'Harvard', 'Williams', 'YaleUniversity', 'JohnsHopkins', 'CarnegieMellon', 'Universityof', 'BrownUniversity', 'Duke', 'ColgateUniversity', 'Pomona', 'MichiganTechnological', 'PennState', ' The', 'MiamiUniversity', 'OregonState', ' St.Lawrence', 'Rose-Hulman', 'WakeForest', 'Marquette', 'AustinCollege', ' HobartandWilliam', ' CollegeofWoosterWooster,', 'WorcesterPolytechnic']

    completePconversionList = ['university-of-denver', 'emory-university', 'lehigh-university', 'florida-state-university', 'virginia-tech', 'washington-state-university', 'auburn-university', 'washington-university-in-st-louis', 'kansas-state-university', 'rice-university', 'tulane-university-of-louisiana', 'hampden-sydney-college', 'angelo-state-university', 'franklin-university', 'claremont-mckenna-college', 'university-of-wisconsin-madison', 'college-of-the-atlantic', 'university-of-chicago', 'thomas-aquinas-college', 'hamilton-college', 'amherst-college', 'university-of-cincinnati-main-campus', 'vanderbilt-university', 'gonzaga-university', 'arizona-state-university', 'syracuse-university', 'clemson-university', 'brigham-young-university-provo', 'ohio-state-university-main-campus', 'michigan-state-university', 'the-university-of-texas-at-austin', 'butler-university', 'wabash-college', 'university-of-notre-dame', 'university-of-dayton', 'the-university-of-tennessee', 'united-states-naval-academy', 'xavier-university', 'university-of-nebraska-lincoln', 'iowa-state-university', 'bryant-university', 'university-of-san-francisco', 'bryn-mawr-college', 'lewis-and-clark-college', 'florida-southern-college', 'mount-holyoke-college', 'salve-regina-university', 'reed-college', 'rhodes-college', 'rollins-college', 'high-point-university', 'texas-christian-university', 'university-of-puget-sound', 'university-of-california-berkeley', 'pepperdine-university', 'loyola-marymount-university', 'american-university', 'simmons-college', 'emerson-college', 'columbia-university-in-the-city-of-new-york', 'city-university-of-seattle', 'suny-at-binghamton', 'suffolk-university', 'northeastern-university', 'george-washington-university', 'cooper-union-for-the-advancement-of-science-and-art', 'university-of-vermont', 'loyola-university-chicago', 'new-york-university', 'drury-university', 'juniata-college', 'st-johns-university-new-york', 'denison-university', 'california-state-university-los-angeles', 'wellesley-college', 'drew-university', 'agnes-scott-college', 'saint-bonaventure-university', 'bowdoin-college', 'scripps-college', 'pitzer-college', 'university-of-kentucky', 'wheaton-college-illinois', 'skidmore-college', 'christopher-newport-university', 'elon-university', 'university-of-massachusetts-amherst', 'cornell-university', 'bates-college', 'james-madison-university', 'muhlenberg-college', 'st-olaf-college', 'gettysburg-college', 'georgia-institute-of-technology-main-campus', 'university-of-virginia-main-campus', 'university-of-michigan-ann-arbor', 'university-of-north-carolina-at-chapel-hill', 'university-of-washington-seattle-campus', 'university-of-georgia', 'university-of-illinois-at-urbana-champaign', 'suny-at-binghamton', 'university-of-missouri-columbia', 'college-of-william-and-mary', 'purdue-university-main-campus', 'the-new-school', 'texas-a-and-m-university-college-station', 'the-college-of-new-jersey', 'massachusetts-institute-of-technology', 'princeton-university', 'stanford-university', 'harvey-mudd-college', 'california-institute-of-technology', 'dartmouth-college', 'harvard-university', 'williams-college', 'yale-university', 'johns-hopkins-university', 'carnegie-mellon-university', 'university-of-chicago', 'brown-university', 'duke-university', 'colgate-university', 'pomona-college', 'michigan-technological-university', 'pennsylvania-state-university-main-campus', 'suny-at-binghamton', 'miami-university-oxford', 'oregon-state-university', 'st-lawrence-university', 'rose-hulman-institute-of-technology', 'wake-forest-university', 'marquette-university', 'austin-college', 'hobart-william-smith-colleges', 'the-college-of-wooster', 'worcester-polytechnic-institute']

    #Loops through all of finalListCollegesOnlyP
    i = 0
    flcoplen = len(finalListCollegesOnlyP)
    while i < flcoplen:
        try:
            oneIndex = finalPlist.index(finalListCollegesOnlyP[i])

            finalListCollegesOnlyP.insert(i, completePconversionList[oneIndex])
            del finalListCollegesOnlyP[i + 1]
        except ValueError:
            pass

        i += 1


#Adds Zeros Function for Final College-by-College Report-------------------------------------------------------------------------------------
def previousZeros():
    global TICKER
    global finalList

    #Iterates through finalList
    #print("TICKER = " + str(TICKER))
    i = 0
    #ii = 0
    tempList = []
    lenfl = len(finalList)
    while i < lenfl:
        #Then adds number of integers to list, and adds number of zeros based on number of values in list
        value = str(finalList[i])
        #print(value)
        if len(value) < 6 and value != 'Elon' and value != 'Duke' and value != ' The' and value != '' and value != ' ':
            finalV = float(value)
            tempList.append(finalV)
            i += 1
        else:
            #print("tempList: ")
            #print(tempList)

            if len(tempList) == 0:
                i += 1
                tempList = []
                pass
            else:
                #Say ticker is 2
                if len(tempList) < TICKER:
                    finalList.insert(i - 1, 0)

                    #Reset tempList
                    tempList = []

                    i += 2
                else:
                    #print("TICKER Error")
                    tempList = []
                    i += 1


# Makes final attribute-by-attribute specific report list
def rList():
    global fullListP
    global fullListC
    global specificsList

    # First, iterate through finalListC
    ic = 0
    while ic < len(fullListC):
        tschoolC = fullListC[ic]
        specificsList.append(tschoolC)

        #print(tschoolC)

        # If school is in both full lists
        if tschoolC in fullListP:
            pI = fullListP.index(tschoolC)

            # Now appends required a point info-----------

            # Iterates through fullListP to get point values
            max = pI + 12
            tpI = pI + 1
            while tpI < max:
                try:
                    specificsList.append(fullListP[tpI])
                except:
                    break

                tpI += 1

        else:

            iss = 0

            while iss < 12:
                specificsList.append(0)
                iss += 1

        # Appends fullListC values
        cI = fullListC.index(tschoolC)

        maxC = cI + 5
        tcI = cI + 1
        while tcI < maxC:
            try:
                specificsList.append(fullListC[tcI])
            except:
                break

            tcI += 1

        ic += 5

    #Then, append schools that only exist in P
    ip = 0
    while ip < len(fullListP):
        tschoolP = fullListP[ip]

        if tschoolP in specificsList:
            pass
        else:
            specificsList.append(tschoolP)

            pI2 = fullListP.index(tschoolP)
            # Iterates through fullListP to get point values
            max2 = pI2 + 12
            tpI2 = pI2 + 1
            while tpI2 < max2:
                try:
                    specificsList.append(fullListP[tpI2])
                except:
                    break

                tpI2 += 1

            nin = 0
            while nin < 4:
                specificsList.append(0)

                nin += 1

        ip += 13





#Flask Section----------------------------------------------------------------------------------------------------------
app = Flask(__name__)

#Home Page-------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('home.html')

#In Progress Page------------------------------------------------------------------------
@app.route('/calculate')
def next():
    # Gets all user inputs from URL and stores them in string
    global stl
    global atl
    stl = ''


    stl = request.url
    #print(stl)

    #Increments stl to build up atl
    #3/2 change for in PyCharm
    i = 7
    atl = ''
    while i < len(stl):
        atl = atl + stl[i]
        i += 1

    #11/20 - test inputStr errors 621
    return render_template('in_progress.html', valueip = atl)

#Algorithm for rankings------------------------------------------------------------------
@app.route('/results')
def results():
    #print("Working")

    global customList
    global finalList
    global reportfinalListC
    global reportfinalListP
    global finalListCollegesOnlyP
    global finalListCollegesOnlyC
    global stl
    global numPcalls
    global numCcalls
    global TICKER
    global fullListP
    global fullListC
    global tfullListC
    global atl

    #Clears all lists
    customList = []
    reportfinalListP = []
    reportfinalListC = []
    finalList = []
    numPcalls = 0
    numCcalls = 0
    finalListCollegesOnlyP = []
    finalListCollegesOnlyC = []
    ultiStr = ''
    endStr = []
    first = ''
    second = ''
    third = ''
    fourth = ''
    fifth = ''
    sixth = ''
    seventh = ''
    eighth = ''
    ninth = ''
    tenth = ''
    eleventh = ''
    twelfth = ''
    thirteenth = ''
    fourteenth = ''
    fifteenth = ''
    sixteenth = ''
    seventeenth = ''
    eighteenth = ''
    nineteenth = ''
    twentieth = ''

    #12/17 suggestion from Dr. Anton - find first value of underscore, then store that value and use that as variable to split at other points
    """
    icheck = 0
    checkcount = 0

    while icheck < 1000:
        try:
            underscore = atl[43]
            break
            #return render_template('test.html', testV = underscore)
        except:
            try:
                underscore = stl[43]
                break
            except:
                icheck += 1
                checkcount += 1"""

    atlCheck = ""

    try:
        underscore = atl[26]
        #print("tried")
        #In PA: underscore = atl[43]
    except:
        try:
            underscore = stl[43]
        except:
            atl = 'https://www.iscollegesearch.com/calculate?s_=Business_&b_=5&wut_=Economics&z_=5&c_=5&d_=5&e_=5&x_=5&f_=5&g_=5&h_=5&i_=5&j_=5&k_=5&l_=5&m_=5&C=Business&Z_=5'
            underscore = atl[43]
            atlCheck = "..."

    #return render_template('test.html', testV = checkcount, testV2 = atl)

    '''tempatl = atl
    atl = str(tempatl)
    print(atl)'''

    # Trims down inputStr
    #3/2 - for now in PyCharm, this commented out and atl = atl v
    try:
        endStr = atl.split(underscore, 1)
        print(endStr)
        ultiStr = endStr[1]
        print("ultiStr1 = ", ultiStr)
    except IndexError:
        ultiStr = str(atl)

    #ultiStr = str(inputStr)
    #stl = str(inputStr)

    # Determines which attributes to actually search for----

    #print(atl)
    # 3 CollegeFactual Attributes First---------------------
    # Undergrad School ranking
    called = False

    uSchoolNameEq = atl.find("=")
    uSchoolIeq = atl.find("b")


    i2 = uSchoolNameEq + 1
    #return render_template('test.html', testV = uSchoolIeq)

    uSchoolName = ''
    while i2 < len(atl):
        if atl[i2] == "&":
            break
        else:
            uSchoolName = uSchoolName + atl[i2]
            i2 += 1

    tusi = uSchoolIeq + 3

    #return render_template('test.html', testV = stl)

    ######%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TODO TODO#######3
    todoexcept = False

    try:
        uSchoolIM = atl[tusi]
    except IndexError:
        uSchoolIM = 7
        todoexcept = True


    #return render_template('test.html', testV = uSchoolIM)

    #print(uSchoolIM)

    if todoexcept == False and atl[uSchoolNameEq + 1] == "&" or uSchoolIeq == -1 or atl[uSchoolIeq + 3] == "0" or atl[uSchoolIeq + 3] == "&":
        TICKER = 1
        pass
    else:
        called = True
        numCcalls += 2

        #Calls both CollegeVine and CollegeFactual functions
        collegeFactual(uSchoolName, uSchoolIM)
        listA(1, "C")
        #print("FinalList: ")
        #print(finalList)

        cVine(uSchoolName, uSchoolIM)
        listA(0.5, "C")

        #Special average now for CF and cV calls
        averageA("C")
        #print(reportfinalListC)
        finalList = []
        finalList = reportfinalListC
        reportfinalListC = []
        #print(finalList)

        #Resets TICKER in this case
        TICKER = 1

    if called == True:
        nextStr = ultiStr.split(underscore, 3)
        print(nextStr)
        ultiStr = nextStr[3]
        numCcalls = 1

    #print("num C calls: " + str(numCcalls))

    # Intended major attribute-----------------------------------------------------------------------------------
    #v  called Determines if CF function is actually called
    called = False
    imNameEq = ultiStr.find("=")
    print(ultiStr)
    print("imNameEq = ", imNameEq)
    iiF = False

    #Loops through to find intended major importance
    fi = 0
    while fi < (len(ultiStr) - 1):
        if ultiStr[fi] != '0' and ultiStr[fi] != '1' and ultiStr[fi] != '2' and ultiStr[fi] != '3' and ultiStr[fi] != '4' and ultiStr[fi] != '5' and ultiStr[fi] != '6' and ultiStr[fi] != '7' and ultiStr[fi] != '8' and ultiStr[fi] != '9':
            pass
        else:
            intendMajorIM = int(ultiStr[fi])
            iiF = True
            break
        fi += 1

    if iiF == False:
        intendMajorIM = 7

    i1 = imNameEq + 1
    intendMajorName = ''
    try:
        while ultiStr[i1] != "&":
            intendMajorName = intendMajorName + ultiStr[i1]
            i1 += 1
    except IndexError:
        intendMajorName = ultiStr

        #print(intendMajorName)



    #intendMajorIM = ultiStr[imNameIeq + 4]
    ##print(intendMajorIM)
    #return render_template('test.html', testV = intendMajorIM)

    if intendMajorIM == 0:
        TICKER += 1
        pass
    else:
        called = True
        numCcalls += 1

        collegeFactual(intendMajorName, intendMajorIM)
        listA(1, "C")

    #Deletes used part of string -- - - - - - - - - -
    nextStr = []
    if called == True:
        #return render_template('test.html', testV = ultiStr)
        try:
            tStr = ultiStr
            nextL = tStr.split("&", 2)
            ultiStr = nextL[2]
        except IndexError:
            pass
        #return render_template('test.html', testV = ultiStr)


    #print(ultiStr)

    # Overall Prestige----------------------------------------------
    oPrestigeIeq = ultiStr.find("c")
    called = False

    if oPrestigeIeq == -1 or ultiStr[oPrestigeIeq + 3] == "0" or ultiStr[oPrestigeIeq + 3] == "&":
        TICKER += 1
        pass
    else:
        called = True
        numCcalls += 1

        collegeFactual("Overall Prestige", oPrestigeIeq + 3)
        listA(3, "C")
        #print(finalList)

    """if called == True:
        return render_template('test.html', testV = ultiStr)

        nextStr = ultiStr.split("_", 1)
        ultiStr = nextStr[1]"""

    # CollegeVine Section------------------------------------------------------------------------------------------------
    # Research (article15)

    rChoiceNameEq = ultiStr.find("C")
    rChoiceIeq = ultiStr.find("Z")

    #print("____:" + ultiStr)

    rChoiceName = ''
    iz = rChoiceNameEq + 2
    endiz = iz + 9

    if rChoiceIeq != -1 or rChoiceIeq == 0:
        while iz < endiz:
            rChoiceName = rChoiceName + ultiStr[iz]
            iz += 1
    else:
        pass

    #print(rChoiceName)

    rChoiceIM = ultiStr[rChoiceIeq + 3]

    #print(rChoiceIM)
    if ultiStr[rChoiceNameEq + 1] == "&" or rChoiceIeq == -1 or ultiStr[rChoiceIeq + 3] == "0" or ultiStr[
        rChoiceIeq + 3] == "&":

        #Add extra zero to all colleges in fullListC if cVine is not called 1
        icv = 0
        lenflc = len(finalList)
        while icv < lenflc:
            if type(finalList[icv]) == str:
                flcstr = finalList.index(finalList[icv])
                finalList.insert(flcstr + 1, 0)
            else:
                pass
            icv += 1
        pass

    else:
        finalpC = "Diverse Research Universities for " + rChoiceName
        cVine(finalpC, rChoiceIM)
        listA(4, "C")
        numCcalls += 1

        #print("FINAL CHECK 12-10 FINALIST v \n\n")
        #print(finalList)

    #12/31 Loops through finalList and adds zeros to all colleges with less than four digits following
    iflco = 0
    while iflco < (len(finalListCollegesOnlyC) - 1):
        tempV = finalListCollegesOnlyC[iflco]
        try:
            tempo = finalList.index(tempV)
            realV = finalList[tempo + 4]
            tempBool = isinstance(realV, float)
            tempBool2 = isinstance(realV, int)
            print(type(realV))
            if tempBool or tempBool2:
                pass
            else:
                finalList.insert(tempo + 1, 0)
        except:
            pass

        iflco += 1
    #---------------------------------------------------------------#

    fullListC = []
    #Add to fullListC
    iff = 0
    while iff < len(finalList):
        fullListC.append(finalList[iff])
        iff += 1

    #NC State Special Case
    if 'north-carolina-state-university' in fullListC:
        ncsui = fullListC.index('north-carolina-state-university')
        fullListC.insert(ncsui + 1, 0)

    #print(fullListC)


    # averageA for CF calls
    ##print(finalListCollegesOnlyC)
    averageA("C")

    #print(reportfinalListC)

    # 11 PrincetonReview attributes next--------------------------------------------------------------------------------
    #Reset TICKER
    TICKER = 0

    #print(ultiStr)

    # List of PrincetonReview attributes
    #First, Engineering special case
    engrIndex = ultiStr.find("E")
    if engrIndex != -1:
        nextStr = ultiStr.split(underscore, 1)
        ultiStr = nextStr[1]

    #print(ultiStr)

    attributesList = ["Their Students Love these colleges", "Students love their school teams",
                      "Campus Beauty", "Cities", "Lots of race_class interaction", "Dorms", "Food",
                      "Public school value top 50", "Private school value top 50", "Internships Public",
                      "Internships Private"]
    pNameLoop = ["d", "e", "x", "f", "g", "h", "i", "j", "k", "l", "m"]
    preimportanceList = []
    importanceList = []

    for letter in pNameLoop:
        pnIndex = ultiStr.find(letter)
        preimportanceList.append(pnIndex)

    #print(preimportanceList)

    for elem in preimportanceList:
        if elem == -1:
            rightIndex = "0"
        else:
            rightIndex = ultiStr[elem + 3]
        ##print(rightIndex)
        if rightIndex == "&" or rightIndex == "0":
            importanceList.append(0)
        else:
            try:
                importanceList.append(int(rightIndex))
            except ValueError:
                importanceList.append(0)

    print("importanceList: v")
    print(importanceList)
    #3/2 Should be 3-campus 5-diversity 6-dorms 7-food

    #Now calls the P functions
    i2 = 0
    while i2 < 11:
        if importanceList[i2] == 0:
            TICKER += 1

            # Add extra zero to all colleges in fullListC if P attribute is not called
            ip = 0
            lenfl = len(finalList)
            while ip < lenfl:
                if type(finalList[ip]) == str:
                    flstr = finalList.index(finalList[ip])
                    finalList.insert(flstr + 1, 0)
                else:
                    pass
                ip += 1
            pass

        else:
            numPcalls += 1

            princetonReview(attributesList[i2], importanceList[i2])
            listA(i2 + 1, "P")

            #Removes first school error
            firstin = finalList[0]

            try:
                findin = firstin.find("-")
                if findin != -1:
                    del finalList[0]
                    del finalList[0]
                    del finalList[0]
                    del finalList[0]
                    del finalList[0]
            except AttributeError:
                while type(finalList[0]) == int:
                    if type(finalList[0]) != int:
                        break
                    else:
                        del finalList[0]

            #print(finalList)

        i2 += 1

    #converions() and averageA() for P calls
    conversions()
    averageA("P")
    print(reportfinalListP)

    #Join P and CF list together-----------------------------------------------------------
    joinA()
    print(reportfinalListC)

    #Deletes Southern New Hampshire University Case
    try:
        snhuT = 0
        snhuT = reportfinalListC.count("southern-new-hampshire-university")
        while snhuT != 0:
            snhuI = reportfinalListC.index("southern-new-hampshire-university")

            del reportfinalListC[snhuI]
            del reportfinalListC[snhuI]
            snhuI = 0
            snhuT -= 1

    except ValueError:
        pass

    #print(reportfinalListC)

    #////////////////Only Exists in PythonAnywhere web version: averages values of duplicates in reportfinalListC/////////////
    lendup = len(reportfinalListC)
    idup = 0
    tlendup = lendup / 4
    reallendup = tlendup * 3

    while idup < reallendup:
        dupcheck = reportfinalListC[idup]
        #print(dupcheck)

        dupcount = reportfinalListC.count(dupcheck)

        #print(dupcount)

        if dupcount > 1:
            tempdupList = []

            # Sets number of times value is looked for
            xdup = 0
            while xdup < dupcount:
                dupindex = reportfinalListC.index(dupcheck)
                tempdupList.append(reportfinalListC[dupindex + 1])
                del reportfinalListC[dupindex]
                del reportfinalListC[dupindex]

                xdup += 1

            #print(tempdupList)

            # Now averages tempdupList
            newdupV = 0
            iadup = 0
            while iadup < len(tempdupList):
                newdupV += tempdupList[iadup]

                iadup += 1

            newdupV /= dupcount

            #print(newdupV)

            # Then appends new, correct values to reportfinalListC
            reportfinalListC.append(dupcheck)
            reportfinalListC.append(newdupV)

        #print("--------------")

        idup += 2

    #print("\n")
    #print(reportfinalListC)

    #return render_template('test.html', testV = reportfinalListC)














    #/////////////////////////////////////////////////////////////////////////////////////////////
    #Still to do --- all attributes link to front end, including those that already exist (like in princetonReview function)

    #3/2 - Finished USNews function, began working on front-end connection

        """Attributes already up:
                -Majors_________
                -Food
                -Diversity
                -Campus
                -Internships
                
            Attrributed not up yet:
                -FYE
                -Study abroad
                """

    finalList = []
    #Intended major----------------
    #TODO 3/4 Duplicates of all colleges on list occur
    try:
        intendMajorNameU = intendMajorName
        intendMajorIMU = intendMajorIM

        print(intendMajorNameU)
        usNews(intendMajorNameU, intendMajorIMU)
        listA(1, "C")

        print(finalList)
    except:
        print("[]Intend Major not Called in U")
        pass

    #Shared PR and USnews attributes---------------------------
    print("importanceList: v")
    print(importanceList)

    # 3/2 Should be 3-campus 5-diversity 7-food       10-internships public 11-internships private
    campusU = importanceList[2]
    diversityU = importanceList[4]
    foodU = importanceList[6]
    internU1 = importanceList[9]
    internU2 = importanceList[10]

    if campusU != 0:
        usNews("Campus", campusU)
    if diversityU != 0:
        usNews("Diversity", diversityU)
    if foodU != 0:
        usNews("Food", foodU)

    if internU1 != 0:
        usNews("Internships", internU1)
    elif internU2 != 0:
        usNews("Internships", internU2)


    #Unique USNews Attributes----------------------------------------
    print("Latest ultiStr: " + ultiStr)

    #Now find Q and X in ultiStr
    #Study Abroad
    QstudyI = ultiStr.find("Q")
    if QstudyI != -1:
        try:
            Qim = int(ultiStr[QstudyI + 3])
        except:
            Qim = 0
        if Qim != 0:
            usNews("Study Abroad", Qim)

    XexpI = ultiStr.find("X")
    if XexpI != -1:
        try:
            Xim = int(ultiStr[XexpI + 3])
        except:
            Xim = 0
        if Xim != 0:
            usNews("Study Abroad", Xim)

    #Joins USNews (reportfinalListU) with reportfinalListC-----------------------------------------------------------



    #Gets top 10 schools   ... or top 20 schools---------------------------------------------------------------
    bestSort()
    tenor20 = request.args.get("z", "twenty")
    #print(tenor20)
    #print(customList)

    #Other Way
    first = customList[0]
    second = customList[1]
    third = customList[2]
    fourth = customList[3]
    fifth = customList[4]
    sixth = customList[5]
    seventh = customList[6]
    eighth = customList[7]
    ninth = customList[8]
    tenth = customList[9]

    if tenor20 == "twenty":
        eleventh = customList[10]
        twelfth = customList[11]
        thirteenth = customList[12]
        fourteenth = customList[13]
        fifteenth = customList[14]
        sixteenth = customList[15]
        seventeenth = customList[16]
        eighteenth = customList[17]
        nineteenth = customList[18]
        twentieth = customList[19]

    if tenor20 == "twenty":
        return render_template('results.html', value1 = first, value2 = second, value3 = third, value4 = fourth, value5 = fifth, value6 = sixth, value7 = seventh, value8 = eighth, value9 = ninth, value10 = tenth, value11 =  "11. " + eleventh, value12 = "12. " + twelfth, value13 = "13. " + thirteenth, value14 = "14. " + fourteenth, value15 = "15. " + fifteenth, value16 = "16. " + sixteenth, value17 = "17. " + seventeenth, value18 = "18. " + eighteenth, value19 = "19. " + nineteenth, value20 = "20. " + twentieth, valueCheck = atlCheck)
    else:
        return render_template('results.html', value1=first, value2=second, value3=third, value4=fourth, value5=fifth, value6=sixth, value7=seventh, value8=eighth, value9=ninth, value10=tenth, valueCheck = atlCheck)

#Filters rankings based on acceptance rate... and ---------------------------------------
@app.route('/filter')
def filter():

    #Acceptance Rate Section--------------------------------------------------------

    global customList
    global aRateDict
    global sizeDict
    global preattList

    #1/10 -> potential errors with customList check
    #return render_template('test.html', testV = customList)

    #Gets ALL inputs nows
    minimum = int(request.args.get("filterI"))
    #print(minimum)

    sMin = request.args.get('sizeMin>', 100)
    sMax = request.args.get('sizeMax<', 60000)

    #return render_template('test.html', testV = sMax)

    try:
        fsMin = int(sMin)
        fsMax = int(sMax)
    except ValueError or TypeError:
        fsMin = 100
        fsMax = 60000

    if fsMin < 0 or fsMin == 0:
        fsMin = 100

    if fsMin > fsMax:
        fsMin = 100
        fsMax = 60000

    filterListCounter = 0
    i = 0
    filterList = []

    while filterListCounter < 15:
        while i < len(customList):
            if filterListCounter > 9:
                # #prints final filtered list
                #print(filterList)

                #Resets final place values
                first = ''
                second = ''
                third = ''
                fourth = ''
                fifth = ''
                sixth = ''
                seventh = ''
                eighth = ''
                ninth = ''
                tenth = ''

                first = filterList[0]
                second = filterList[1]
                third = filterList[2]
                fourth = filterList[3]
                fifth = filterList[4]
                sixth = filterList[5]
                seventh = filterList[6]
                eighth = filterList[7]
                ninth = filterList[8]
                tenth = filterList[9]

                #Fake list for git commits
                fakelist = []
                #2/10 renamed
                #It's the return of the no wait ah wait you're kidding

                #Reformats, then appends to list to be used in attribute-by-attribute report page
                preattList = []
                ipl = 0
                while ipl < 10:
                    tempipl = filterList[ipl]
                    preattList.append(tempipl)
                    ipl += 1

                preattList = [x.lower() for x in preattList]
                preattList = [z.replace(' - ', ' ') for z in preattList]
                preattList = [y.replace(' ', '-') for y in preattList]

                #print(aRateDict)
                #print("split")
                #print(sizeDict)

                #return render_template('test.html', testV = preattList)

                return render_template('filter.html', value1b = first, value2b = second, value3b = third, value4b = fourth, value5b = fifth, value6b = sixth, value7b = seventh, value8b = eighth, value9b = ninth, value10b = tenth, valuepal = preattList)

            else:
                # Then search google for acceptance rate of each college on customList
                nowQuery = customList[i]

                try:
                    value = aRateDict[nowQuery]
                    sizeV = sizeDict[nowQuery]

                    #print("Found: " + nowQuery)
                    #print(str(value))
                    #print(str(sizeV))

                    fsV = int(sizeV)
                    fsBool = False

                    if (fsV > fsMin and fsV < fsMax) or fsV == 0:
                        fsBool = True

                    #Appends to filter list
                    if value > minimum and fsBool:
                        filterList.append(nowQuery)
                        filterListCounter += 1
                    else:
                        pass
                    i += 1
                except KeyError:
                    # Searches Google to find URL of CF site and gets acceptance rate data
                    query = "CollegeFactual " + nowQuery

                    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
                        goodURL2 = j

                    #print("Hello: " + goodURL2)
                    # Gets HTML Data from URL
                    r = requests.get(goodURL2)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    f = soup.find_all('div', class_="grid quick-stats")
                    h = soup.find('div', class_="grid quick-stats")
                    g = str(h.get_text())

                    # Gets undergrad population-------------------------
                    # #print(f)
                    sf = str(f)

                    ssf = sf.split(',', maxsplit=10)

                    onesf = ssf[5]
                    finalsf = onesf[len(onesf) - 2]
                    finalsf = finalsf + onesf[len(onesf) - 1]

                    twosf = ssf[6]
                    finalsf = finalsf + twosf[0]
                    finalsf = finalsf + twosf[1]
                    finalsf = finalsf + twosf[2]

                    if finalsf[0] == '>':
                        finalsf = finalsf.replace(">", "")

                    # TODO Potential TypeError
                    try:
                        finalisf = int(finalsf)
                    except ValueError:
                        finalisf = 0

                    # Acceptance rate find----------------------------------
                    aRateIndex = g.find("%")
                    ultiRateInt = 0

                    finalaRate = []
                    finalaRate.append(g[aRateIndex - 1])
                    if g[aRateIndex - 2] == "y":
                        ultiaRateInt = int(finalaRate[0])
                        pass
                    elif goodURL2 == "https://www.collegefactual.com/colleges/thomas-aquinas-college/rankings/":
                        ultiaRateInt = 1
                    else:
                        finalaRate.insert(0, (g[aRateIndex - 2]))
                        tempaRateInt = ''
                        tempaRateInt = finalaRate[0] + finalaRate[1]
                        ultiaRateInt = int(tempaRateInt)
                    # #print(g)
                    # #print(aRateIndex)
                    # Returns integer of acceptance rate---------- And Size integers

                    #print(finalisf)
                    #print(ultiaRateInt)

                    # Adds both values to storage dictionary
                    # aRateDict[customList[i]] = ultiaRateInt

                    # sizeDict[customList[i]] = finalisf

                    # Now adds acceptance rates above value to filterList
                    if ultiaRateInt > minimum and ((finalisf > fsMin and finalisf < fsMax) or finalisf == 0):
                        filterList.append(nowQuery)
                        filterListCounter += 1
                        #print(filterListCounter)
                    i += 1

#Finally, attribute-by-attribute report at the end
@app.route('/areport')
def areport():
    global preattList
    global fullListP
    global fullListC
    global tfullListC
    global specificsList

    #print("\n")
    #print(preattList)

    #print(fullListC)
    #print(fullListP)

    ##Test Return
    #return render_template('test.html', testV = preattList)

    rList()

    i = 0
    lastList = []
    arerror = "Hit the browser's back arrow and try again"

    while i < 10:
        try:
            if preattList[i] in specificsList:
                slo = specificsList.index(preattList[i])

                slomax = slo + 16
                while slo < slomax:
                    lastList.append(specificsList[slo])
                    slo += 1
            else:
                lastList.append("x")

            i += 1
        except:
            return render_template('test.html', testV = preattList, testV2 = arerror)

    #Now converts everything into table---------------------------------------------------------------------------------
    # These 15 are the columns of the tables
    t = PrettyTable(['College', 'Intern Pri', 'Intern Pub', 'Value Pri', 'Value Pub', 'Food', 'Dorms', 'Diversity', 'Town', 'Campus', 'Sports', 'Happy', 'Research', 'Prestige', 'Major', 'uSchool'])

    i2 = 0
    tempList = []

    while i2 < 10:
        tempList = []

        try:
            li = lastList.index(preattList[i2])
            #print(li)

            maxli = li + 16
            #print(maxli)

            listart = li + 1
            #print(listart)

            tempList.append(preattList[i2])
            #print(tempList)

            inkli = listart

            while inkli < (maxli + 1):
                #print("inkli: " + str(inkli))
                #print("maxli: " + str(maxli))

                try:
                    lli = lastList[inkli]
                    #print("lli" + str(lli))
                    intB = isinstance(lli, int)
                    floatB = isinstance(lli, float)
                    #print(intB)
                    #print(floatB)
                    isnotstr = intB or floatB
                    #print(isnotstr)
                    lentB = len(tempList)
                    #print("lentB: " + str(lentB))

                    if isnotstr == False or inkli == (maxli + 1) or inkli > (maxli + 1) or lentB == 16 or lentB > 16:
                        try:
                            t.add_row(tempList)
                            tempList = []
                            i2 += 1

                            #print(t)
                            break
                        except:
                            i2 += 1
                            break
                    else:
                        tempList.append(lastList[inkli])
                        inkli += 1

                        #print("lentB special: " + str(lentB))
                        #print(tempList)

                except IndexError:
                    if i2 >= 10:
                        break
                    else:
                        i2 += 1
                        t.add_row(tempList)
                        tempList = []

                #print(t)
        except:
            i2 += 1

    #print(t)

    #return render_template('test.html', testV = t)

    #Converts to HTML---------------------------------------------------------------------------------------
    headerHTML = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Final Report</title>

        <!--Favicon-->
        <link rel="icon" type="image/x-icon" href="static/favicon.ico">

        <articletop>
            Custom College Search &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a style="text-decoration-color:mediumseagreen;" href="https://docs.google.com/document/d/1QtNWo_EUQdz14494aZvGdapv7yCHZZ70vJnsSHIqkJA/edit?tab=t.0"><span style="color:mediumseagreen;">Instructions</span></a>
            <br />
        </articletop>

        <!-- Link to CSS File -->
        <link href="static/IS.UI_V1.css" type="text/css" rel="stylesheet">

        <br />
        <br />
    </head>
    """

    footerHTML = """
    <footer>
        {{ valueLL }}
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v1.2
        <br />
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Last Updated: 11/25/24
        <br/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/apearl2">Connect on Github</a>
        <br/>
    </footer>
    """

    htmlCode = t.get_html_string()

    #print(htmlCode)

    #2/11 Test Github
    
    #1/2 file creation version using random module
    nameNum = 1
    nameNum = random.randint(1, 1000000)
    snameNum = str(nameNum)
    baseUrl = "/home/iscollegesearch/mysite/templates/numreport"
    endbUrl = ".html"
    fullUrl = ""
    fullUrl = baseUrl + snameNum + endbUrl

    fo = open(fullUrl, "w")
    fo.write(headerHTML + htmlCode + footerHTML)
    fo.close()

    tretName = "numreport"
    tendName = ".html"
    fullRet = ""
    fullRet = tretName + snameNum + tendName

    return render_template(fullRet, valueLL = lastList)


#Runs Flask------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()


