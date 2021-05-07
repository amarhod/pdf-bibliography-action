# :blue_book: :mag_right: PDF Bibliography summary action
This Github Action generates a summary of the bibliography for each PDF file in a PR and posts it in a comment 

```yaml
      env:
        BRANCH_DIFF: origin/main
      run: |
        git diff-tree --no-commit-id --name-status -r $BRANCH_DIFF ${{ github.sha }} > CHANGED_FILES_PATHS.txt
    - uses: amarhod/pdf-bibliography-action@v1
      with:
        token: ${{ github.token }}
        repo_path: ./
        repo_name: ${{ github.repository }}
        pr_number: ${{ github.event.number }}
        verbosity: 2
```


## How to setup

### Create a yaml workflow file in your project

Create a YAML file in the workflow directory, name it `bibliography-summary.yml`


An example of what to put in your `.github/workflows/bibliography-summary.yml` file to trigger the action

```yaml
on:
  pull_request:
    types: [labeled]

jobs:
  pdf-bibliography:
    name: A job to check bibliography in PDF files and post summary comment in PR
    if: ${{ github.event.label.name == 'essay' }}
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with:
        fetch-depth: 0
    - name: Get paths to changed files in the PR branch
      env:
        BRANCH_DIFF: origin/main
      run: |
        git diff-tree --no-commit-id --name-status -r $BRANCH_DIFF ${{ github.sha }} > CHANGED_FILES_PATHS.txt
    - uses: amarhod/pdf-bibliography-action@v1
      with:
        token: ${{ github.token }}
        repo_path: ./
        repo_name: ${{ github.repository }}
        pr_number: ${{ github.event.number }}
        verbosity: 2
```

**This YAML file checks the new/modified files in a PR (compared to `origin/main`) when the label `essay` is assigned. If there are new or modified PDF files in the PR, the action will try to extract the reference lists and comment on the PR with a summary**


## Example of generated comment on PR

### :blue_book: :mag_right: PDF Bibliography summary
### File: examples/example_1.pdf (reference count: 3)
```
[1] Michel Goossens, Frank Mittelbach, and Alexander Samarin. The L A TEX Companion. Addison-Wesley, Reading, Massachusetts, 1993.
[2] Albert Einstein. Zur Elektrodynamik bewegter Körper. (German) [On the electrodynamics of moving bodies]. Annalen der Physik, 322(10):891–921, 1905.
[3] Knuth: Computers and Typesetting, http://www-cs-faculty.stanford.edu/~uno/abcde.html 1
```
:x: Could not find reference list for PDF files: examples/example_2.pdf

## Unit tests
Run unit tests with:
```
python -m unittest discover tests
```
