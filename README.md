<div align="center">
  <img src="image.png" alt="AutoUpdateApp Logo" width="150">
</div>

# <div align="center">AutoUpdateApp</div>

## ✅ Download & use `mylib` for updating

Create a `version.py` file in the project root and add the following:

```python
CURRENT_VERSION = "1.0.4"
REPO_URL = "https://api.github.com/repos/mdhira-ai/AutoUpdateApp/releases/latest"
```

Import the `mylib` folder into your project and call the `check_for_updates()` function from your update button.

Import `version.py` and use `CURRENT_VERSION` to display the current application version.

Check the `example` folder for the Inno Setup Compiler script.

> **Important**
>
> Never change:
>
> ```iss
> AppId={{YOUR-UNIQUE-GUID-HERE}}
> ```
>
> Only update the version number, and make sure these lines are included:
>
> ```iss
> CloseApplications=yes
> RestartApplications=yes
> ```

## ℹ️ Future Updates

- Refactor `mylib` to use OOP.
- Convert `CURRENT_VERSION` into a class method/property.
