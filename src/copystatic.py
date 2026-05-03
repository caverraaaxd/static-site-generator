import os, shutil

def copy_files_recursive(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    for item in os.listdir(source_dir):
        full_source_path = os.path.join(source_dir, item)
        full_dest_path = os.path.join(dest_dir, item)


        if os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_dest_path)
        
        else:
            copy_files_recursive(full_source_path, full_dest_path)


def folder_cleanup(dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)