import os,sys,time
from src.updates import Update

class CheckForUploads:



    def __init__(self,server):
        self.server = server

    def start(self):
        #
        print("Update")
        #print(getUpdatesList())
        try :
            Updater = Update()
            updates = Updater.getUpdatesList()
            for update in updates:
                print(update)
                print("get information about file")
                # server/HASH

                print("(CheckForUploads) start: Get fileinfo")
                try:
                    fileInfo = Updater.getFileInfo(update)
                    #print(fileInfo)
                except:
                    e = sys.exc_info()[0]
                    print( e )
                    print("A update failed....  (Updater.getFileInfo)")
                    time.sleep(5)

                print("(CheckForUploads) start: Download file")
                try:
                    Updater.download(fileInfo)
                except:
                    print("A update failed....  (Updater.download)")
                    e = sys.exc_info()[0]
                    print( e )
                    #print(fileInfo)

                print("(CheckForUploads) start: Download torrent")
                try:
                    Updater.downloadTorrent(fileInfo)
                    #print(saveloc)
                    #sys.exit()
                except:
                    e = sys.exc_info()
                    print( e )
                    print("A update failed....  (Updater.downloadTorrent)")
                    time.sleep(5)

                print("(CheckForUploads) start: seedTorrent")
                try:
                    print("(Updater.seedTorrent) seedTorrent")
                    Updater.seedTorrent(fileInfo)

                except:
                    print("A update failed....  (Updater.seedTorrent)")
                    e = sys.exc_info()[0]
                    print( e )
                    time.sleep(5)
                    #pass

                print("(CheckForUploads) start: Mark completed")
                try:
                    print("(Updater.seedTorrent) markFileCompleted")
                    Updater.markFileCompleted(fileInfo)
                except:
                    print("A update failed....  (Updater.seedTorrent)")
                    e = sys.exc_info()[0]
                    print( e )
                    time.sleep(3)

            print("Sleeping")
        except :
            print("FATAL! .... .. .")
            print(sys.exc_info())
            sys.exit()
            e = sys.exc_info()[0]
            print( e )
            time.sleep(10)
            pass
