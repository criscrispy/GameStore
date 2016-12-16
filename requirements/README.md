# Python Requirement Files
Separation between requirements for production and development environments.

[Requirement File Format](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format)

## Virtualenv
Install and activate

```bash
virtualenv -p <path to python interpreter> ENV
sourse ENV/bin/activate
pip install -r requirements.txt
Deactivating the environment
```

To deactivate use

```bash
deactivate
```
