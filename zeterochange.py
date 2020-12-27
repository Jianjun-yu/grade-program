#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-02 21:25:46
# @Author  : Jianjun Yu 
# @Link    : http://example.org
# @Version : 3.0
"""
This file strips fields from a biblatex file. The original code was written by astrobel found here: 
https://forums.zotero.org/discussion/22629/bibtex-export-request-option-to-omit-certain-fields-for-less-cluttered-bibliographies  
Jake Chanenson made the code more robust by modifying it to run from the command line, automatic outputfile creation, giving options on what to strip 
and taking in multiple fields to strip. The code can be found here:
https://github.com/JakeC007/Biblatex-Field-Stripper
I moderate the code to fit political science's journals and add a new function to moderate date format. I also change a lopp to make the code more efficient and fix a small problem that lead to failure of removing abstract. 
"""


import sys


def main():
    if len(sys.argv) != 1:
        print("Usage: python3 prog.py ")
        sys.exit

    inputF = ''
    raw_inputF = input("Enter your .bib filename: ")
    inputF = raw_inputF + '.bib'
    outputF = raw_inputF + 'FIXED'+'.bib'

    lst_strip_options = getOptions(inputF)

    if lst_strip_options == "quit":  # handle IOError
        sys.exit

    else:
        print("These are your options of what you can strip:\n {}".format(
            lst_strip_options[0:]))
        
        # Get user input on what to strip
        q_flag = True
        strip = []
        while q_flag is True:
            raw_strip = input(
                "What would you like to strip? \n input politics to automatically apply Chicago format (press q to when you're done): ")
            if raw_strip == "q":
                break
            if raw_strip in lst_strip_options:  # validating input
                strip.append(raw_strip)
                print("Things to strip:", end=" ")
                print(strip)
            # easy way to apply chicago format for political science journals
            if raw_strip == "politics":
                keys=politics_input(lst_strip_options)
                print ("Using Chicago format for political science. The keys reminded are", end=" ")
                print(keys)
                strip=lst_strip_options
                print (strip)
            else:
                print("Please input one of the options listed above.")
        #mchange date from y/m/d to y
        date = "N"
        if "date" not in strip:
            date = input("Do you want to moderate date (only remind year of published) \n Y/N")
        clean(inputF, outputF, strip, date)
        end_pos = len(strip)-1
        print("Cleaned {} from {} and writing to {}".format(
            strip[0:end_pos], inputF, outputF))


def getOptions(inputF):
    strip_options = []
    try:
        with open(inputF, 'r', encoding='UTF-8') as f:
            for line in f:
                temp_word = line.split(None, 1)
                try:
                    if '@' not in temp_word[0] and '}' not in temp_word[0]:
                        strip_options.append(temp_word[0])
                except:  # edge case for blank lines
                    pass
    except IOError:  # If the input file was not found
        print("File not found. Please input the filename w/out the extension")
        return "quit"
    strip_lst = list(dict.fromkeys(strip_options))  # remove duplicates
    return strip_lst


def clean(inputF, outputF, strip, date):
    filename = inputF  # the input file
    filename2 = outputF  # create a new file for output
    start = ''  # set type for field to strip

    tripped = False  # flag to ensure that none of the desired fields have been found
    with open(filename, encoding='UTF-8') as infile, open(filename2, 'w', encoding='UTF-8') as outfile:
        for line in infile:                      ####################do not forget to write a function to check whether the field include more than one line
            tripped = False
            for word in strip:
                start = word + ' = '  # current word to strip
                if line.strip().startswith(start) is True:
                    tripped = True
            if tripped is False:  # none of the desired fields have been found
                if date=="N":  # no date transfer 
                    outfile.write(line)
                else:
                    if line.strip().startswith("date = ") is False: 
                        outfile.write(line)
                    else:  #date transfer
                        year = moderatedate(line)
                        outfile.write(year)


def politics_input (fullstrip):
	#keys reminded
	strips = ['title', 'volume','pages', 'number', 'journaltitle', 'shortjournal','author' ,'date']
	for strip in strips:
		fullstrip.remove(strip)
	return strips

def moderatedate(line):
    year = line [0:13] + "},"
    return year


if __name__ == "__main__":
    main()
