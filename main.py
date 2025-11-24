import shutil
import os
import sys
import sched
import time
import hashlib
import datetime as dt
import argparse
from pathlib import Path

class Synchroniser:
    '''class to maintain a replica'''

    def __init__(self, source,
                 replica, interval, runs,
                 log):
        #initialise
        self.source = source
        self.replica = replica
        self.interval = interval
        self.runs = runs
        self.log = log

        #init dict {relative_path:hash}
        self.hash_dict = {}

    def run(self):
        '''schedule the syncs and run them'''

        #init the scheduler
        my_scheduler = sched.scheduler(time.time, time.sleep)

        #get current time
        start = time.time()

        #schedule the syncs
        for i in range(self.runs):
            #set runtime
            runtime = start+i*self.interval

            my_scheduler.enterabs(
                    runtime,
                    0, #priority
                    self.sync_folder,
                    argument = (self.source,))

        #run the syncs
        #this program is single-threaded in accordance with the spec
        my_scheduler.run()

    def sync_folder(self, folder_path):
        '''perform a sync'''

        #get current list of files
        src_file_list = [entry for entry in os.listdir(folder_path)
                         if os.path.isfile(
                             os.path.join(folder_path,entry))]


        #update or create files
        for filename in src_file_list:
            old_hash = self.hash_dict.get(filename)
            new_hash = self.get_hash(filename)

            #create new files
            if old_hash is None:
                self.create_file(filename)

            #update edited files
            if old_hash != new_hash:
                self.update_file(filename)

            self.hash_dict[filename] = new_hash

        #delete missing files
        for filename in self.hash_dict.keys():
            if filename not in src_file_list:
                self.delete_file(filename)

    def get_hash(self, path_to_file):
        '''get hash given name of file in source'''

        #create the path to the file
        abs_path = os.path.join(self.source, path_to_file)

        #read the file and hash it
        with open(abs_path, "rb") as file:
            contents = file.read()
            md5_of_file = hashlib.md5(contents).hexdigest()

        return md5_of_file

    def create_file(self, file_to_create):
        '''create a file'''

        self.make_copy(file_to_create)
        self.make_log("created", file_to_create)

    def update_file(self, file_to_update):
        '''update a file'''

        self.make_copy(file_to_update)
        self.make_log("updated", file_to_update)

    def make_copy(self, file_to_copy):
        '''make a copy of a file from source to replica'''

        #create the path
        path_to_file = os.path.join(self.source,file_to_copy)

        #create destination
        dest_path = os.path.join(self.replica,file_to_copy)

        #copy the file (copy2 preserves metadata)
        shutil.copy2(path_to_file, dest_path)

    def delete_file(self, file_to_delete):
        '''delete a file from replica that is no longer in source'''

        #create path
        path_to_file = os.path.join(self.replica, file_to_delete)

        #os can remove files and empty directories (rmdir)
        #remove directories with shutil.rmtree()
        try:
            os.remove(path_to_file)


        except FileNotFoundError:
            #nothing to do as the file isn't there
            pass

        self.hash_dict.pop(file_to_delete, None)

        #log the deletion
        self.make_log("deleted", file_to_delete)

    def make_log(self, action, filename):
        '''makes a log of the action'''

        #generate the timestamp
        timestamp = dt.datetime.now().replace(
                microsecond=0
                ).isoformat()

        #generate path
        path_to_file = os.path.join(self.source,filename)

        #make the log string
        log = "\t".join((timestamp,path_to_file,action))

        #add log to logfile
        with open(self.log, "a") as log_file:
            log_file.write(log+"\n")

        #print log to console
        print(log)

########################################################
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("replica", type=Path)
    parser.add_argument("interval", type=int)
    parser.add_argument("runs", type=int)
    parser.add_argument("log_file", type=Path)

    args = parser.parse_args()


    app = Synchroniser(args.source, args.replica, args.interval,
                       args.runs, args.log_file)


    app.run()

if __name__ == "__main__":
    main()

