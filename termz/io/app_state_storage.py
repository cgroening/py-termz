"""
termz.io.app_state_storage
==========================

A simple JSON-based storage system that allows reading, writing and modifying
key-value pairs in a JSON file. It ensures data persistence across sessions
and provides utility functions for handling lists within the JSON structure.

The class AppStorage provides an easy-to-use interface for managing application
settings or any structured data in a JSON file. It follows a singleton pattern
to ensure a single instance across the application.

Features:
- Reads a JSON file and loads its content into a dictionary.
- Provides methods to retrieve (`get`) and update (`set`) key-value pairs.
- Supports modifying lists within the JSON file, including:
  - Inserting elements at a specific index (`array_insert`).
  - Editing individual elements within a list (`edit_array_item`).
  - Deleting elements from a list (`delete_array_item`).
  - Moving elements within a list (`move_array_item`).
- Ensures data persistence by saving changes to the JSON file automatically.
- Manages file creation and error handling for missing or corrupted JSON files.

This module is useful for applications requiring persistent storage of
configuration settings, user preferences or structured data that does not
require a full-fledged database.

"""

# Libs
import sys
import json
import os
from pathlib import Path

from termz.util.singleton import Singleton


class AppStateStorage(metaclass=Singleton):
    """
    This class opens a JSON file and saves the content in a dictionary which can be accessed with get().

    Changed values or new key-value pairs can be stored
    within the Dictionary and the JSON file with the method set().

    Attributes
    ----------
    json_file : Path or str or None
        Path to the JSON file.
    json_dict : dict[str, str | int | float | bool | list[dict]]
        Content of the JSON file as a dictionary.
    """
    json_file: Path | str | None
    json_dict: dict[str, str | int | float | bool | list[dict]] = {}


    def __init__(self, cfg_file: Path | str | None = None) -> None:
        """
        Opens the JSON file and stores the key-value pairs in self.json_dict.

        Parameters
        ----------
        cfg_file : Path or str or None, optional
            Path to the JSON file.
        """
        # Raise error if class instance is None and no file path is given
        if AppStateStorage.instance is None and cfg_file is None:
            raise Exception('No JSON file given.')

        # Store path the JSON file
        self.json_file = cfg_file


        # Open JSON file
        self.read_json_file()

    def read_json_file(self) -> None:
        """
        Opens the JSON file and stores the content in self.json_dict.
        """
        abs_path = os.path.abspath(self.json_file)  # type: ignore

        # Open file
        try:
            # Store key-value pairs
            with open(self.json_file, encoding='utf-8') as file:  # type: ignore
                self.json_dict = json.load(file)
        except FileNotFoundError:
            # File not found -> try to create a new one
            try:
                with open(self.json_file, 'w') as file:  # type: ignore
                    file.write('{}')
            except FileNotFoundError:
                print('ERROR: Could not find or create JSON file '
                      f'"{abs_path}".')
                sys.exit()
        except json.JSONDecodeError:
            # File has JSON errors
            print(f'Error: File "{abs_path}" contains invalid JSON.')
            sys.exit()

    def save_json_file(self) -> None:
        """
        Stores the content of self.json_dict in the JSON file.
        """
        abs_path = os.path.abspath(self.json_file)  # type: ignore

        try:
            with open(self.json_file, 'w', encoding='utf-8') as file:  # type: ignore
                json.dump(self.json_dict, file, indent=4)  # noqa
        except IOError:
            print(f'Fehler: File {abs_path} could not be written.')

    def get(self, key: str, default_value: object = None) \
            -> str | int | float | bool | list | dict | None:
        """
        Returns a value from the JSON file.

        If the given key cannot be found
        the default value specified will be returned.

        Parameters
        ----------
        key : str
            Key of the entry.
        default_value : object, optional
            Default value.

        Returns
        -------
        str or int or float or bool or list or dict or None
            The value belonging to the given key.
        """
        if key in self.json_dict:
            return self.json_dict[key]
        else:
            return default_value  # type: ignore

    def set(self, key: str,
            value: str | int | float | bool | list | dict) -> None:
        """
        Updates the dictionary self.json_dict and stores the given key-value pair in the JSON file.

        Parameters
        ----------
        key : str
            Key of the entry.
        value : str or int or float or bool or list or dict
            Value of the entry.
        """
        self.json_dict.update({key: value})    # type: ignore
        self.save_json_file()

    def array_insert(self, array_name: str, array_index: int,
                     value: str | int | float | list | dict) -> None:
        """
        Adds a new entry to an array/list at the given index.

        Parameters
        ----------
        array_name : str
            Name of the array/list.
        array_index : int
            Index of the array/list element.
        value : str or int or float or list or dict
            Value of the array/list element = dictionary.
        """
        # Create array/list if it doesn't exist
        if array_name not in self.json_dict:
            self.json_dict.update({array_name: []})

        # Create empty array/list if value is empty
        if self.json_dict[array_name] is None:
            self.json_dict[array_name] = []

        # Add given data to dict and write to JSON file
        self.json_dict[array_name].insert(array_index, value)    # type: ignore
        self.save_json_file()

    def edit_array_item(self, array_name: str, array_index: int,
                        dict_key: str, value: str | int | float | list | dict) \
            -> None:
        """
        Changes the value of an array item.

        Parameters
        ----------
        array_name : str
            Name of the array/list.
        array_index : int
            Index of the array/list element.
        dict_key : str
            The key of the dictionary.
        value : str or int or float or list or dict
            Value of the array/list element = dictionary.
        """
        self.json_dict[array_name][array_index][dict_key] = value  # type: ignore
        self.save_json_file()

    def delete_array_item(self, array_name: str, array_index: int) -> None:
        """
        Deletes an element of an array/list.

        Parameters
        ----------
        array_name : str
            Name of the array/list.
        array_index : int
            Index of the array/list element.
        """
        del self.json_dict[array_name][array_index]  # type: ignore
        self.save_json_file()

    def move_array_item(self, array_name: str, array_index: int,
                        array_index_new: int) -> None:
        """
        Moves an array/list element by deleting and re-inserting it at a new position.

        Parameters
        ----------
        array_name : str
            Name of the array/list.
        array_index : int
            Index of the array/list element.
        array_index_new : int
            Index of the new array/list element.
        """
        # Save value of the element
        array_element = self.json_dict[array_name][array_index]  # type: ignore

        # Delete element
        del self.json_dict[array_name][array_index]  # type: ignore

        # Insert element at new position
        self.json_dict[array_name].insert(array_index_new, array_element)  # type: ignore
        self.save_json_file()

