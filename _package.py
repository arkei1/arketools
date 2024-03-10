import os
import zipfile

from version import version


def pack_addon(source_folder: str):
    source_folder = os.path.abspath(source_folder)
    addon_name = os.path.basename(source_folder) # получаем имя аддона по названию папки

    with zipfile.ZipFile(addon_name + f'_v{version[0]}.{version[1]}.{version[2]}' + ".zip", 'w') as zip_file:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                
                if file == '__init__.py': pass
                elif root.endswith('__pycache__'): continue
                elif file.startswith('_') or file.startswith('.'): continue
                elif file.endswith('.blend1') or file.endswith('.zip'): continue
                
                file_path = os.path.relpath(os.path.join(root, file), os.path.abspath('.'))
                arcname = os.path.join(addon_name, file_path.replace(source_folder + '/', ''))
                zip_file.write(file_path, arcname=arcname)

# Путь к папке аддона и куда сохранить .zip файл
source_folder = '.'

pack_addon(source_folder)