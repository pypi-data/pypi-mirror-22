### OVERVIEW
`scriptcrypt` is a database/notebook program for user programs and associated scripts.

It provides two functions:

1. A structured view of user defined program entries
1. Ability to easily install/remove listed entries via user specified script (using specified shell)

Each entry of the program database consists of:

- Unique name
- Category
- Subcategory
- Brief description
- Install script
- Remove script

### INSTALLATION
To install `scriptcrypt` you have to have these installed:

- `pip3`
- `setuptools`

On the debian-like system you may obtain those by issuing the following commands:

`sudo apt-get install python3-pip`

`sudo pip3 install -U pip`

`sudo pip3 install setuptools`

Finally, to install `scriptcrypt` system-wide:

`sudo pip3 install scriptcrypt`

Or for current user only:

`pip3 install --user scriptcrypt`

If you installing scriptcrypt for the specific user, you may have to modify your system `$PATH` variable to add `~/.local/bin` folder to it.

### OPTIONS
`scriptcrypt` provides some useful options:

`scriptcrypt --db` sets the path to the database

`scriptcrypt --editor` and `scriptcrypt --viewer` set the TUI text editor and pager

`scriptcrypt --appdir` sets the environmental variable `$APPDIR` for use in user defined scripts. 

### --POPULATE OPTIONS

`scriptcrypt --populate-db` copies a predefined database for the user usage

`scriptcrypt --populate-bash` copies bash-completion script to the user local `bash-completion` folder

`scriptcrypt --populate-zsh` copies zsh-completion script to the user local completion folder.

Note that this function only works if you use `oh-my-zsh` zsh settings framework as it uses '~/oh-my-zsh/completion' folder.
If you want to use zsh completion without installing `oh-my-zsh`, you need to either copy `_scriptcrypt` completion file to one of the `/usr/share/zsh/functions/Completion` folders or add `_scriptcrypt` containing folder to zsh `$fpath` variable.

### KNOWN ISSUES

- using `backspace` or similar when editing entries containing Unicode characters may have unexpected results. When this happens `scriptcrypt` falls back to the empty strings

### ADDITIONS

`json2db.py` and `db2json.py`  scripts may be useful if out want to convert database to json fine and visa-versa




