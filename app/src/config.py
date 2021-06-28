import os,sys,getopt
import urllib.request
import time
from random import shuffle
from random import choice
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request



class BIdentifyConfig:

    optionVerbose = True
    ROOTSERVER = False
    ROOTSERVERLIST = "https://raw.githubusercontent.com/jerryhopper/bidentify-definitions/master/data/servers.list"
    LOCALAPPDATA = "/downloads"

    def __init__(self):
        if not os.path.exists( "/downloads" ):
            raise OSError ("/downloads directory doesnt exist")
        #print("(BIdentifyConfig) init: set verbosity to: False")
        #self.start()

    def start(self):
        #
        # Check if bidentify serverlist exists.
        #
        if not os.path.exists( os.path.join( self.LOCALAPPDATA,"servers.list")):
            if self.optionVerbose : print("servers.list does not exist!")
            # Grab the initial serverlist from github!
            self.getInitialRootservers()


        FiveDays = (3600*24)*5
        OneDay = 3600*24
        OneHour = 3600
        current_time = time.time()
        #
        # If serverlist is too old, update it from github!
        #
        modTimesinceEpoc = os.path.getmtime(os.path.join( self.LOCALAPPDATA,"servers.list"))
        modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
        #print("servers.list modificationTime: "+modificationTime)
        if (current_time-modTimesinceEpoc) > FiveDays :
            if self.optionVerbose : print("Servers.list was older than five days : ", modificationTime )
            self.getInitialRootservers()

        #
        # get the available bidentify rootservers
        #

        self.ROOTSERVERS = self.readServers()

        #
        # Select the bidentify rootserver
        #
        self.ROOTSERVER = choice(self.ROOTSERVERS)
        teller = 0
        while not self.getServerStatus(self.ROOTSERVER):
            self.ROOTSERVER = choice(self.ROOTSERVERS)
            if self.optionVerbose : print("Finding optimal server... (Trying: "+self.ROOTSERVER+")")
            teller=teller+1
            if teller>3:
                time.sleep(1.4)

        if self.optionVerbose : print("Initial Rootservers set!")
        if self.optionVerbose : print(self.ROOTSERVER)







    def getServer(self):
        return self.ROOTSERVER



    def getServerStatus(self,rootServer):
        try:
            response = urllib.request.urlopen( rootServer +"/api/status")
            response_status = response.status # 200, 301, etc
        except HTTPError as error:
            response_status = error.code # 404, 500, etc
            if self.optionVerbose : print("Error: "+self.ROOTSERVER+" returned "+str(response_status))
            return False
        except URLError as error:
            if self.optionVerbose : print("Error: "+self.ROOTSERVER+" "+str(error))
            return False
            sys.exit()
        return True

    def readServers(self):
        #print("readServers")
        # Grab the initial serverlist from the rootserver(s)
        serversFile = open(os.path.join( self.LOCALAPPDATA,"servers.list"), 'r')
        serverList = []
        count = 0
        while True:
            count += 1
            # Get next line from file
            server = serversFile.readline()
            # if line is empty
            # end of file is reached
            if not server:
                break
            #print("Server{}: {}".format(count, server.strip()))
            serverList.append( server.strip() )
        serversFile.close()
        # Set variable
        return serverList

    def getInitialRootservers(self):
            print("getInitialRootservers()")
            try:
                urllib.request.urlretrieve( self.ROOTSERVERLIST ,os.path.join( self.LOCALAPPDATA,"servers.list"))
            except ( urllib.error.URLError,urllib.error.HTTPError) as e:
                print (e)
                sys.exit()
            # Grab the initial serverlist from the rootserver(s)
            serversFile = open(os.path.join( self.LOCALAPPDATA,"servers.list"), 'r')
            serverList = []
            count = 0
            while True:
                count += 1
                # Get next line from file
                server = serversFile.readline()
                # if line is empty
                # end of file is reached
                if not server:
                    break
                #print("Server{}: {}".format(count, server.strip()))
                serverList.append( server.strip() )
            serversFile.close()
