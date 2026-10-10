import os
import sys
import socket

hostname = socket.gethostname()
username = os.environ.get("USERNAME") or os.environ.get("USER") or "user"
cur_path = os.path.dirname(__file__)

#приглашение

# Главный цикл
while True:
    user_input_list = input(username+"@"+hostname+":~$ ").split()

    if not user_input_list: continue # Пустой ввод
    cmd = user_input_list[0]
    args = user_input_list[1:]
    
    # Раскрытие переменных окружения
    for i, arg in enumerate(args):
        if arg[0] == '$' and arg[1:] in os.environ:
            args[i] = os.environ[arg[1:]]
    
    if cmd == "exit": break
    elif cmd == "ls": print("ls", args)
    elif cmd == "cd": print("cd", args)
    else: print("Command not found")