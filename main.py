import os
import sys
from github import Github
from refextract import extract_references_from_file


def comment_pr(github_token, repo_name, pr_number, content, ref_count, faulty_pdfs):
    """ Returns the parsed string version of the reference (dict) and strip down based on verbosity

    Keyword arguments:
    github_token -- token to authenticate in workflow run
    repo_name -- the name of the repo that the workflow is run from
    pr_number -- the number of the PR that triggered the action
    content -- the content that should be commented in the PR
    faulty_pdfs -- a list of pdf files either without references or with problems parsing
    """
    content_md = content_to_md(content, ref_count, faulty_pdfs)
    github = Github(github_token)
    repo = github.get_repo(repo_name)
    issue = repo.get_issue(int(pr_number))
    comment_header = '## :blue_book: :mag_right: PDF Bibliography summary\n'
    issue.create_comment(comment_header + content_md)


def content_to_md(content, ref_count, faulty_pdfs):
    """ Returns the content (reference list for each pdf file) in a markdown formated string

    Keyword arguments:
    content -- a dict with each key being a pdf filepath and reference list (str) as value
    ref_count -- a dict with each key being a pdf filepath and reference count as value
    faulty_pdfs -- a list of pdf files either without references or with problems parsing
    """
    content_md = ''
    for key, value in content.items():
        content_md += ('### File: ' + key + ' (reference count: ' + str(ref_count[key]) +
                       ')\n```\n' + value + '```\n')
    if len(faulty_pdfs) != 0:
        content_md += ('\n :x: Could not find reference list for pdf files: ' + ' '.join(faulty_pdfs))
    return content_md


def remove_duplicate_refs(refs):
    """ Returns the list of references without duplicates that sometimes happen with refextract

    Keyword arguments:
    refs -- list of references parsed by refextract
    """
    saved_refs = []
    refs_cleaned = []
    for ref in refs:
        if 'linemarker' in ref and ref['linemarker'][0] not in saved_refs:
            refs_cleaned.append(ref)
            saved_refs.append(ref['linemarker'][0])
    return refs_cleaned


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
    refs -- list of references parsed by refextract
    verbosity -- the level of verbostiy for the reference composition (default 2)
    """
    reference_list = ''
    for ref in refs:
        prettified_ref = prettify_reference(ref, verbosity)
        if prettified_ref is not None:
            reference_list += (prettified_ref + '\n')
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
    return remove_duplicate_refs(references)


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
    _, _, github_token, repo_name, pr_number, verbosity = sys.argv
    filepaths = changed_files_list()
    print(filepaths)
    filepaths_pdf = filter_pdf_files(filepaths)
    if len(filepaths_pdf) == 0:
        print('No pdf files in commit')
        return
    print(filepaths_pdf)
    faulty_pdfs = []
    references_in_pdfs = {}
    references_in_pdfs_count = {}
    for path in filepaths_pdf:
        reference_list = find_reference_list(path)
        if len(reference_list) == 0:
            faulty_pdfs.append(path)
            continue
        prettified_refs = prettify_references(reference_list, verbosity=int(verbosity))
        references_in_pdfs[path] = prettified_refs
        references_in_pdfs_count[path] = len(reference_list)
    if references_in_pdfs != {} or faulty_pdfs != 0:
        comment_pr(github_token, repo_name, pr_number, references_in_pdfs,
                   references_in_pdfs_count, faulty_pdfs)


if __name__ == '__main__':
    main()
