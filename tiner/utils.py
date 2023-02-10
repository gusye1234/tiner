import os
from types import FrameType
from typing import Dict
from difflib import get_close_matches


def getline(frame: FrameType):
    lineno = frame.f_lineno
    filename = frame.f_code.co_filename
    filename = os.path.relpath(filename)    
    return filename, lineno


def sanity_check(key, infos: Dict):
    if len(infos) == 0:
        raise KeyError(
            f"tiner didn't have any key")
    if key not in infos:
        most_key = get_close_matches(
            key, infos.keys(), n=1)
        if most_key:
            raise KeyError(
                f"tiner didn't have the key {key}, is it {most_key[0]}?")
        else:
            raise KeyError(
                f"tiner didn't have the key {key}")
