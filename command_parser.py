# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

#command_parser.py

import pathlib
from notebook import Notebook

class CommandParser:
    def __init__(self):
        pass

    def create_notebook(self, args: list[str]) -> tuple[Notebook | None, pathlib.Path | None, str | None]:
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
            notebook.save_notebook(notebook_path)
            return notebook, notebook_path.resolve(), f"{notebook_path.resolve()} CREATED"
        except Exception:
            return None, None, "ERROR"

    def delete_notebook(self, args: list[str]) -> str | None:
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

    def open_notebook(self, args: list[str]) -> tuple[Notebook | None, pathlib.Path | None, str | None]:
        if len(args) != 1:
            return None, None, "ERROR"

        file_path_str = args[0]
        file_path = pathlib.Path(file_path_str).resolve()

        if not file_path.exists() or file_path.suffix != '.json':
            return None, None, "ERROR"

        try:
            username = input("username: ")
            password = input("password: ")

            notebook = Notebook.load_notebook(file_path)
            if notebook and notebook.username == username and notebook.password == password:
                return notebook, file_path, f"Notebook loaded.\n{notebook.username}\n{notebook.bio}"
            else:
                return None, None, "ERROR"
        except Exception:
            return None, None, "ERROR"

    def edit_notebook(self, notebook: Notebook, notebook_path: pathlib.Path, args: list[str]) -> str | None:
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
                    notebook.add_diary(diary_entry)
                    i += 1
                else:
                    return "ERROR"
            elif option == '-del':
                if i < len(args):
                    try:
                        index_to_delete = int(args[i])
                        notebook.delete_diary(index_to_delete)
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
                notebook.save_notebook(notebook_path)
            except Exception:
                return "ERROR"
        return None

    def print_notebook(self, notebook: Notebook, args: list[str]) -> str | None:
        output_lines = []
        i = 0
        error_occurred = False
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
                for index, diary in enumerate(notebook.diaries):
                    output_lines.append(f"{index}: {diary}")
            elif option == '-diary':
                if i < len(args):
                    try:
                        diary_id = int(args[i])
                        if 0 <= diary_id < len(notebook.diaries):
                            output_lines.append(notebook.diaries[diary_id])
                        else:
                            error_occurred = True
                    except ValueError:
                        error_occurred = True
                    i += 1
                else:
                    error_occurred = True
            elif option == '-all':
                output_lines.append(notebook.username)
                output_lines.append(notebook.password)
                output_lines.append(notebook.bio)
                for index, diary in enumerate(notebook.diaries):
                    output_lines.append(f"{index}: {diary}")
            else:
                error_occurred = True

            if error_occurred:
                break

        output = "\n".join(output_lines) if output_lines else None
        return f"{output}\nERROR" if output and error_occurred else output if output else "ERROR" if error_occurred and not output_lines else None
    