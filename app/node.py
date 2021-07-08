import os,sys,time

from src.config import BIdentifyConfig
from src.checktorrents import BIdentifyTorrents
from src.CheckForUploads import CheckForUploads
from src.updates import Update


class Node:

    uploadStamp = 0
    rootserverStamp = 0
    alltorrentsStamp = 0

    def start(self):
        self.config = BIdentifyConfig()
        key = 'HOME'
        value = os.getenv(key)
        self.loop()

    def loop(self):
        while True:
            try:
                self.checkForRootservers()
            except:
                a=1
            #try:
            self.checkForUpload()
            #except:
            #    a=1
            #try:
            self.checkAllTorrents()
            #    #except:
            #    #    a=1

            time.sleep(2)

    def current_time(self):
        return int(time.time())

    def checkForUpload(self):
        if self.uploadStamp < (self.current_time() - 30):
            sys.stdout.write('checkForUpload\n')
            checkUploads = CheckForUploads(self.config.getServer())
            checkUploads.start()
            self.uploadStamp = self.current_time()

    def checkForRootservers(self):
        if self.rootserverStamp < (self.current_time() - 3600):
            sys.stdout.write('checkForRootservers\n')
            self.config.start()
            #self.config.getServer()
            self.rootserverStamp=self.current_time()

    def checkAllTorrents(self):
        if self.alltorrentsStamp < (self.current_time() - (3600*48)):
            sys.stdout.write(str(self.alltorrentsStamp)+' checkAllTorrents------------------\n')
            checktorrent = BIdentifyTorrents( self.config.getServer() )
            self.alltorrentsStamp=self.current_time()
            print("Done!")
            #sys.exit()



sys.stdout.write('Start! \n')
instance = Node()
while True:
    try:
        #sys.stderr.write(':)\n')
        sys.stdout.write(':)\n')

        instance.start()
        time.sleep(60)
    except Exception as inst:
       print(type(inst))
       print(inst.args)
       print(inst)
       #print("Fatal error!")
       sys.stderr.write('Fatal error!\n')
       #time.sleep(3600/4)
       time.sleep(5)
       pass
       #exit()
