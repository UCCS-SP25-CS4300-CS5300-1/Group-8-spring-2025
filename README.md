# Group-8-spring-2025

## Pip Requirements Management
To install requirements.txt:

```bash
source venv_myenv/bin/activate
pip install -r requirements.txt
```

This will individually install each listed package at the listed versions.

If you install new packages into the virtual environment, please re-export the requirements.txt:

```bash
pip freeze > requirements.txt
```

This way we can ensure all our environments are using the same dependencies.

