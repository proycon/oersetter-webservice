#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Service Configuration File --
#       by Maarten van Gompel (proycon)
#       http://ilk.uvt.nl/~mvgompel
#       Induction for Linguistic Knowledge Research Group
#       Universiteit van Tilburg
#
#       Licensed under GPLv3
#
###############################################################

from __future__ import print_function, unicode_literals, division, absolute_import

from clam.common.parameters import *
from clam.common.formats import *
from clam.common.converters import *
from clam.common.viewers import *
from clam.common.data import *
from base64 import b64decode as D
#from clam.common.digestauth import pwhash
import sys

import os
host = os.uname()[1]


REQUIRE_VERSION = 0.9

# ======== GENERAL INFORMATION ===========

# General information concerning your system.


#The System ID, a short alphanumeric identifier for internal use only
SYSTEM_ID = "oersetter"

#System name, the way the system is presented to the world
SYSTEM_NAME = "Oersetter"

#An informative description for this system (this should be fairly short, about one paragraph, and may not contain HTML)
SYSTEM_DESCRIPTION = "Frysk-Nederlânske oersetter / Fries-Nederlands vertaalsysteem"

# ======== LOCATION ===========

#The root directory for CLAM, all project files, (input & output) and
#pre-installed corpora will be stored here. Set to an absolute path:

USERS = None

if 'VIRTUAL_ENV' in os.environ:
    ROOT = os.environ['VIRTUAL_ENV'] + "/oersetter.clam/"
    PORT = 8080

    if host == 'mlp01': #configuration for server in Nijmegen
        HOST = "webservices-lst.science.ru.nl"
        URLPREFIX = 'oersetter'


        if not 'CLAMTEST' in os.environ:
            ROOT = "/var/www/webservices-lst/live/writable/oersetter/"
            if 'CLAMSSL' in os.environ:
                PORT = 443
            else:
                PORT = 80
        else:
            ROOT = "/var/www/webservices-lst/test/writable/oersetter/"
            PORT = 81

        USERS_MYSQL = {
            'host': 'mysql-clamopener.science.ru.nl',
            'user': 'clamopener',
            'password': D(open(os.environ['CLAMOPENER_KEYFILE']).read().strip()),
            'database': 'clamopener',
            'table': 'clamusers_clamusers'
        }
        DEBUG = False
        REALM = "WEBSERVICES-LST"
        DIGESTOPAQUE = open(os.environ['CLAM_DIGESTOPAQUEFILE']).read().strip()
        SECRETKEY = open(os.environ['CLAM_SECRETKEYFILE']).read().strip()
        ADMINS = ['proycon','antalb','wstoop']


        BASEDIR = "/var/www/webservices-lst/live/repo/oersetter-webservice"
        MTSYSTEM_NLFY_HOST = 'localhost'
        MTSYSTEM_NLFY_PORT = 2003
        MTSYSTEM_FYNL_HOST = 'localhost'
        MTSYSTEM_FYNL_PORT = 2002
    elif host == 'applejack': #configuration for server in Nijmegen
        HOST = "webservices-lst.science.ru.nl"
        URLPREFIX = 'oersetter'


        if not 'CLAMTEST' in os.environ:
            ROOT = "/scratch2/www/webservices-lst/live/writable/oersetter/"
            if 'CLAMSSL' in os.environ:
                PORT = 443
            else:
                PORT = 80
        else:
            ROOT = "/scratch2/www/webservices-lst/test/writable/oersetter/"
            PORT = 81

        USERS_MYSQL = {
            'host': 'mysql-clamopener.science.ru.nl',
            'user': 'clamopener',
            'password': D(open(os.environ['CLAMOPENER_KEYFILE']).read().strip()),
            'database': 'clamopener',
            'table': 'clamusers_clamusers'
        }
        DEBUG = False
        REALM = "WEBSERVICES-LST"
        DIGESTOPAQUE = open(os.environ['CLAM_DIGESTOPAQUEFILE']).read().strip()
        SECRETKEY = open(os.environ['CLAM_SECRETKEYFILE']).read().strip()
        ADMINS = ['proycon','antalb','wstoop']


        BASEDIR = "/scratch2/www/webservices-lst/live/repo/fryskemt"
        MTSYSTEM_NLFY_HOST = 'localhost'
        MTSYSTEM_NLFY_PORT = 2003
        MTSYSTEM_FYNL_HOST = 'localhost'
        MTSYSTEM_FYNL_PORT = 2002
