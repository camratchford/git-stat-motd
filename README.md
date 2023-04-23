# Git-Stat-motd

## Description

- A script meant to be executed upon session login time (via `/etc/profile.d/`, `~/.bashrc`, etc.)
- Works on Linux, Windows, and MacOS (You just need to figure out how to execute it when you want it executed)
- Prints the current status of git repositories contained in the text file you provide it as an argument.

## Requirements

Python Interpreter
- Python 3.6 or greater

Pip Packages
- `Click` 
- `Colorama` 

### Considerations:
- You can install the packages via pip on your system interpreter (not recommended)
- You can prepare a virtual environment and use its python interpreter as the path in the shebang of the script

Shebang for system interpreter
```python
#!/usr/bin/python3
```

Shebang for the venv located at `/home/ubuntu/git-stat-motd/venv`
```python
#!/home/ubuntu/git-stat-motd/venv/bin/activate
```

## Using

> Just some examples, feel free to use it however you like.


### Linux
```bash
sudo su root
cd /usr/share/bin
git clone https://github.com/camratchford/git-stat-motd.git
cd git-stat-motd
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Open up git-status-motd.py with text editor of your choice
# Change first line with:
# #!/usr/share/bin/git-stat-motd/venv/bin/python

# Create a repos.txt with text editor of your choice
# Put the absolute path of each repository you wish to receive stats for

echo "/usr/share/bin/git-stat-motd/git-stat-motd.py -r /usr/share/bin/git-stat-motd/repos.txt" \
  > /etc/profile.d/motd.sh
```

### Windows (PowerShell profile)
```powershell

cd $ENV:USERPROFILE
git clone https://github.com/camratchford/git-stat-motd.git
cd git-stat-motd
python3 -m venv venv
.\venv\scripts\pip install -r requirements.txt

# Create a repos.txt with text editor of your choice
# Put the absolute path of each repository you wish to receive stats for

$GitStatDir = "$ENV:USERPROFILE\git-stat-motd"

if (!(Test-Path $PROFILE)) {
    New-Item $PROFILE -ItemType File
}
$GitStatCmd =  "$GitStatDir\venv\scripts\python $GitStatDir\git-stat-motd.py -r $GitStatDir\repos.txt"
Add-Content -Path $PROFILE -Value $GitStatCmd
```
