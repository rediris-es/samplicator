#!/usr/bin/python
#
# create a configfile for samplicator)

import os
import time
import sys
import argparse
import ConfigParser
import re
import json

## vars
config="rules.ini"
debug =True
nodebug=False

## functions

def dodebug(line):
   """ simple debug funtion """
   if debug == True:
        print "DEBUG " + line

## start code
#
# Check the arguments
parser = argparse.ArgumentParser(description='Create config files for samplicator.')
parser.add_argument('--config','-C',help='Config file,(defaults to ' + config + ')')
parser.add_argument('--debug','-D',help='set the debug flag',action='store_true')
parser.add_argument('--nodebug','-ND',help='unset the debug flag',dest='nodebug',action='store_true')

args = parser.parse_args()
if (args.config):
        config = args.config

# Load of the configuration file
if os.path.exists(config):
    Config = ConfigParser.ConfigParser()
    Config.read(config) 
    dodebug  ("Config file " + config + " read" )
else:
    print "Error can't read config file " + config
    print "Try using --config configfile to especify the config file"
    sys.exit("Error")

# OK test the file / debug 

for section in ['sources', 'destinations']:
    for src in Config.options(section):
        value = Config.get(section,src) 
        dodebug(" section " + section + " key = " + src + " value " + value)
        pattern =re.compile(r'\]')
        if (pattern.search(value)):
            dodebug( "Has a component value")
            list= json.loads(value) 
            for val in list:
                dodebug( val )


# file generation

sections = Config.sections()

ctlfile = Config.get('main','config_dir') + Config.get('main','samplicatectl_file')
pidbase = Config.get('main','pidbase') 
debugval = Config.get('main','debug')

pattern = re.compile(r'rule')
pattern2 = re.compile(r'rule ')
dodebug("Launchctl file is " + ctlfile )
dodebug("NOW running" ) 

outputctl = open(ctlfile,"wb")
outputctl.write ("address,port,debugval,pid_file,config_file\n")

for sec in sections:
      if pattern.search(sec):
          dodebug( "section " + sec + " is a rule/config file section")
          port = Config.get(sec,'port') 
          address = Config.get(sec,'address')
          filename= pattern2.sub('',sec)
          dodebug('Filename is ' + filename)
          pidfile = pidbase + filename
          file=  Config.get('main','config_dir') +  Config.get(sec,'file')
          dodebug( "File to be written is " + file)
          dodebug( "rules are " +  Config.get(sec,'rules'))
          rules = json.loads (Config.get(sec,'rules')) 
          output = open (file,'wb')
          output.write( "#section: " + sec + "\n" )
          for rul in rules:
              output.write("# rule: " + rul+ "\n" )
              source , destination = rul.split(":",1) 
              for src_key in json.loads(Config.get("sources",source)):
                  for dst_key in json.loads(Config.get("destinations",destination)):
                      output.write(src_key + ": " + dst_key + "\n") 
          output.close 
          outputctl.write(address+ "," + port + "," + debugval+ "," + pidfile + "," + file + "\n" )

outputctl.close 

    


