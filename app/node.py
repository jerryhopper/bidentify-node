import os,sys,time

class Node:
    rootserver = "bidentify.jerryhopper.com"
    uploadStamp = 0
    rootserverStamp = 0
    alltorrentsStamp = 0

    def start(self):
        a=1
        key = 'HOME'
        value = os.getenv(key)
        #self.loop()

    def loop(self):
        while True:
            try:
                self.checkForRootservers()
            except:
                a=1
            try:
                self.checkAllTorrents()
            except:
                a=1
            try:
                self.checkForUpload()
            except:
                a=1
            time.sleep(2)

    def current_time(self):
        return int(time.time())

    def checkForUpload(self):
        if self.uploadStamp < self.current_time() + 300:
            sys.stdout.write('checkForUpload\n')
            a=1
            self.uploadStamp = self.current_time()

    def checkForRootservers(self):
        if self.rootserverStamp < self.current_time() + 3600*164:
            sys.stdout.write('checkForRootservers\n')
            print(current_time)
            self.rootserverStamp=self.current_time()
        a=1
    def checkAllTorrents(self):
        if self.alltorrentsStamp < self.current_time() + 3600*2:
            sys.stdout.write('checkAllTorrents\n')
            a=1
            self.alltorrentsStamp=self.current_time()


sys.stdout.write('Start! \n')
time.sleep(5)
while True:
    try:
        #sys.stderr.write(':)\n')
        sys.stdout.write(':)\n')
        instance = Node()
        instance.start()
        time.sleep(5)
    except:
       #print("Fatal error!")
       sys.stderr.write('Fatal error!\n')
       time.sleep(3600/4)
       pass
