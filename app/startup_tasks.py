import pathlib
from config import LOCAL_PHOTO_STORAGE_DIR

pathlib.Path(LOCAL_PHOTO_STORAGE_DIR).mkdir(parents=True, exist_ok=True)