#!/usr/bin/env python

import string
import os

inp = open(".newmodel", "r")
oup = open("models_tmp.py", 'w')

Type = [['URL', 'url', 'Url'], ['Char', 'char', 'CHAR'], ['ManyToMany', \
    'manytomany', 'Manytomany'], ['Integer', 'int', 'INT'], ['ForeignKey', \
    'foreign', 'foreignkey'], ['OnetoOne', 'onetoone'], ['DateTime', \
    'datetime'], ]


val = 'Start'
while val != '':
    val = inp.readline()
    if val == '':
        break

    if val != '\n':
        val = val[:len(val)-1]
    else:
	    continue

    oup.write("    ")
    s = val.split(' ')

    if len(s) == 1:

        #name = '\"Class '+ s[0] + '\"'
        #command = 'grep '+ name + ' models.py'
        #print os.system('ls')
        #exist = os.system(command)
        #print command
        #exit(0)
        oup.write('\nclass ' + s[0] + "(models.Model):\n")
    else:
        for it in Type:
            if s[1] in it:
                s[1] = it[0]
                break

        oup.write(s[0] + ' = models.' + s[1]) 
        if it[0] != 'ForeignKey':
            oup.write('Field(')
        else:
            oup.write('(')

        if (len(s) == 2):
            oup.write(')\n')
        else:
            i = 2
            while i < len(s):
                if s[i] == 'blank':
                    oup.write('blank = True')
                elif s[i] == 'null':
                    oup.write('null = True')
                elif s[i] == 'auto_now' or s[i] == 'auto_now_add':
                    oup.write(s[i] + ' = True')
                else:
                    oup.write(s[i])
                i = i+1
                if (i != len(s)):
                    oup.write(', ')
                else:
                    oup.write(')\n')
            

oup.write('\n')

inp.close()
oup.close()

