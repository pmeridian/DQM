#!/usr/bin/env python   

import sys
import os
from array import *

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-i","--inputFile")
parser.add_option("-o","--outputFile")

(options,args)=parser.parse_args()
import ROOT as r
r.gROOT.SetBatch(1)
#r.gStyle.SetOptStat(0)
#r.gStyle.SetOptTitle(0)

r.gROOT.ProcessLine(".L drawRawData.C+")
file = r.TFile.Open(options.inputFile)

if (not file.IsOpen()):
    print "Cannot open "+ options.inputFile
    exit(-1)

tree = file.Get("eventRawData")
a=r.drawRawData(tree)
a.outFile=options.outputFile+".root"
a.Loop()

outFile = r.TFile.Open(options.outputFile+".root")

if (not outFile.IsOpen()):
    print "Cannot open "+ options.inputFile
    exit(-1)

types = {}
for key in outFile.GetListOfKeys():
    name = key.GetName()
    if (len(name.split('_'))>1):
        type=name.split('_')[0]
        if type not in types.keys():
            types[type]=[]
        types[type].append(name)
#print types

c=r.TCanvas("c","c",1500,900)
c.Divide(8,4,0,0)
for i in range(1,33):
    c.cd(i)
    outFile.Get("ADC_adcSpectra_%d"%(i-1)).Draw()
c.SaveAs(options.outputFile+".png")
    
