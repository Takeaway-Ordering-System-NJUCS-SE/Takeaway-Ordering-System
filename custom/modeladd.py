#!/usr/bin/env python

import string
import os

inp = open(".newmodel", "r")
oup = open("models_tmp.py", 'w')

Type = [['URL', 'url', 'Url'], ['Char', 'char', 'CHAR'], ['ManyToMany', \
    'manytomany', 'Manytomany'], ['Integer', 'int', 'INT'], ['ForeignKey', \


oup.write('\n')

inp.close()
oup.close()

