#!/usr/bin/env python
# Created By: Wheeler Gans

import argparse
import glob
import subprocess
import os
from time import sleep



if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description='flash-bootloader arguments:'
  )
  parser.add_argument(
    '--device', '-d', dest='device',
    help='usb tty device'
  )
  args = parser.parse_args()

  script_dir = os.path.dirname(os.path.realpath(__file__))

  device = args.device
  if not device:
    dev_list = glob.glob("/dev/tty.usbserial*")
    if len(dev_list):
      device = dev_list[0]
      if len(dev_list) > 1:
        print("\n\033[33mWarning more than 1 usb serial device found. uploading to:" + device + "\033[0m")

  if not device:
    print("\n\033[31mNo device specified or found!\033[0m")
    sleep(20)
    exit(1)

  hex_file = os.path.realpath( glob.glob('{0}/dat/*.hex'.format(script_dir ) )[0] )
  if not hex_file:
    print("\n\033[31mNo hex file found!\033[0m")
    sleep(20)
    exit(1)

  eep_file = os.path.realpath( glob.glob('{0}/dat/*.eep'.format(script_dir ) )[0] )
  if not eep_file:
    print("\n\033[31mNo eep file found!\033[0m")
    sleep(20)
    exit(1)

  conf_file = os.path.realpath(glob.glob('{0}/dat/avrdude.conf'.format(script_dir))[0])
  if not conf_file:
    print("\n\033[31mNo conf file found!\033[0m")
    sleep(20)
    exit(1)

  args_file = os.path.realpath( glob.glob('{0}/dat/*avrdude_args'.format(script_dir) )[0] )
  with open(args_file) as f:
    args = f.readlines()
  args = [ arg.strip() for arg in args ]
  if not args:
    print("\n\033[31mNo args file found!\033[0m")
    sleep(20)
    exit(1)

  print("\n\033[34mUploading to\033[1;36m " + device + "\033[0m")
  print("\t\033[36m" + os.path.basename( hex_file ) + "\033[0m")
  print("\t\033[36m" + os.path.basename( eep_file ) + "\033[0m")

  arg_list = []
  arg_list.append( str("-P" + device) )
  arg_list.append( str("-U" + hex_file) )
  arg_list.append( str("-U" + eep_file) )
  arg_list.append( str("-C" + conf_file) )


  for arg in args:
    if arg.startswith('-U'): continue
    if arg.startswith('-P'): continue
    if arg.startswith('-C'): continue
    if arg.startswith('-v'): continue
    if arg.startswith('AVRDUDE'): continue
    arg_list.append(arg)

  arg_list.insert( 0, "{0}/bin/avrdude".format(script_dir) )

  p = subprocess.Popen(arg_list, bufsize=1, universal_newlines=True, stdout=subprocess.PIPE)
  try:
    p.wait()
    assert p.returncode == 0
    print("\033[32mUpload succeeded\033[0m")
    sleep(4)
    exit(0)
  except Exception as err:
    print( "\033[31mUpload FAILED!\033[0m" )
    p.kill()
    print( "\033[31m", err, "\033[0m" )
    sleep(20)
    exit(1)





avrdude -c avrispmkii -p m644p -P usb48 -B 8 -u -e -U lock:w:0x3F:m -v
avrdude -c avrispmkii -p m644p -P usb48 -v
avrdude -c avrispmkii -p m644p -P usb48 -u -U efuse:w:0xFD:m -v
avrdude -c avrispmkii -p m644p -P usb48 -u -U hfuse:w:0xDC:m -v
avrdude -c avrispmkii -p m644p -P usb48 -u -U lfuse:w:0xFF:m -v
avrdude -c avrispmkii -p m644p -P usb48 -U flash:w:ATmegaBOOT_644P.hex -v
avrdude -c avrispmkii -p m644p -P usb48 -U lock:w:0x0F:m -v