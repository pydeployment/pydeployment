# Using Both

Use both an environment file and the command line.

---

Command line arguments override options set in the environment file. For
example, the following two cases will yield the same build options.

**Case 1**

Contents of `.env`

```
FILENAME=myapp
APPNAME='My App'
VERSION=0.1.0
```

Command

```
pydeploy myapp.py
```

**Case 2**

Contents of `.env`

```
FILENAME=testing
VERSION=0.1.0
```

Command

```
pydeploy -f myapp -a 'My App' myapp.py
```