else:
    raise Exception("I don't know where I'm running from!")

#The hostname of the system. Will be automatically determined if not set. (If you start clam with the built-in webserver, you can override this with -H)
#Users *must* make use of this hostname and no other (even if it points to the same IP) for the web application to work.
#HOST = 'localhost'

#If the webservice runs in another webserver (e.g. apache, nginx, lighttpd), and it
#doesn't run at the root of the server, you can specify a URL prefix here:
#URLPREFIX = "/myservice/"

#The location of where CLAM is installed (will be determined automatically if not set)
#CLAMDIR = "/path/to/clam"

# ======== AUTHENTICATION & SECURITY ===========

#Users and passwords

#set security realm, a required component for hashing passwords (will default to SYSTEM_ID if not set)
#REALM = SYSTEM_ID

#If you want to enable user-based security, you can define a dictionary
#of users and (hashed) passwords here. The actual authentication will proceed
#as HTTP Digest Authentication. Although being a convenient shortcut,
#using pwhash and plaintext password in this code is not secure!!

#USERS = { user1': '4f8dh8337e2a5a83734b','user2': pwhash('username', REALM, 'secret') }

#Amount of free memory required prior to starting a new process (in MB!), Free Memory + Cached (without swap!). Set to 0 to disable this check (not recommended)
REQUIREMEMORY = 10

#Maximum load average at which processes are still started (first number reported by 'uptime'). Set to 0 to disable this check (not recommended)
MAXLOADAVG = 25.0

#Minimum amount of free diskspace in MB. Set to 0 to disable this check (not recommended)
DISK = '/dev/sda1' #set this to the disk where ROOT is on
MINDISKSPACE = 10


# ======== WEB-APPLICATION STYLING =============

#Choose a style (has to be defined as a CSS file in style/ ). You can copy, rename and adapt it to make your own style
STYLE = 'classic'

# ======== ENABLED FORMATS ===========

#Here you can specify an extra formats module
CUSTOM_FORMATS_MODULE = None

# ======== PREINSTALLED DATA ===========

#INPUTSOURCES = [
#    InputSource(id='sampledocs',label='Sample texts',path=ROOT+'/inputsources/sampledata',defaultmetadata=PlainTextFormat(None, encoding='utf-8') ),
#]

# ======== PROFILE DEFINITIONS ===========

