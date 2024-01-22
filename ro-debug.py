#!/usr/bin/env python3

import tkinter
import RO.Comm.Generic
RO.Comm.Generic.setFramework("tk")
from RO.Comm.HubConnection import HubConnection
import time
#from twisted.internet import reactor
from getpass import getpass

if __name__=="__main__":
    root=tkinter.Tk()  ## For Tk.

    host = "hub35m.apo.nmsu.edu"
    port = 9877
    progID = "TU01"
    password = getpass("Enter password: ")
    username = "gmac"

    def readCallback(sock, astr):
        print(f"read: {astr}")

    def stateCallback(sock):
        state, reason = sock.fullState
        if reason:
            print(f"{state}: {reason}")
        else:
            print(f"{state}:")
    
    conn = HubConnection(
            name="debug-client",
            stateCallback=stateCallback,
            readCallback=readCallback
            )
    print("**** DOING CONNECTION ****")
    conn.connect( progID = progID,
            password = password,
            username = username,
            host = host,
            port = port,
            )
    root.mainloop()  ## For Tk.
    #reactor.run()  ## For twisted.
    print("**** FINISHED DOING CONNECTION ****")
    time.sleep(1)
    conn.disconnect()
