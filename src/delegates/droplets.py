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
        for droplet in response['droplets']:
            print "Checking name %s" % droplet['name']
            if droplet['name'] == name:
                print "Found a droplet with name matching: %s - %s" % (name,droplet)
                return droplet
        return {}


    # Given a dropletRequest, will attempt to create a droplet.
    # Return: droplet dict
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
            if response.status_code == 202:
                print "Droplet successfully created."
                droplet = response.json()
                print "About to return this %s" % droplet
                return droplet['droplet']
        except ValueError:
            print "Error with droplet post: %s" % ValueError
            return {}

    def createDropletUnique(self,dropletRequest):
        # create a droplet from the deployment configFile
        #{"name":"example.com","region":"nyc3","size":"512mb","image":"ubuntu-14-04-x64","ssh_keys":null,"backups":false,"ipv6":true,"user_data":null,"private_networking":null,"volumes": null,"tags":["web"]}'
        droplet = self.getDropletByName(dropletRequest['name'])
        # check to see if already deployed
        if bool(droplet):
            print "Droplet with name [%s] already exists." % droplet['name']
            return droplet
        else:
            droplet = self.createDroplet(dropletRequest)
            if bool(droplet):
                print "Droplet creation successful"
                return droplet
            else:
                print "Error with droplet creation."
            return {}


    def removeDropletByName(self,name):
        print "removing droplet by name: %s" % name
        try:
            droplet = self.getDropletByName(name)
            # if something exists here, attempt to continue
            if bool(droplet):
                print "Droplet %s with id %s to be removed." % (name,droplet['id'])
                url = self.conf.getURL()+"droplets/"+str(droplet['id'])
                response = requests.delete(url,
                    headers=self.conf.getHeaders())
                print "response: %s" % response.status_code
                if response.status_code == 204:
                    print "Deletion of droplet %s successful." % droplet['id']
                    return response.status_code
                else:
                    print "There was an issue: %s" % response
                    return response.status_code
            else:
                print "No droplet to remove with name: %s" % name
                return 204
        except(ValueError):
            print "No droplets to remove with name %s %s" % (name,ValueError)
            return 500
