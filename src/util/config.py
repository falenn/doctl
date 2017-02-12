#!/usr/bin/python
import yaml
import os

class Config(object):

    # class constructor.  First parameter is the refernce to the object - always
    # true with class methods as the first param is a pointer to the object itself
    def __init__(self,configFile):
        # Load configs
        with open(configFile, 'r') as f:
            self.config = yaml.load(f)

        # global vars
        # Load token from envrinment
        self.DIGITALOCEAN_TOKEN="Bearer " + os.environ['DIGITALOCEAN_TOKEN']
        self.DIGITALOCEAN_URL = self.config["deployment"]["api"]["url"]
        self.headers =  {"Content-Type": "application/json",
                    "Authorization": self.DIGITALOCEAN_TOKEN
                   }

        #print "DO URL: %s" % self.getURL()
        #print "Headers: %s" % self.getHeaders()


    def getToken(self):
        return self.DIGITALOCEAN_TOKEN

    def getURL(self):
        return self.DIGITALOCEAN_URL

    def getHeaders(self):
        return self.headers

    # return the entire config object
    def getConfig(self):
        return self.config
