#!/usr/bin/env python
import os
import sys
from airconditioning.Condition import *

ip =input("ip address")
Client1=Client(adress=ip)

if __name__ == "__main__":

    thread1 = UseThread(1)
    thread2 = UseThread(2)
    # 开启新线程
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


'''
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airconditioning.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
'''
