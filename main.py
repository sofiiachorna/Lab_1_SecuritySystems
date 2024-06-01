import os
import getpass

emulated_disk_path = 'D:\\kpi\\3 KYPC\\Системи безпеки\\Lab_1_SB\\emulated_disk'

if not os.path.exists(emulated_disk_path):
    os.makedirs(emulated_disk_path)

def protect_emulation_path(path):
    os.chmod(path, 0o700)

def unprotect_emulation_path(path):
    os.chmod(path, 0o755)

protect_emulation_path(emulated_disk_path)

class AccessManager:
    def __init__(self):
        self.users = {
            'admin': {'password': 'adminpass', 'role': 'admin'},
            'user': {'password': 'userpass', 'role': 'user'}
        }
        self.current_user = None

    def login(self):
        print("Starting login process...")
        username = input("Username: ")
        print(f"Username entered: {username}")
        password = input("Password: ")
        print("Password entered")

        if username in self.users:
            print(f"User {username} found.")
            if self.users[username]['password'] == password:
                self.current_user = self.users[username]
                print(f"Welcome, {username}!")
            else:
                print("Invalid password")
                exit()
        else:
            print("Invalid username")
            exit()

    def check_access(self, path, mode):
        if self.current_user['role'] == 'admin':
            return True
        if mode == 'read' and os.access(path, os.R_OK):
            return True
        if mode == 'write' and os.access(path, os.W_OK):
            return True
        return False

    def pwd(self):
        print(os.getcwd())

    def ls(self):
        items = os.listdir()
        if not items:
            print("The directory is empty.")
        else:
            for item in items:
                print(item)

    def cd(self, path):
        if os.path.exists(path):
            os.chdir(path)
        else:
            print("Directory not found")

    def mkdir(self, path):
        if self.check_access(os.getcwd(), 'execute'):
            os.makedirs(path, exist_ok=True)
        else:
            print("Access denied")

    def vi(self, filename):
        if self.check_access(os.getcwd(), 'execute'):
            with open(filename, 'w') as f:
                content = input("Enter file content: ")
                f.write(content)
        else:
            print("Access denied")

    def rm(self, path):
        if self.check_access(os.getcwd(), 'execute'):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                os.rmdir(path)
        else:
            print("Access denied")

manager = AccessManager()
manager.login()

while True:
    command = input("$ ").split()
    if not command:
        continue
    cmd = command[0]
    args = command[1:]

    if cmd == 'pwd':
        manager.pwd()
    elif cmd == 'ls':
        manager.ls()
    elif cmd == 'cd' and args:
        manager.cd(args[0])
    elif cmd == 'mkdir' and args:
        manager.mkdir(args[0])
    elif cmd == 'vi' and args:
        manager.vi(args[0])
    elif cmd == 'rm' and args:
        manager.rm(args[0])
    elif cmd == 'exit':
        break
    else:
        print("Unknown command")

unprotect_emulation_path(emulated_disk_path)
