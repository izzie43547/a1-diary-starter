# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# LEXI ARBALLO
# LARBALLO@UCI.EDU
# 67207873

#command_parser.py

import pathlib
from notebook import Notebook, Diary
from typing import List, Tuple, Optional

class CommandParser:
    """
    A class responsible for parsing commands and interacting with the Notebook.
    """
    def __init__(self):
        """
        Initializes the CommandParser.
        """
        pass

    def create_notebook(self, args: List[str]) -> Tuple[Optional[Notebook], Optional[pathlib.Path], Optional[str]]:
        """
        Handles the 'C' command to create a new notebook.

        Args:
            args (List[str]): A list of arguments following the 'C' command.

        Returns:
            Tuple[Optional[Notebook], Optional[pathlib.Path], Optional[str]]:
            A tuple containing the created Notebook object, its path, and an output message,
            or (None, None, "ERROR") if the command fails.
        """
        if len(args) != 3 or args[1] != '-n':
            return None, None, "ERROR"

        path_str = args[0]
        diary_name = args[2]

        try:
            notebook_path = pathlib.Path(path_str) / f"{diary_name}.json"
            if notebook_path.exists():
                return None, None, "ERROR"
            if not notebook_path.parent.exists():
                return None, None, "ERROR"

            username = input("username: ")
            password = input("password: ")
            bio = input("bio: ")

            notebook = Notebook(username, password, bio)
            notebook.save(notebook_path)
            return notebook, notebook_path.resolve(), f"{notebook_path.resolve()} CREATED"
        except Exception as e:
            print(f"Error during create_notebook: {e}")
            return None, None, "ERROR"

    def delete_notebook(self, args: List[str]) -> Optional[str]:
        """
        Handles the 'D' command to delete an existing notebook.

        Args:
            args (List[str]): A list containing the path to the notebook to delete.

        Returns:
            Optional[str]: A success message with the deleted path, or "ERROR" if deletion fails.
        """
        if len(args) != 1:
            return "ERROR"

        file_path_str = args[0]
        file_path = pathlib.Path(file_path_str).resolve()

        if not file_path.exists() or file_path.suffix != '.json':
            return "ERROR"

        try:
            file_path.unlink()
            return f"{file_path} DELETED"
        except Exception:
            return "ERROR"

    def open_notebook(self, args: List[str]) -> Tuple[Optional[Notebook], Optional[pathlib.Path], Optional[str]]:
        """
        Handles the 'O' command to load an existing notebook.

        Args:
            args (List[str]): A list containing the path to the notebook to open.

        Returns:
            Tuple[Optional[Notebook], Optional[pathlib.Path], Optional[str]]:
            A tuple containing the loaded Notebook object, its path, and user information,
            or (None, None, "ERROR") if loading fails.
        """
        if len(args) != 1:
            return None, None, "ERROR"

        file_path_str = args[0]
        file_path = pathlib.Path(file_path_str).resolve()

        if not file_path.exists() or file_path.suffix != '.json':
            return None, None, "ERROR"

        try:
            username = input("username: ")
            password = input("password: ")

            # Create notebook with temporary values
            notebook = Notebook(username, password, "")
            # Load the actual values from file
            notebook.load(file_path)
            
            if notebook.username == username and notebook.password == password:
                return notebook, file_path, f"Notebook loaded.\n{notebook.username}\n{notebook.bio}"
            else:
                return None, None, "ERROR"
        except Exception as e:
            print(f"Error during open: {e}")
            return None, None, "ERROR"

    def edit_notebook(self, notebook: Notebook, notebook_path: pathlib.Path, args: List[str]) -> Optional[str]:
        """
        Handles the 'E' command to edit the loaded notebook.

        Args:
            notebook (Notebook): The currently loaded Notebook object.
            notebook_path (pathlib.Path): The path to the currently loaded notebook file.
            args (List[str]): A list of arguments specifying the edits to perform.

        Returns:
            Optional[str]: None if edits were successful, or "ERROR" if any edit failed.
        """
        i = 0
        while i < len(args):
            option = args[i]
            i += 1
            if option == '-usr':
                if i < len(args):
                    notebook.username = args[i]
                    i += 1
                else:
                    return "ERROR"
            elif option == '-pwd':
                if i < len(args):
                    notebook.password = args[i]
                    i += 1
                else:
                    return "ERROR"
            elif option == '-bio':
                if i < len(args):
                    notebook.bio = args[i]
                    i += 1
                else:
                    return "ERROR"
            elif option == '-add':
                if i < len(args):
                    diary_entry = args[i]
                    diary = Diary(entry=diary_entry)
                    notebook.add_diary(diary)
                    i += 1
                else:
                    return "ERROR"
            elif option == '-del':
                if i < len(args):
                    try:
                        index_to_delete = int(args[i])
                        if not notebook.del_diary(index_to_delete):
                            return "ERROR"
                        i += 1
                    except ValueError:
                        return "ERROR"
                    except IndexError:
                        return "ERROR"
                else:
                    return "ERROR"
            else:
                return "ERROR"
            try:
                notebook.save(notebook_path)
            except Exception:
                return "ERROR"
        return None

    def print_notebook(self, notebook: Notebook, args: List[str]) -> Optional[str]:
        """
        Handles the 'P' command to print information from the loaded notebook.

        Args:
            notebook (Notebook): The currently loaded Notebook object.
            args (List[str]): A list of arguments specifying what information to print.

        Returns:
            Optional[str]: The formatted output to print, or "ERROR" if an invalid option is encountered.
        """
        output_lines = []
        i = 0
        while i < len(args):
            option = args[i]
            i += 1
            if option == '-usr':
                output_lines.append(notebook.username)
            elif option == '-pwd':
                output_lines.append(notebook.password)
            elif option == '-bio':
                output_lines.append(notebook.bio)
            elif option == '-diaries':
                for index, diary in enumerate(notebook.get_diaries()):
                    output_lines.append(f"{index}: {diary.get_entry()}")
            elif option == '-diary':
                if i < len(args):
                    try:
                        diary_id = int(args[i])
                        diaries = notebook.get_diaries()
                        if 0 <= diary_id < len(diaries):
                            output_lines.append(diaries[diary_id].get_entry())
                        else:
                            print("\n".join(output_lines))
                            return "ERROR"
                    except ValueError:
                        print("\n".join(output_lines))
                        return "ERROR"
                    i += 1
                else:
                    print("\n".join(output_lines))
                    return "ERROR"
            elif option == '-all':
                output_lines.append(notebook.username)
                output_lines.append(notebook.password)
                output_lines.append(notebook.bio)
                for index, diary in enumerate(notebook.get_diaries()):
                    output_lines.append(f"{index}: {diary.get_entry()}")
            else:
                print("\n".join(output_lines))
                return "ERROR"

        return "\n".join(output_lines) if output_lines else None
    