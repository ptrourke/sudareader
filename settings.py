from pathlib import Path

# Most settings values will be vaulted in a local_settings.py ansible vault.
VAULT = None

# Directory where the sol-entries files are kept to be extracted.
HOST_ROOT_DIRECTORY = VAULT
EXTRACT_SOURCE_FILES = VAULT
CODE_FILES = Path.cwd()
INDEX_HOSTNAME = VAULT

try:
    from local_settings import *
except:
    pass
