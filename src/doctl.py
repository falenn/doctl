#!/usr/bin/python
#from importlib import import_module
from util.config import Config
from delegates.volumes import Volumes
from delegates.droplets import Droplets
from delegates.networking import Networking
import getopt
import sys
import json
import time

configFile = "config.yml"

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    print "in the main"
    if argv is None:
        argv = sys.argv
        options, remainder = getopt.getopt(argv[1:], 'f:',['file='])
        print "OPTIONS: ", options
    try:
        try:
            for opt, arg in options:
                if opt in ('-f', '--file'):
                    configFile = arg

        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    print "Config File: ", configFile

    # --------- My code
    # This is the main driver...
    # instantiate config
    conf = Config(configFile)

    # instantiate delegates passing in config.  Perhaps a better way to do this?
    vol = Volumes(conf)
    drop = Droplets(conf)
    net = Networking(conf)
    print "Using DigitalOcean Token: %s" % conf.getToken()
    print "Using DigitalOcean URL: %s" % conf.getURL()
    print "Entire deployment config: %s" % conf.getConfig()

    #droplets = drop.getDroplets()
    #print "Found droplets: "
    #for d in droplets['droplets']:
#        print "Droplet: %s" % d
        #print "%s\t%s\t%s\t%s\t%s\t%s" % (d['id'], d['name'], d['image']['distribution'], d['status'], d['size_slug'], d['tags'])

    minecraftDroplets = drop.getDropletsByTag("minecraft")
    print "Found minecraft droplets: "
    for d in minecraftDroplets['droplets']:
        print "%s\t%s\t%s\t%s\t%s\t%s" % (d['id'], d['name'], d['image']['distribution'], d['status'], d['size_slug'], d['tags'])



    vols = vol.getVolumes()
    #print "Found volumes: %s" % vols
    for v in vols['volumes']:
        volume = vol.getVolumeByName(v['name'])
        print "Volumes -----"
        print "id: %s name: %s" % (v['id'],v['name'])

    fips = net.getFloatingIPs()
    print "Floating IPs: %s" % fips

    # dropping existing droplet
    status = drop.removeDropletByName(conf.getConfig()['deployment']['droplet']['name'])
    time.sleep(5)
    if status == 204:
        print "creating droplet..."
        droplet = drop.createDropletUnique(conf.getConfig()['deployment']['droplet'])
        while droplet['status'] != "active":
            time.sleep(10)
            droplet = drop.getDropletByName(conf.getConfig()['deployment']['droplet']['name'])
        print "Assigning Floating IP..."
    fip = net.getAvailableFloatingIPbyIP(conf.getConfig()['deployment']['networking']['floating_ip'])
    if bool(fip):
        net.assignFloatingIPbyIPtoDroplet(conf.getConfig()['deployment']['networking']['floating_ip'],droplet)
    else:
        print "Not continuing.  See why droplet was not deleted."



if __name__ == "__main__":
    sys.exit(main())
