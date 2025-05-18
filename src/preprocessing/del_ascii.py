"""
recursively delete all results.ascii.txt files
"""

import os
import sys

def delete_results(root_dir = "annual_txts_fitz"):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'results.ascii.txt' in filenames:
            file_path = os.path.join(dirpath, 'results.ascii.txt')
            try:
                os.remove(file_path)
                print(f"Removed: {file_path}")
            except OSError as e:
                print(f"Error removing {file_path}: {e}", file=sys.stderr)

if __name__ == '__main__':
    delete_results()
