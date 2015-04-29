#!/usr/bin/env python

import os, sys, time, subprocess
import logging
import ConfigParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG)
global host, post, user, pwd, target, path
def log(s):
   logging.info('[Monitor] %s' % s)

class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.upload_file = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('changeType = ' + event.event_type + '; FileName = '+event.src_path)
            self.upload_file()

def start_process():
    global process, command
    log('Start process %s...' % ' '.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


# upload the file to server
def upload_file():
    print "upload_file"
    cmd = "rsync  -avz %s %s@%s:%s" % (path, user, host, target)
    print cmd
    runCmd(cmd)

def runCmd(cmd):
     os.system(cmd)
 

def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHander(upload_file), path, recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    # start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    argv = sys.argv
    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)
    if argv[0]!='python':
        argv.insert(0, 'python')
    command = argv
    print len(argv)
    if len(argv)<=2:
        config_file_path = "./config.ini"
    else: 
        config_file_path = argv[2]

    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)


    host = cf.get("baseconf", "host")
    port = cf.getint("baseconf", "port")
    user = cf.get("baseconf", "user")
    target = cf.get("baseconf","target")
    path = cf.get("baseconf","path")

    start_watch(path, None)