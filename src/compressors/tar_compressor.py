"""
Модуль овечает за сборку tar-архива
"""

import os
import tarfile

def tar_compress(path_src: os.path, path_dst: os.path) -> None:
    """
    Сборка tar-архива из директории
    Принимает параметры:
        path_src - Путь к директории из которой нужно собрать архив;
        path_dst - Путь архива;
    Ничего не возвращает
    """
    # Открываем архив
    with tarfile.open(f"{path_dst}.tar.gz", mode='w:gz') as tf:
                tf.add(path_src, arcname=os.path.basename(path_src))
                

if __name__ == "__main__":
    tar_compress(path_src=os.path.join("E://scripts/dir_test"), 
                 path_dst=os.path.join("E://scripts/test_tar"))