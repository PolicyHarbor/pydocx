######
PyDocX - Cert Automation Fork
######

### To develop locally
* Check out the repo
* create a virtual env: `python3 -m venv ./venv`
* install the library as editable: `pip install -e .`

### To run build tests/docs/linting
* install `tox`: `pip install tox`
* run tox: `tox`

### To do a release:
* PR merge into master (remember to increment version number)
* tag in GitHub with inremented version number
* Update requirements.txt in project that uses this repo
