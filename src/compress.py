"""
Модуль реализует функции, отвечающие за сжатие бэкапа в архив
"""

import os
import logging

import compressors.tar_compressor as tar
import compressors.zip_compressor as zip

def compress(src: os.path, comp_type: str) -> None:
    """
    Функция реализует сжатие файлов, размещенных по пути src в архив в 
    соответсвии с выбранном типом архива
    Принимает параметры:
        src - путь, по которому находятся данные для сжатия
    Ничего не возвращает
    """
    logging.info(f"Start compress {os.path.abspath(src)} as {comp_type} archive")
    if comp_type == "tar":
        tar.tar_compress(src, src)
    elif comp_type == "zip":
        zip.zip_compress(src, src)
    # Никакого дефолтного значения тут нет, так как модуль config.py должен
    # озаботится валидацией
    logging.info(f"Successfully compressed")