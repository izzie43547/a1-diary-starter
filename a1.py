# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# LEXI ARBALLLO
# LARBALLO@UCI.EDU
# 67207873

import os

def processCommand(command):
    parts = command.split(maxsplit=1)

    if len(parts) < 2:
        print('ERROR')
        return

    action, argument = parts

    if action == 'R':
        handleReadCommand(argument)
    elif action == 'C':
        handleCreateCommand(argument)
    elif action == 'D':
        handleDeleteCommand(argument)
    else:
        print('ERROR')

def handleReadCommand(filePath):
    if not os.path.exists(filePath) or not filePath.endswith('.dsu'):
        print('ERROR')
    else:
        try:
            with open(filePath, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if content:
                    print(content)
                else:
                    print('EMPTY')
        except Exception:
            print('ERROR')

def handleCreateCommand(arguments):
    args = arguments.split('-n', maxsplit=1)
    if len(args) != 2:
        print('ERROR')
        return

    dirPath, fileName = args[0].strip(), args[1].strip()
    filePath = os.path.join(dirPath, f"{fileName}.dsu")

    try:
        with open(filePath, 'w', encoding='utf-8') as file:
            pass
        print(filePath)
    except Exception:
        print('ERROR')

def handleDeleteCommand(filePath):
    if not os.path.exists(filePath):
        print('ERROR')
    else:
        try:
            os.remove(filePath)
            print(f"{filePath} DELETED")
        except Exception:
            print('ERROR')

if __name__ == '__main__':
    while True:
        try:
            command = input().strip()
            if command.upper() == 'Q':
                break
            processCommand(command)
        except EOFError:
            break
