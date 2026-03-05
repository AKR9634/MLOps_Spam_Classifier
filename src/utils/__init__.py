import os
import sys
import numpy as np
import dill
import yaml
import pandas

from src.exception import MyException
from src.logger import logging

def read_yaml_file(file_path : str) -> dict:
    try:
        with open(file_path, "rb") as  file:
            return yaml.safe_load(file)
    
    except Exception as e:
        raise MyException(e, sys)
    

def write_yaml_file(file_path : str, content : object, replace : bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise MyException(e, sys)
    

def load_object(file_path : str) -> object:
    try:
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)
        return obj
    except Exception as e:
        raise MyException(e, sys)
    

def save_object(file_path : str, obj : object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise MyException(e, sys)
    

def save_numpy_array_data(file_path : str, array : np.array):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise MyException(e, sys)
    

def load_numpy_array_data(file_path : str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MyException(e, sys)
    
