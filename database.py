import datetime
import json
import os

from config import INDEX_FILE


def init_index():
    """
    Initializes files index if empty
    """
    DIR = os.path.dirname(INDEX_FILE)

    if not os.path.isdir(DIR):
        os.mkdir(DIR)

    if not os.path.exists(INDEX_FILE):
        Index = {}
        with open(INDEX_FILE, 'w') as f:
            f.write(json.dumps(Index))


def read_index():
    """
    Reads files index and returns database state
    """

    with open(INDEX_FILE, 'r') as f:
        Index = json.load(f)

    files_info = [{'name': f[0], 'datetime': f[1]} for f in Index.items()]

    return files_info


def update_index(filename):
    """
    Updates files index with a new file
    """
    with open(INDEX_FILE, 'r') as f:
        Index = json.load(f)
        Index[os.path.basename(filename)] = str(datetime.datetime.now())
        with open(INDEX_FILE, 'w') as f:
            f.write(json.dumps(Index))
