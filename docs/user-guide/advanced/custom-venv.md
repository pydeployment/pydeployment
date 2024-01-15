# Using a Custom Virtual Environment

Use your own virtual environment.

---

By default, PyDeployment creates a virtual environment and installs PyInstaller
along with any requirements specified by the requirements file. It is possible
to instead specify your own virtual environment created by the `venv` module.
In this case, the requirements file will be ignored. To do so, provide the path
to `VENV` in the environment file or `--venv` on the command line.

Be sure that PyInstaller is installed in the virtual environment that you
specify.
