#!/usr/bin/env python
"""
# Inspired from http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html

create a file for testing like this: 

joshi@joshi-Inspiron:~$ echo "hello">touch.conf

run python program like this:

joshi@joshi-Inspiron:~$ python file_watcher.py /home/joshi/
created /home/joshi/touch.conf
modified /home/joshi/touch.conf

"""

import sys
import time

#import xmltodict
#import magicdate

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class FileSysHandler(PatternMatchingEventHandler):
    patterns=["*.conf"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
	print event.event_type, event.src_path

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(FileSysHandler(), path=args[0] if args else '.', recursive=True)
    observer.start()

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()

