import os
import pdftotext


def find_reference_list(path):
    """ Returns the reference list as a string if there is one """
    with open(path, 'rb') as f:
        pdf = pdftotext.PDF(f)
    for page in pdf:
        print(page)


def changed_files_list():
    """ Returns a list of paths for the changed files in the latest commit """
    with open('CHANGED_FILES_PATHS.txt') as f:
        filepaths = f.read().split('\n')
        filepaths = [x[2:] for x in filepaths if x and x[0] != 'D']  # remove empty str & paths to deleted files
        os.remove('CHANGED_FILES_PATHS.txt')
        return filepaths


def filter_pdf_files(filepaths):
    """ Returns a filtered list with strings that end with '.pdf' """
    return [x for x in filepaths if x.endswith('.pdf')]


if __name__ == '__main__':
    filepaths = changed_files_list()
    print(filepaths)
    filepaths_pdf = filter_pdf_files(filepaths)
    if len(filepaths_pdf) == 0:
        print('No pdf files in commit')
    print(filepaths_pdf)
    for path in filepaths_pdf:
        find_reference_list(path)
