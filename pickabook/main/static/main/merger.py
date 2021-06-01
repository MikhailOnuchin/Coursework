import os
import shutil
import zipfile


def unpack_covers():
    path = '../../../static/main/covers/'
    zips = os.listdir('splitted_covers')
    zips.sort(key=lambda s: int(s[6:-4]))
    for z in zips:
        with zipfile.ZipFile('splitted_covers/'+z, 'r') as zip_ref:
            zip_ref.extractall(path)
        print(z)
        os.remove('splitted_covers/'+z)


unpack_covers()
