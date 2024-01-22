#!/usr/bin/env python3

import tkinter
import tkinter.scrolledtext as scrolledtext
import RO.Comm.Generic
RO.Comm.Generic.setFramework("twisted")
from RO.Comm.HubConnection import HubConnection
import RO.KeyDispatcher
import time
from getpass import getpass

if __name__=="__main__":
    
    root=tkinter.Tk()  ## For Tk.
    import twisted.internet.tksupport
    twisted.internet.tksupport.install(root)
    from twisted.internet import reactor

    host = "hub35m.apo.nmsu.edu"
    port = 9877
    progID = "TU01"
    password = getpass("Enter password: ")
    username = "gmac"

    def updateScrolledText(astr):
        timeStr = time.ctime()
        textArea.configure(state='normal')
        textArea.insert(tkinter.INSERT, f"{timeStr}: {astr}\n")
        textArea.configure(state='disabled')
        textArea.see(tkinter.END)

    def onExit():
        conn.disconnect()
        reactor.stop()

    def readCallback(sock, astr):
        print(f"read: {astr}")
        updateScrolledText(astr)

    def stateCallback(sock):
        state, reason = sock.fullState
        if reason:
            print(f"{state}: {reason}")
        else:
            print(f"{state}:")

    root.title("RO Debug")  ## Window title
    tkinter.Label(root,     ## Text area title
            text="Messages from hub35m"
            ).grid(
                    column=0,
                    row=0
                    )
    textArea = scrolledtext.ScrolledText(root,  ## Text area
            width=120,
            height=30
            )
    textArea.grid(column=0, pady=10, padx=10)
    tkinter.Button(root,    ## Quit button
            text="Exit",
            command=onExit
            ).grid(
                    column=0,
                    row=2
                    )

    conn = HubConnection(
            name="debug-client",
            stateCallback=stateCallback,
            readCallback=readCallback
            )
    disp = RO.KeyDispatcher.KeyDispatcher(connection=conn)
    print("**** DOING CONNECTION ****")
    disp.connection.connect( progID = progID,
            password = password,
            username = username,
            host = host,
            port = port,
            )
    print("**** FINISHED DOING CONNECTION ****")
    disp.refreshAllVar(resetAll=True)
    reactor.run()  ## For twisted.
    
