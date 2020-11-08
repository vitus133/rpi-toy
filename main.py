from multiprocessing import Process, Queue, Event
from pathlib import Path
import time
import json
import pickle
import secrets

import os
import sys

from cmd_server import run_server
from logger import Logger


class RobotServer(Logger):
    def __init__(self, notif_q):
        try:
            self.notif_q = notif_q
            self.notif_p = Process(
                target=run_server, args=[notif_q])
            self.notif_p.start()
        except Exception as e:
            self.logger.exception(str(e))

    def __del__(self):
        self.notif_p.terminate()
        self.notif_p.join()


    def main_loop(self, sleep_time=0.2):
        try:
            while True:
                if not self.notif_q.empty():
                    item = json.loads(self.notif_q.get())
                    self.logger.debug(f"Notification Q:\n{item}")
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            self.logger.exception(str(e))


def application():
    notif_q = Queue()
    c = RobotServer(notif_q)
    c.main_loop()


if __name__ == '__main__':
    application()
