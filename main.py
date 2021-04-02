import os
import sys
from github import Github 
from refextract import extract_references_from_file


def comment_pr(github_token, repo_name, pr_number, content):
    """ Returns the parsed string version of the reference (dict) and strip down based on verbosity

    Keyword arguments:
    github_token -- token to authenticate in workflow run
    repo_name -- the name of the repo that the workflow is run from
    pr_number -- the number of the PR that triggered the action
    content -- the content that should be commented in the PR
    """
    github = Github(github_token)
    repo = github.get_repo(repo_name)
    issue = repo.get_issue(int(pr_number))
    issue.create_comment(content)


def prettify_reference(ref, verbosity=2):
    """ Returns the parsed string version of the reference (dict) and strip down based on verbosity

    Keyword arguments:
    ref -- reference parsed by refextract as a dict
    verbosity -- the level of verbostiy for the reference composition (default 2)
    """
    if verbosity == 2 and len(ref['raw_ref'][0]) != 0:
        return ref['raw_ref'][0]


def prettify_references(refs, verbosity=2):
    """ Returns the parsed string version of the references (dict)

    Keyword arguments:
    refs -- List of references parsed by refextract
    verbosity -- the level of verbostiy for the reference composition (default 2)
    """
    reference_list = ''
    for ref in refs:
        reference_list += prettify_reference(ref, verbosity) + '\n'
    return reference_list


def find_reference_list(path):
    """ Returns the reference list as a list of dicts if refextract can detect one

    Keyword arguments:
    path -- path to the file containing filepaths for the files that should be examined
    """
    references = []
    try:
        references = extract_references_from_file(path)
    except:
        print('Could not read pdf file')
    return references


def changed_files_list():
    """ Returns a list of paths for the changed files in the latest commit """
    try:
        with open('CHANGED_FILES_PATHS.txt') as f:
            filepaths = f.read().split('\n')
            filepaths = [x[2:] for x in filepaths if x and x[0] != 'D']  # Skip deleted files & empty str
            os.remove('CHANGED_FILES_PATHS.txt')
        return filepaths
    except:
        print('Could not read file containing filepaths for changed files')
        return []


def filter_pdf_files(filepaths):
    """ Returns a filtered list with strings that end with '.pdf'

    Keyword arguments:
    filepaths -- List of filepath strings
    """
    return [x for x in filepaths if x.endswith('.pdf')]


def main():
    _, _, github_token, repo_name, pr_number = sys.argv
    filepaths = changed_files_list()
    print(filepaths)
    filepaths_pdf = filter_pdf_files(filepaths)
    print(filepaths_pdf)
    if len(filepaths_pdf) == 0:
        print('No pdf files in commit')
        return
    references_in_pdfs = {}
    for path in filepaths_pdf:
        reference_list = find_reference_list(path)
        prettified_refs = prettify_references(reference_list)
        references_in_pdfs[path] = prettified_refs
    if references_in_pdfs != {}:
        comment_pr(github_token, repo_name, pr_number, references_in_pdfs)


if __name__ == '__main__':
    main()
