# -*- coding: utf-8 -*-
import time
import argparse
from watchdog.observers import Observer
from py.sync.sync import MyHandler

def main():
    """
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source",help="The source directory", default=None)
    parser.add_argument("-t", "--target",help="The target directory", default=None)
    parser.add_argument("--local",  help="Mirror local directorys", action="store_true")

    args = parser.parse_args()

    if args.local:
        if args.target != None:
                source_path = args.source
                target_path = args.target

                event_handler = MyHandler(source_path=source_path, target_path=target_path)
                observer = Observer()
                observer.schedule(event_handler, path=source_path, recursive=True)
                observer.start()

                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    observer.stop()
                observer.join()

        else:
            raise RuntimeError("No Target set!")
