#!/usr/bin/python3

# -*- coding: utf-8 -*-

# SPDX-License-Identifier: AGPL-3.0-only
#
# Copyright (c) 2021 Patrick Dung

from __future__ import unicode_literals
import os
from configparser import ConfigParser

import sys
sys.path.insert(0, "/path-to/pelican_cdn_sri")

from cdn_sri_module import query_cdn_api

inifile='cdn-config.ini'
output_file='cdn_sri_pelicanconf.py'

# clear and create an emtpy setting file
try:
  file = open(output_file, "w+")
  file.close()
except:
  raise

def read_Config_Ini(section):
  try:
    filename=(os.path.dirname(__file__)+'/'+inifile)
    #print (filename)
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    ##parser.read("cdn-config.ini")

    # get sections data
    cdn_parameters = {} 
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
          cdn_parameters[param[0]] = param[1]
        return cdn_parameters
  except:
    raise Exception('Section {0} not found in the {1} file'.format(section, inifile))

def read_All_Config_Ini():
    try:
      filename=(os.path.dirname(__file__)+'/'+inifile)
      parser = ConfigParser()
      parser.read(filename)
      global CDN_SRI
      CDN_SRI=(as_dict(parser))
      #print ("DEBUG", CDN_SRI)
    except:
      raise Exception('problem reading all sections for ini config')

def as_dict(config):
    # https://stackoverflow.com/questions/1773793/convert-configparser-items-to-dictionary
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """
    the_dict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            the_dict[section][key] = val
    return the_dict

def update_setting_file (content):
    try:
        file = open(output_file, "a+")
        file.write(content)
        file.write('\n')
        file.close()
    except:
        raise

def search_files_in_dict (dict1, search_item_name):
  for i in dict1['files']:
    if i['name'] == search_item_name:
      return i

def get_cdn_sri_result():
  read_All_Config_Ini()
  #print (CDN_SRI)
    
  cdn_result = query_cdn_api(CDN_SRI)
  #print("DEBUG 9", cdn_result)

  return (cdn_result)

def transform_to_pelican_settings(cdn_result):
  for k,v in cdn_result.items():
    #print ("DEBUG10", k,v)
    update_setting_file ('CDNSRI_'+str(k).upper().replace("-","_").replace(".","_") +"='"+ v +"'")

cdn_result=get_cdn_sri_result()
if (cdn_result):
  update_setting_file ('CDN_SRI = True')
  transform_to_pelican_settings(cdn_result)