PROFILES = [
    Profile(
        InputTemplate('input-fy', PlainTextFormat,"Friese tekst / Fryske tekst",
            StaticParameter(id='encoding',name='Encoding',description='De encoding van de tekst / De encoding fan de tekst', value='utf-8'),
            StaticParameter(id='language',name='Taal / Sprake',description='De taal van de tekst / De sprake fan de tekst', value='fy'),
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            CharEncodingConverter(id='latin1',label='Converteer van Latin-1',charset='iso-8859-1'),
            CharEncodingConverter(id='latin15',label='Converteer van Latin-9',charset='iso-8859-15'),
            PDFtoTextConverter(id='pdfconv',label='Converteer van PDF Document'),
            MSWordConverter(id='docconv',label='Converteer van MS Word Document'),
            ChoiceParameter(id='tokenised',name='Getokeniseerd',description='Is dit document al getokeniseerd?', choices=['ja','nee'],default='nee'),
            extension='fy.txt',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        OutputTemplate('output-nl',PlainTextFormat,u'Nederlandse vertaling / Nederlânske oersetting',
            SetMetaField('encoding','utf-8'),
            SetMetaField('language','nl'),
            removeextension='.fy.txt',
            extension='nl.txt',
            multi=True
        ),
    ),
    Profile(
        InputTemplate('input-nl', PlainTextFormat,u"Nederlandse tekst / Nederlânske tekst",
            StaticParameter(id='encoding',name='Encoding',description='De encoding van de tekst / De encoding fan de tekst', value='utf-8'),
            StaticParameter(id='language',name='Taal / Sprake',description='De taal van de tekst / De sprake fan de tekst', value='nl'),
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            CharEncodingConverter(id='latin1',label='Convert from Latin-1',charset='iso-8859-1'),
            CharEncodingConverter(id='latin15',label='Convert from Latin-9',charset='iso-8859-15'),
            PDFtoTextConverter(id='pdfconv',label='Convert from PDF Document'),
            MSWordConverter(id='docconv',label='Convert from MS Word Document'),
            ChoiceParameter(id='tokenised',name='Getokeniseerd',description='Is dit document al getokeniseerd?', choices=['ja','nee'],default='nee'),
            extension='nl.txt',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        OutputTemplate('output-fy',PlainTextFormat,'Friese vertaling / Fryske oersetting',
            SetMetaField('encoding','utf-8'),
            SetMetaField('language','fy'),
            removeextension='.nl.txt',
            extension='fy.txt',
            multi=True
        ),
    )

]


# ======== COMMAND ===========

#The system command. It is recommended you set this to small wrapper
#script around your actual system. Full shell syntax is supported. Using
#absolute paths is preferred. The current working directory will be
#set to the project directory.
#
#You can make use of the following special variables,
#which will be automatically set by CLAM:
#     $INPUTDIRECTORY  - The directory where input files are uploaded.
#     $OUTPUTDIRECTORY - The directory where the system should output
#                        its output files.
#     $STATUSFILE      - Filename of the .status file where the system
#                        should output status messages.
#     $DATAFILE        - Filename of the clam.xml file describing the
#                        system and chosen configuration.
#     $USERNAME        - The username of the currently logged in userassociative creed
#                        (set to "anonymous" if there is none)
#     $PARAMETERS      - List of chosen parameters, using the specified flags
#
COMMAND = BASEDIR + "/oersetter_wrapper.py $DATAFILE $STATUSFILE $OUTPUTDIRECTORY " + MTSYSTEM_NLFY_HOST + ' ' + str(MTSYSTEM_NLFY_PORT) + ' ' + MTSYSTEM_FYNL_HOST + ' ' + str(MTSYSTEM_FYNL_PORT)

# ======== PARAMETER DEFINITIONS ===========

#The parameters are subdivided into several groups. In the form of a list of (groupname, parameters) tuples. The parameters are a list of instances from common/parameters.py

PARAMETERS =  [
    #('Group title', [
        #BooleanParameter(id='createlexicon',name='Create Lexicon',description='Generate a separate overall lexicon?'),
        #ChoiceParameter(id='casesensitive',name='Case Sensitivity',description='Enable case sensitive behaviour?', choices=['yes','no'],default='no'),
        #StringParameter(id='author',name='Author',description='Sign output metadata with the specified author name',maxlength=255),
    #] )
]



# ======== DISPATCHING (ADVANCED! YOU CAN SAFELY SKIP THIS!) ========

#The dispatcher to use (defaults to clamdispatcher.py), you almost never want to change this
#DISPATCHER = 'clamdispatcher.py'

#Run background process on a remote host? Then set the following (leave the lambda in):
#REMOTEHOST = lambda: return 'some.remote.host'
#REMOTEUSER = 'username'

#For this to work, the user under which CLAM runs must have (passwordless) ssh access (use ssh keys) to the remote host using the specified username (ssh REMOTEUSER@REMOTEHOST)
#Moreover, both systems must have access to the same filesystem (ROOT) under the same mountpoint.
