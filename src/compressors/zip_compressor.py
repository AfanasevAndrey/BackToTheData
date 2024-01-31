"""
Модуль овечает за сборку zip-архива
"""

import glob
import os
import logging
import zipfile

def zip_compress(path_src: os.path, path_dst: os.path) -> None:
    """
    Сборка zip-архива из директории
    Принимает параметры:
        path_src - Путь к директории из которой нужно собрать архив;
        path_dst - Путь архива;
    Ничего не возвращает
    """
    # Открываем архив
    with zipfile.ZipFile(f"{path_dst}.zip", mode='w', \
                            compression=zipfile.ZIP_DEFLATED) as zf:
                # Получаем содержимое директории
                name_list = glob.glob(f"{os.path.abspath(path_src)}/**", 
                                      recursive=True)
                name_list_for_logging = '\n'.join(name_list)
                logging.debug(f"Get files in {path_src} for compress:"+
                              f"\n{name_list_for_logging}")
                # Добавляем содержимое директории в архив 
                # arcname нужен чтобы в архиве не было абсолютных путей
                for name in name_list:
                    if not os.path.isdir(name):
                        zf.write(name, 
                                arcname=os.path.abspath(name).removeprefix(
                                os.path.abspath(os.path.join(os.path.dirname(path_src),
                                os.path.basename(path_src)))+"\\"))
