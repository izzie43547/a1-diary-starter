# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# LEXI ARBALLO
# LARBALLO@UCI.EDU
# 67207873

# a1.py

import shlex
import pathlib
from notebook import Notebook
from command_parser import CommandParser
import sys

def main():
    """
    The main entry point for the diary program.
    It handles user input, parses commands, and interacts with the CommandParser and Notebook.
    """
    notebook = None
    notebook_path = None
    command_parser = CommandParser()

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            command_parts = shlex.split(user_input)
            if not command_parts:
                continue

            command = command_parts[0].upper()
            args = command_parts[1:]

            if command == 'Q':
                break
            elif command == 'C':
                notebook, notebook_path, output = command_parser.create_notebook(args)
                if output:
                    print(output)
            elif command == 'D':
                output = command_parser.delete_notebook(args)
                if output:
                    print(output)
            elif command == 'O':
                notebook, notebook_path, output = command_parser.open_notebook(args)
                if output:
                    print(output)
            elif command == 'E':
                if notebook and notebook_path:
                    output = command_parser.edit_notebook(notebook, notebook_path, args)
                    if output:
                        print(output)
                else:
                    print("ERROR")
            elif command == 'P':
                if notebook:
                    output = command_parser.print_notebook(notebook, args)
                    if output:
                        print(output)
                else:
                    print("ERROR")
            else:
                print("ERROR")

        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("ERROR")

if __name__ == "__main__":
    main()
