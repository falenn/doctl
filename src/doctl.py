#!/usr/bin/python
#from importlib import import_module
from util.config import Config
from delegates.volumes import Volumes
from delegates.droplets import Droplets
import getopt
import sys
import json

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

    dfd = drop.createDropletUnique(conf.getConfig()['deployment']['droplet'])
    print "droplet status: %s" % dfd['status']




if __name__ == "__main__":
    sys.exit(main())
