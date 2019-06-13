#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PacketStorm information
#   Based on Vulners
#
# Software is free software released under the "Modified BSD license"
#
# Copyright (c) 2017 	Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Sources
SOURCE_NAME = 'packetstorm'
SOURCE_FILE = "https://vulners.com/api/v3/archive/collection/?type=packetstorm&api_key={}"

# Imports
import json

from collections import defaultdict

from lib.Config import Configuration as conf
from lib.Source import Source

def add_if(_, entry, item, name=None):
    if not name: name=item
    if entry.get(item): _[name] = entry[item]

def clean_date(_, item):
    if _.get(item): _[item] = _[item].split('T')[0]

class PacketStorm(Source):
    def __init__(self):
        self.name = SOURCE_NAME
        self.cves = defaultdict(list)

        source_file = SOURCE_FILE.format(conf.readSetting("vulners", "api_key", ""))

        _file, r = conf.getFeedData(SOURCE_NAME, source_file)
        data = json.loads(str(_file.read(), 'utf-8'))
        for entry in data:
            ps = {}
            source = entry['_source']
            add_if(ps, source, 'published')
            add_if(ps, source, 'lastseen', 'last seen')
            add_if(ps, source, 'id')
            add_if(ps, source, 'title')
            add_if(ps, source, 'description')
            add_if(ps, source, 'references')
            add_if(ps, source, 'reporter')
            add_if(ps, source, 'href', 'source')
            add_if(ps, source, 'sourceHref', 'data source')

            for date in ['published', 'last seen']: clean_date(ps, date)
            if ps:
                for CVE in source['cvelist']: self.cves[CVE].append(ps)

    def getSearchables(self):
        return ['id', 'reporter']
