#!/usr/bin/python
from util.config import Config

import json
import requests
import getopt
import os
import sys


class Networking(object):

    def __init__(self,config):
        self.conf = config

    def getFloatingIPs(self):
        print "Getting floating IPs"
        url = self.conf.getURL()+"floating_ips"
        response = requests.get(url, headers=self.conf.getHeaders())
        return response.json()

    def getFloatingIpByIP(self,ip):
        print "Getting floating Ip by ip: %s" % ip
        fips = self.getFloatingIPs()
        if bool(fips):
            if fips['meta']['total'] > 0:
                for fip in fips['floating_ips']:
                    if fip['ip'] == ip:
                        print "found floating_ip: %s" % (fip['ip'])
                        return fip
                    else:
                        print "No matching floating ip found"
                        return {}
            else:
                print "No floating ips returned"
                return {}
        else:
            print "Error with request: %s" % fips
            return {}

    def getAvailableFloatingIPbyIP(self,ip):
        fip = self.getFloatingIpByIP(ip)
        if bool(fip):
            if bool(fip['droplet']):
                print "Floating IP %s already assigned" % ip
            else:
                print "Floating IP %s found" % ip
                return fip
        return {}

    #{
    #  "type": "assign",
    #  "droplet_id": 8219222
    #}
    def assignFloatingIPbyIPtoDroplet(self,ip,droplet):
        fip = self.getAvailableFloatingIPbyIP(ip)
        if bool(fip):
            url = self.conf.getURL()+"floating_ips/"+ip+"/actions"
            body = {}
            body['type'] = "assign"
            print "Droplet assigning ip to: %s" % droplet
            body['droplet_id'] = droplet['id']
            print "sending this body msg: %s" % body
            response = requests.post(url,
                headers=self.conf.getHeaders(),
                data=json.dumps(body))
            if response.status_code == 201:
                print "Floating IP %s assigned to droplet %s" % (ip,droplet['name'])
                return response.json()
            else:
                print "There was a problem assiging the floating ip. %s" % response.json()
                return response.json()
        else:
            print "No free floating ip with ip %s was found." % ip
