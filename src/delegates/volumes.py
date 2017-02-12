#!/usr/bin/python
from util.config import Config

import json
import requests
import getopt
import os
import sys

class Volumes(object):

    def __init__(self,config):
        self.conf = config


    def getVolumes(self):
        url = self.conf.getURL()+"volumes"
        response = requests.get(url, headers=self.conf.getHeaders())
        return response.json()


    def getVolumeByName(self,name):
        url = self.conf.getURL()+"volumes?name="+name
        response = requests.get(url, headers=self.conf.getHeaders())
        #data = response.json()
        #print "getVolumeByName returned: %s" % data
        #for v in data['volumes']:
        #    print "id: %s name:%s description:%s" % (v['id'],v['name'],v['description'])
        return response.json()

    def getVolumeCount(self):
        data = self.getVolumes()
        numVolumes = int(data['meta']['total'])
        if numVolumes == 0:
            print "No volumes."
            return 0
        else:
            return numVolumes

    # Attach volume to the droplet.
    # volume - the volume object from DigitalOcean
    # droplet - the droplet object from DigitalOcean
    def attachVolumeToDroplet(self,volume,droplet):
        volumeId = volume['id']
        dropletId = droplet['id']
        region = volume['slug']
        url=self.conf.getURL()+"volumes/"+volumeId+"/actions"

        actionObj = {
            "type": "",
            "droplet_id": droplet_Id,
            "region": droplet['region']
        }
