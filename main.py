import os

def changed_files_list():
    """ Returns a list of paths for the changed files in the latest commit """
    with open('CHANGED_FILES_PATHS.txt') as f:
        filepaths = f.read().split('\n')
        filepaths = [x[2:] for x in filepaths if x and x[0] != 'D'] # remove empty strings and paths to deleted files
        os.remove('CHANGED_FILES_PATHS.txt')
        return filepaths

def filter_pdf_files(filepaths):
    """ Returns a filtered list with strings that end with '.pdf' """
    return [x for x in filepaths if x.endswith('.pdf')]

if __name__ == '__main__':
    filepaths = changed_files_list()
    print(filepaths)
    print(filter_pdf_files(filepaths))
    for path in filepaths:
        with open(path) as f:
            print(f.read())