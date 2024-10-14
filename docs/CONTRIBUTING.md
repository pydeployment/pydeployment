# Contributing to PyDeployment

Feel free to contribute to the project by sending pull requests or reporting
issues to the GitHub repository. As a simple wrapper script, PyDeployment's scope
is limited by design, so please keep that in mind when submitting requests for
features or other improvements.

## Testing the Development Version

You can install the development version from the project repository itself.
First, clone the repository and enter the project directory.

```
git clone https://github.com/pydeployment/pydeployment && cd pydeployment
```

Then, create a virtual environment.

```
python -m venv --upgrade-deps venv
```

Install the testing requirements.

```
venv/bin/pip install -r requirements_pytest.txt
```

Finally, install the project in editable mode.

```
venv/bin/pip install --editable .
```

Run any of the scripts in the `tests` directory to conduct tests on a specific
aspect of PyDeployment, or run the following command to conduct all tests.

```
venv/bin/pytest tests/
```

In order to test macOS notarization, you will need to create a file named
`.env` in the project directory with the information necessary to notarize an
application. See
[macOS Notarization](user-guide/advanced/macos-notarization.md) for details
on the necessary values.

```
CERT="Developer ID Application: Name Here (TEAMIDHERE)"
KEYC="keychain-profile-name"
```
