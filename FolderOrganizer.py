import os
import shutil
import logging
import argparse
import time

def create_logger():
    logging.basicConfig(filename='file_organizer.log', level=logging.INFO, format='%(asctime)s: %(message)s')
    return logging.getLogger()

def move_file(file_path, target_directory, logger):
    try:
        shutil.move(file_path, target_directory)
        logger.info(f"Move file {file_path} to {target_directory}")
    except Exception as e:
        logger.error(f"Error moveing file {file_path} to {target_directory}: {e}")

def organize_by_type(directory, logger):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_type = filename.split('.')[-1]
            target_directory = os.path.join(directory, file_type)

            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            file_path = os.path.join(directory, filename)
            move_file(file_path, target_directory, logger)

def organize_by_date(directory, logger):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_creation_time = os.path.getctime(os.path.join(directory, filename))
            date_folder = time.strftime('%Y-%m-%d', time.localtime(file_creation_time))
            target_directory = os.path.join(directory, date_folder)

            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            file_path = os.path.join(directory, filename)
            move_file(file_path, target_directory, logger)

def main():
    parser = argparse.ArgumentParser(description='Organize files in a directory.')
    parser.add_argument('directory', help='Directory to organize')
    parser.add_argument('--sort', choices=['type', 'date'], default='type', help='Sort by file type or creation date')

    args = parser.parse_args()
    directory_path = args.directory
    sort_method = args.sort
    logger = create_logger()

    if sort_method == 'type':
        organize_by_type(directory_path, logger)
    elif sort_method == 'date':
        organize_by_date(directory_path, logger)

if __name__ == "__main__":
    main()