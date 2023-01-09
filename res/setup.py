"""Download and unpack models"""

import requests
import zipfile
import os

models = {
    "nlp": "1LTJs2mORb7MgCjPvNQ_CGK_hkiB1Noaa",
    "wav2vec": "1rOwXgccc2PQu39xGarnPZ_R_5ubcD_iT"
}

for fname, id in models.items():
    fpath = f"./{fname}.zip"
    dirpath = f"./{fname}"
    
    if os.path.exists(dirpath):
        print(f"Folder {fname} already exists, please delete to re-download model")
        continue

    url = f"https://drive.google.com/uc?export=download&confirm=t&id={id}"
    
    print(f"Downloading {fname} model (may take some time)...")
    response = requests.get(url)
    open(fpath, "wb").write(response.content)

    print(f"Extracting {fname} model...")
    with zipfile.ZipFile(fpath, 'r') as f:
        f.extractall(".")
        
    os.unlink(fpath)
    print(f"Model {fname} ready")
