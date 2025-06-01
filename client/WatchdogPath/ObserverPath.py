
from watchdog.observers import Observer
import os
import time
from .actions.actions import ActionsDirectory

        
class ObserverDirectory:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = os.path.abspath(directory_to_watch)
        self.ActionDirectory = ActionsDirectory(self.directory_to_watch)
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self.ActionDirectory, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

   


# def run(self):
#     self.observer.schedule(self.ActionDirectory, self.directory_to_watch, recursive=True)
#     self.observer.start()
#     try:
#         self.observer.join()  # aguarda enquanto o observer está ativo
#     except KeyboardInterrupt:
#         self.observer.stop()
#         self.observer.join()



# import threading

# def run(self):
#     self.observer.schedule(self.ActionDirectory, self.directory_to_watch, recursive=True)
#     self.observer.start()
#     self.stop_event = threading.Event()
#     try:
#         self.stop_event.wait()  # aguarda até ser sinalizado para parar
#     except KeyboardInterrupt:
#         self.observer.stop()
#         self.stop_event.set()  # libera a espera
#     self.observer.join()

   
            