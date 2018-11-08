#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 21:30:20 2018

@author: dutchman
"""
from bs4 import BeautifulSoup


def main(gmlfile, output='output.gml', tag='bldg:RoofSurface'):
    with open(gmlfile, 'r') as f:
        xml = f.read()
        f.close()

    soup = BeautifulSoup(xml, 'lxml-xml')

    lines = xml.split('\n')
    roofs = soup.find_all(tag)

    out = open(output ,'w')

    out.write(lines[0] + '\n')
    out.write(lines[1] + '\n')


    for roof in roofs:
        out.write(str(roof))

    out.write('\n' + lines[-1])

    out.close()


if __name__ == '__main__':
    main('3890_5819.gml')

