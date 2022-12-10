import os


def create_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
