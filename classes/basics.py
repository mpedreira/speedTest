#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.parse import urlparse
import datetime


def eliminar_caracteres(texto):
    replacements = (
        ('á', 'a'),
        ('é', 'e'),
        ('í', 'i'),
        ('ó', 'o'),
        ('ú', 'u'),
        ('ñ', 'n'),
    )
    for old, new in replacements:
        texto = texto.replace(old, new).replace(old.upper(), new.upper())
    return texto


def urlEncode(text):
    return urlparse(text)


def unique(list1):
    # intilize a null list
    unique_list = []
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    return unique_list


def writeDebug(file, content):
    try:
        f = open(file, 'w')
        f.write(eliminar_caracteres(content))
        f.close()
        return True
    except FileNotFoundError:
        return False


def extractTags(text, separator):
    return text.split(separator)
