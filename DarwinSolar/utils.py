# to send email faster
import os
import threading


class EmailThread(threading.Thread):
    def __init__(self, send_email):
        self.send_email = send_email
        threading.Thread.__init__(self)

    def run(self):
        self.send_email.send(fail_silently=False)


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext

