#!/usr/bin/python
from util.config import Config

import json
import requests
import getopt
import os
import sys


class Droplets(object):

    def __init__(self,config):
        self.conf = config

    def getDroplets(self):
        url = self.conf.getURL()+"droplets"
        response = requests.get(url, headers=self.conf.getHeaders())
        return response.json()

    def getDropletsByTag(self,tag):
        url = self.conf.getURL()+"droplets?tag_name="+tag
        response = requests.get(url, headers=self.conf.getHeaders())
        return response.json()

    def getDropletByName(self,name):
        print "Looking for droplet with name: %s" % name
        response = self.getDroplets()
        print "Looking through %d droplets" % len(response['droplets'])
        for d in response['droplets']:
            print "Checking name %s" % d['name']
            if d['name'] == name:
                print "Found a droplet with name matching: %s" % name
                return d
        return []



    def createDroplet(self,dropletRequest):
        #"https://api.digitalocean.com/v2/droplets"
        url = self.conf.getURL()+"droplets"
        print "Creating droplet with this JSON post: %s" % dropletRequest
        try:
            body = dropletRequest
            if isinstance(dropletRequest,dict):
                body = json.dumps(dropletRequest)
            response = requests.post(url,
                headers=self.conf.getHeaders(),
                data=body)
            print "response: %s" % response.status_code
            #if response.status_code == 202:
            #data = json.loads(response.text)
            return response.json()
        except ValueError:
            print "Error with droplet post: %s" % ValueError

    def createDropletUnique(self,dropletRequest):
        # create a droplet from the deployment configFile
        #{"name":"example.com","region":"nyc3","size":"512mb","image":"ubuntu-14-04-x64","ssh_keys":null,"backups":false,"ipv6":true,"user_data":null,"private_networking":null,"volumes": null,"tags":["web"]}'
        dfd = self.getDropletByName(dropletRequest['name'])
        # check to see if already deployed
        if len(dfd) < 1:
            response = self.createDroplet(dropletRequest)
            print "Droplet creation response: %s" % response
            return response
        else:
            print "Droplet with name [%s] already exists." % dfd['name']
            return dfd
