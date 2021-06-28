
import os,sys,time

from transmission_rpc import Client
import urllib.request, json




class Update:

    host = "transmission"

    port = 9091
    usern = "username"
    passw = "password"

    def __init__(self):
        self.DATAPATH="/downloads"
        self.TORRENTSPATH="/torrents"
        self.SERVER= "http://bidentify.jerryhopper.com"


    def seedTorrent( self,dataObject ):
       fileid = dataObject['id']
       filename = dataObject['filename']
       filehash = dataObject['filehash']
       section = dataObject['section'].replace("arma2_oa","arma2oa")
       game = dataObject['game'].replace("arma2_oa","arma2oa")

       theDownloadFolder = os.path.join( self.DATAPATH , game+os.path.sep+section )
       saveloc =  os.path.join( theDownloadFolder, dataObject['filename'] )

       theTorrent = self.TORRENTSPATH+"/"+filehash+".torrent"

       if os.path.exists( os.path.join(theDownloadFolder,filename) ) :
            print("(Update) seedTorrent: The file exists.")

       if os.path.exists( theTorrent  ) :
            print("(Update) seedTorrent: The torrent exists.")

       #hashlist = getHashesList()
       #for item in hashlist:
       #info = getHashInfo(item)
       #filePath = info['filePath'].split("\\")
       #theTorrent = os.path.join(TORRENTSPATH,item+".torrent")
       #theDownloadFolder = os.path.join(DATAPATH,filePath[0],filePath[1])
       #if os.path.exists(os.path.join(DATAPATH,filePath[0],filePath[1],info['fileName'])) :
       print("(Update) seedtorrent: ", theTorrent,theDownloadFolder)
       try:
           #filemirror = nodeTorrent("transmissions",9091,"username","password")
           #filemirror.seedTorrent(theTorrent ,theDownloadFolder)

           c = Client(host=self.host, port=self.port, username=self.usern, password=self.passw)
           c.add_torrent(theTorrent, download_dir=theDownloadFolder)


       except:
           e = sys.exc_info()[0]
           print( e )
           print(sys.exc_info()[1])
       return True


    def markFileCompleted(self,dataObject):
       fileid = dataObject['id']
       filehash = dataObject['filehash']
       with urllib.request.urlopen(self.SERVER+"/api/node/complete/"+fileid) as url:
              data = json.loads(url.read().decode())
       return data

    def getUpdatesList(self):

       with urllib.request.urlopen(self.SERVER+"/api/node/updates.list") as url:
           data = json.loads(url.read().decode())
       return data

    def getFileInfo(self,id):
        with urllib.request.urlopen(self.SERVER+"/api/node/file/"+id) as url:
               data = json.loads(url.read().decode())
        return data

    def downloadTorrent(self,dataObject):
        print("(Update) downloadTorrent ")
        print(dataObject)
        fileid = dataObject['id']
        filehash = dataObject['filehash']

        download = self.SERVER+"/api/torrent/"+filehash

        saveloc = self.TORRENTSPATH+"/"+filehash+".torrent"
        print("Downloading... ("+download+","+saveloc+")")

        try:

            urllib.request.urlretrieve( download , saveloc)
        except:
            e = sys.exc_info()
            print( e )

        #except ( urllib.error.URLError,urllib.error.HTTPError) as e:
        #    print (e)
        #    sys.exit()
        print("Downloaded torrent to "+saveloc)
        return os.path.exists(saveloc)

    def download(self,dataObject):
        fileid = dataObject['id']
        filename = dataObject['filename']
        section = dataObject['section'].replace("arma2_oa","arma2oa")
        game = dataObject['game'].replace("arma2_oa","arma2oa")

        savepath = os.path.join( self.DATAPATH , game+os.path.sep+section )
        saveloc =  os.path.join( savepath, dataObject['filename'] )

        #print(self.ROOTSERVER+"/api/servers.list" )
        #print(path)
        download = self.SERVER+"/api/node/download/"+fileid
        print("(Update) download: "+download)
        print("(Update) save to : "+saveloc)
        #print(os.path.exists(savepath) )
        #print(os.path.isdir(savepath) )
        #print(os.path.exists(saveloc) )

        try:
            print("(Update) download: Downloading... ("+download+","+saveloc+")")
            urllib.request.urlretrieve( download , saveloc)
        except:
            print('Error: {}. {}, line: {}'.format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
            e = sys.exc_info()[0]
            print( e )
            #except ( urllib.error.URLError,urllib.error.HTTPError) as e:
            print("ERROR! ")
            print (e)
            sys.exit()
        print("(Update) Downloaded "+filename+" to "+saveloc)
        return os.path.exists(saveloc)

