#!/usr/bin/env python3
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- CLAM Wrapper script for Text Statistics --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################

from __future__ import print_function, unicode_literals, division, absolute_import

#This script will be called by CLAM and will run with the current working directory set to the specified project directory

#import some general python modules:
import sys
import os
import datetime
import xmlrpc.client
#import CLAM-specific modules. The CLAM API makes a lot of stuff easily accessible.
import clam.common.data
import clam.common.status

def total_seconds(delta):
    return delta.days * 86400 + delta.seconds + (delta.microseconds / 1000000.0)

#########################################################################################################
#       MAIN WRAPPER
#########################################################################################################


if __name__ == "__main__":

    #this script takes three arguments from CLAM: $DATAFILE $STATUSFILE $OUTPUTDIRECTORY  (as configured at COMMAND= in the service configuration file)
    datafile = sys.argv[1]
    statusfile = sys.argv[2]
    outputdir = sys.argv[3]
    MTSYSTEM_NLFY_HOST = sys.argv[4]
    MTSYSTEM_NLFY_PORT = int(sys.argv[5])
    MTSYSTEM_FYNL_HOST = sys.argv[6]
    MTSYSTEM_FYNL_PORT = int(sys.argv[7])

    cwdir = os.getcwd()

    #Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml))
    clamdata = clam.common.data.getclamdata(datafile)

    #You now have access to all data. A few properties at your disposition now are:
    # clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

    clam.common.status.write(statusfile, "Aan het opstarten...")


    for i, inputfile in enumerate(clamdata.input):
        #Update our status message to let CLAM know what we're doing
        clam.common.status.write(statusfile, "Bezig met " + os.path.basename(str(inputfile)) + "...", round((i/float(len(clamdata.input)))*100))

        try:
            inputfile.loadmetadata()
            #print("Metadata for "+ str(inputfile)+": " + " ".join(k +"=" + v for k,v in metadata.items()), file=sys.stderr)
        except Exception as e:
            print("Error in loading metadata for " + str(inputfile),file=sys.stderr)
            print( str(e),file=sys.stderr)
        extraext = ''
        tokenise = True
        if inputfile.metadata and 'tokenised' in inputfile.metadata:
            print("Tokenised?", inputfile.metadata['tokenised'],file=sys.stderr)
            if inputfile.metadata['tokenised'] == 'ja':
                print("Tokenisation disabled",file=sys.stderr)
                tokenise = False

        if tokenise:
            begintime = datetime.datetime.now()

            if str(inputfile)[-7:] == '.nl.txt':
                print("*** CALLING TOKENISER (NL) FOR " + os.path.basename(str(inputfile)) + "***",file=sys.stderr)
                cmd = 'ucto -n -Lnld ' + cwdir + '/' + str(inputfile) + ' ' +  cwdir + '/' + str(inputfile) + '.tok'
                print( cmd,file=sys.stderr)
                r = os.system(cmd)
                extraext = '.tok'
                d = total_seconds(datetime.datetime.now() - begintime)
                print( "Tokenisation took " + str(d) + 's',file=sys.stderr)
            if str(inputfile)[-7:] == '.fy.txt':
                print( "*** CALLING TOKENISER (FY) FOR " + os.path.basename(str(inputfile)) + "***",file=sys.stderr)
                cmd = 'ucto -n -Lfry ' +  cwdir + '/' + str(inputfile) + ' ' +  cwdir + '/' + str(inputfile) + '.tok'
                print( cmd,file=sys.stderr)
                r = os.system(cmd)
                extraext = '.tok'
                d = total_seconds(datetime.datetime.now() - begintime)
                print( "Tokenisation took " + str(d) + 's',file=sys.stderr)



        begintime = datetime.datetime.now()
        if str(inputfile)[-7:] == '.nl.txt':
            print( "*** STARTING SYSTEM (NL->FY) FOR " + os.path.basename(str(inputfile)) + " ***",file=sys.stderr)
            outputfile = outputdir + '/' + os.path.basename(str(inputfile))[:-7] + '.fy.txt'
            try:
                inittime = datetime.datetime.now()
                client = xmlrpc.client.ServerProxy('http://' + MTSYSTEM_NLFY_HOST +':' + str(MTSYSTEM_NLFY_PORT))
                d = total_seconds(datetime.datetime.now() - inittime)
                print( "Client initialisation time: " + str(d) + 's',file=sys.stderr)
            except Exception as e:
                clam.common.status.write(statusfile, "Interne vertaalserver niet bereikbaar op dit moment",100) # status update
                print("De interne vertaalserver (Nederlands-Fries) is niet bereikbaar",file=sys.stderr)
                print( str(e),file=sys.stderr)
                sys.exit(1)
            f = open(outputfile,'w',encoding='utf-8')
            sentences = 0
            f_in = open(str(inputfile)+ extraext,'r',encoding='utf-8')
            for line in f_in:
                sentences += 1
                failed = False
                try:
                    result = client.translate({"text":line})
                    f.write(result['text'] + "\n")
                except Exception as e:
                    print("Failure processing translation on line " + str(sentences),file=sys.stderr)
                    print( str(e),file=sys.stderr)
            f_in.close()
            f.close()
            d = total_seconds(datetime.datetime.now() - begintime)
            if sentences:
                print( "Translation took " + str(d) + 's (average' + str(d/float(sentences)) + 's per sentence)',file=sys.stderr)

        elif str(inputfile)[-7:] == '.fy.txt':
            print( "*** STARTING SYSTEM (FY-NL) FOR " + os.path.basename(str(inputfile)) + " ***",file=sys.stderr)
            outputfile = outputdir + '/' + os.path.basename(str(inputfile))[:-7] + '.nl.txt'
            try:
                inittime = datetime.datetime.now()
                client = xmlrpc.client.ServerProxy('http://' + MTSYSTEM_FYNL_HOST +':' + str(MTSYSTEM_FYNL_PORT))
                d = total_seconds(datetime.datetime.now() - inittime)
                print( "Client initialisation time: " + str(d) + 's',file=sys.stderr)
            except Exception as e:
                clam.common.status.write(statusfile, "Interne vertaalserver niet bereikbaar op dit moment",100) # status update
                print("De interne vertaalserver (Fries-Nederlands) is niet bereikbaar",file=sys.stderr)
                print( str(e),file=sys.stderr)
                sys.exit(1)

            f = open(outputfile,'w',encoding='utf-8')
            f_in = open(str(inputfile)+ extraext,'r',encoding='utf-8')
            sentences = 0
            for line in f_in:
                sentences += 1
                try:
                    result = client.translate({"text":line})
                    f.write(result['text'] + "\n")
                except Exception as e:
                    print("Failure processing translation on line " + str(sentences),file=sys.stderr)
                    print( str(e),file=sys.stderr)
            f_in.close()
            f.close()
            d = total_seconds(datetime.datetime.now() - begintime)
            if sentences:
                print( "Translation took " + str(d) + 's (average' + str(d/float(sentences)) + 's per sentence)',file=sys.stderr)


    #A nice status message to indicate we're done
    clam.common.status.write(statusfile, "Klaar",100) # status update

    sys.exit(0) #non-zero exit codes indicate an error and will be picked up by CLAM as such!
