import os,sys,time
from transmission_rpc import Client
from transmission_rpc import TransmissionError
import urllib.request, json

import hashlib


class BIdentifyTorrents:

    optionVerbose = True
    vault = True

    ROOTSERVERLIST = "https://raw.githubusercontent.com/jerryhopper/bidentify-definitions/master/data/servers.list"
    LOCALAPPDATA = "/downloads"
    TORRENTDATA = "/torrents"

    host = "transmission"
    port = 9091
    usern = "username"
    passw = "password"


    def find(self,item):
        #print("(BIdentifyTorrents) find:")
        for torrent in self.loadedTorrents:
            #print(item.name)
            if torrent.name == item['filename']:
                print("match "+torrent.name)
                return item
        #print(item)
        return False
        #sys.exit()

    def __init__(self,server):
        #if self.optionVerbose: print("BIdentifyTorrents")
        if not os.path.exists( "/downloads" ):
            raise OSError ("/downloads directory doesnt exist")
        self.server = server
        #print("(BIdentifyConfig) init: set verbosity to: False")
        #self.start()
        self.torrentClient = Client(host=self.host, port=self.port, username=self.usern, password=self.passw)


        #self.get_torrents_status()
        print("(BIdentifyTorrents) init: Get loaded torrents.")
        print("...")
        self.loadedTorrents = self.torrentClient.get_torrents()
        print("...")
        print("(BIdentifyTorrents) init: "+str(len(self.loadedTorrents))+" torrents loaded." )
        #c = Client(host=self.host, port=self.port, username=self.usern, password=self.passw)
        #c = Client(host=self.host, port=self.port, username=self.usern, password=self.passw)
        #return



        # Download a list with all torrents.
        with urllib.request.urlopen( self.server + "/api/node/alltorrents" ) as url:
           data = json.loads(url.read().decode())
        removeMissing = []

        print("(BIdentifyTorrents) loop through allTorrents")
        for item in data:
            folder = os.path.join(self.LOCALAPPDATA,item['game'],item['section'])
            file = os.path.join(folder,item['filename'])
            if not os.path.exists( folder ) :
                os.makedirs(folder, exist_ok=True)

            # check if there is a hash.
            if "filehash" in item:
                # we know the file has been uploaded to bidentify
                if os.path.exists(file):
                    # we have found the file locally
                    if self.checkLocalTorrentFile(item['filehash']) :
                        # the file and torrentfile exists.
                        #print("File & Torrentfile Exists "+ item['filehash']+".torrent "+ item['filename'] )
                        #found = self.find(item)
                        # check if the file is actually loaded in transmission
                        #if found == False:
                        #    print("Not found")
                        #    self.seedTorrent(os.path.join(self.TORRENTDATA,item['filehash']+".torrent") ,folder)
                        a=1
                        #else:
                        #    print("Yesss")
                        #a=1
                        #self.seedTorrent(os.path.join(self.TORRENTDATA,item['filehash']+".torrent") ,folder)
                    else:
                        print ("(BIdentifyTorrents) __init__ : No local Torrentfile." )
                        print(item['filename'],item['filehash'])
                        self.downloadTorrentFile(item['filehash'])
                        self.seedTorrent(os.path.join(self.TORRENTDATA,item['filehash']+".torrent") ,folder)


                else:
                    #print( "WE ARE MISSING: "+file +" which is known on the server"  )
                    if self.vault:
                        # this is a vault.
                        print("Missing "+item['id'])
                        with urllib.request.urlopen( self.server + "/api/node/removal/"+item['id'] ) as url:
                                   data = json.loads( url.read().decode() )
                                   print(data)
                        # instruct server to remove the filehash
                        removeMissing.append(item['id'])
                    else:
                        a=1
                        # this is just a node
                        # we dont have the file locally, try download it via torrent.
                        #print( "MISSING: "+file )
                        self.downloadTorrentFile(item['filehash'])
                        self.seedTorrent(os.path.join(self.TORRENTDATA,item['filehash']+".torrent") ,folder)

            #else:
            #    print("MISSING ")

        # if vault
        if self.vault:
            #submit missing to be removed
            a=1


        print(removeMissing)



    def md5(self,fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_torrents_status(self):
        tors= self.torrentClient.get_torrents()
        for x in tors:
            torinfo = {}
            torinfo['id']=x.id

            torinfo['name']=x.name
            torinfo['rateUpload']=x.rateUpload
            #torinfo['date_added']=x.date_added
            torinfo['ratio']=x.ratio
            torinfo['status']=x.status
            torinfo['available']=x.available


            torinfo['hash']=self.md5(x.download_dir+"/"+x.name)
            #print(torinfo)
            if x.status == "downloading" or x.status == "download pending":
                #self.torrentClient.remove_torrent(x.id)
                # https://transmission-rpc.readthedocs.io/en/v3.2.6/torrent.html
                #print(x)
                #print(x.name)
                #print(x.status)
                #print(x.progress)
                #print(x.rateDownload)
                #print(x.rateUpload)
                #print(x.date_added)
                #print(x.date_done)
                #print(x.available)
                #print(x.is_finished)
                #print(x.hashString)
                #print(x.is_stalled)
                #print(x.ratio)
                print(x.download_dir+"/"+x.name)


    def checkLocalTorrentFile(self,hash):
        return os.path.exists( os.path.join(self.TORRENTDATA,hash+".torrent") )

    def downloadTorrentFile(self, hash):
        print("download torrentfile "+self.server+"/api/torrent/"+hash+".torrent")
        # http://bidentify.jerryhopper.com/api/torrent/73b4320ab4579c29f815e18ccba662e7
        try:
            urllib.request.urlretrieve( self.server+"/api/torrent/"+hash ,os.path.join( self.TORRENTDATA, hash+".torrent"))
        except ( urllib.error.URLError,urllib.error.HTTPError) as e:
            print (e)
            sys.exit()


    def seedTorrent(self,torrentFile,downloadDir):
       if not os.path.exists(torrentFile):
          print("error, torrent not found.")
          sys.exit()
       if not os.path.exists(downloadDir):
          print("error, download-dir doesnt exist.")
          sys.exit()
       if not os.path.isdir(downloadDir):
          print("error, download-dir isnt a directory")
          sys.exit()

       #x= self.torrentClient.get_torrents()
       #c = Client(host=self.host, port=self.port, username=self.usern, password=self.passw)
       #c = Client(host=self.host, port=self.port, username=self.usern, password=self.passw)
       #print(x[0])
       #print(x[0].status)
       #x[0].progress
       #x[0].rateDownload
       #x[0].rateUpload
       #x[0].date_added
       #x[0].date_done
       #x[0].available
       #x[0].is_finished#



       #print("tor: "+torrentFile)
       try:
           self.torrentClient.add_torrent(torrentFile, download_dir=downloadDir)
       except TransmissionError as E :
           print (E.message)



    def item(self,data):
        data['id']
        data['filehash']
        data['filename']
        data['game']
        data['section']



