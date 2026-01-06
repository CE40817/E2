import socket
import time
import os
import secrets
import threading
FLAG =os .environ .get ("FLAG",f"CTF{{SELECTIVE_JAM_{secrets.token_hex(4).upper()}}}")


T_SIFS =0.5

def handle (conn ):
    conn .send (b"--- RF LINK ESTABLISHED ---\n")
    jams =0

    while True :
        try :

            conn .send (b"EVENT: DATA_FRAME_START\n")
            time .sleep (0.5 )
            conn .send (b"EVENT: DATA_FRAME_END\n")


            conn .send (b"EVENT: SIFS_WAIT\n")
            time .sleep (T_SIFS )


            conn .send (b"EVENT: ACK_WINDOW_OPEN\n")


            conn .settimeout (0.5 )
            try :
                data =conn .recv (1024 )
                if b"JAM"in data :
                    jams +=1
                    conn .send (b"RESULT: ACK JAMMED! RETRYING...\n")
                else :
                    jams =0
                    conn .send (b"RESULT: ACK OK.\n")
            except socket .timeout :
                jams =0
                conn .send (b"RESULT: ACK OK.\n")

            if jams >=3 :
                conn .send ((FLAG +"\n").encode ())
                break

        except :break
    conn .close ()

def main ():
    s =socket .socket (socket .AF_INET ,socket .SOCK_STREAM )
    s .bind (('0.0.0.0',5555 ))
    s .listen (5 )
    print ("RF Sim listening on 5555")
    while True :
        c ,a =s .accept ()
        threading .Thread (target =handle ,args =(c ,)).start ()

if __name__ =="__main__":main ()
