# bongo-magic
This is the script used to transcribe separated GTFS data to cohesive, per-agency spreadsheets.

## Installation
Python 3.x.x and Pip are required for `bongo-magic`. Despite the length of this document, it's not as complicated as it seems. If you don't have Python 3 installed, read [these](#python_install) instructions. Otherwise, you can skip to the [installation instructions](#magic_installation).

### <a name="python_install">macOS Python 3 Environment</a>
Python 2.7 comes pre-installed on all instances of macOS. However, 2.7 is an old(er) version of Python, and support will no longer be available soon. To that end, we will install Python 3.x using [Homebrew](https://brew.sh/). Simply run

`$ brew update` &rarr; udpates Homebrew itself

`$ brew upgrade` &rarr; upgrades installed packages

`$ brew install python3` &rarr; installs Python 3.x.x

If `$ brew install python3` gives you an error saying that the bottle can't be compiled because `gcc` is not installed, run `$ xcode-select --install` to install Apple Command Line Tools (which includes `gcc`, the GNU Compiler Collection). Then, run `$ brew install python3`.

**Note:** do *not* use `sudo` when installing any Homebrew, Pip, NPM, or any other third-party packages. `/usr/local/` is for locally installed or third-party software, and the use of `sudo` can affect the read/write permissions of `usr/local` by changing its owner. When installing Homebrew, it asked for your password. This is for *temporary write permissions* to `/usr/local/`. After it's installed, Homebrew takes care of this for you by installing packages in `/usr/local/Cellar/` and then creating symlinks to executable files and placing them in `/usr/local`, whose permissions are managed by Homebrew.

**Note:** there is a difference between `python`, `python3`, `pip`, and `pip3`. `python` and `pip` run scripts and install packages for Python 2.x respectively, while `python3` and `pip3` run scripts and install packages for Python 3.x.x respectively.

After Homebrew is done, check which install of Python 3 is the system default by running `$ which python3`. It should read `/usr/local/bin/python3`. If this is not the case, simply add `/usr/local/bin` to your `PATH` variable. This can be done by editing `~/.bash_profile` or `~/.profile` like so:

```
	...
	# add to the PATH environment variable
	export PATH=$PATH:/usr/local/bin
	...
```

Then either close the current shell and open a new one, or run `$ source ~/.bash_profile`. Adding this line tells bash where to look to find executable files; it adds the default symlink location for packages installed with Homebrew, `/usr/local/bin`.

Running `$ python3` should produce a Python 3 shell, which can be exited using `exit()`.

Pip, the manager for Python's package ecosystem, comes packed with all Python installs. However, Python 2.x and Python 3.x have different managers, namely `pip` and `pip3`. Pip 3 is used for the purpose of this project, as `bongo-magic` is written in Python 3.x and is registered on the Python 3 package group. To test that Pip 3 is installed, run `$ which pip3`, which should return `/usr/local/bin/pip3`. Once you've gotten here, you're all set.

### <a name="magic_installation">Installing `bongo-magic`</a>
Installing `bongo-magic` is as simple as running `$ pip3 install bongo-magic`. Then you're done.


## Usage

`$ magic [source path] [dest path]`

There are effectively two ways to use `bongo-magic`.

1. Clone down the `planner-agency-files` repository, and cd into the repository. Once you're there, run `$ magic`, and the source + destination directories will automatically be picked out, and `bongo-magic` will store the created spreadsheets in `path/to/agencyfiles/planner-agency-files/merged`.

2. Run `$ magic /path/to/source/ /path/to/dest`, and `bongo-magic` will take the files from the specified source directory and store everything in the destination directory.


## How it Works
`bongo-magic` looks at the folder structure of the `planner-agency-files` repository, which looks like this:

```
planner-agency-files/
	|__ ...
	|__ stoptimes/
	|__ trips/
	|__ merged/
	|__ ...
```

It then takes the files from the `stoptimes` directory, which contains directories tied to each agency: `coralville`, `iowacity`, and `uiowa`. These agency directories contain csv files demarcating each route's stops correlated with timepoints. `bongo-magic` creates an Excel workbook for each agency, and then creates a new sheet for each route the agency manages. These spreadsheets are then placed in the `merged/` directory.

**Note:** the* `merged` *directory is cleaned whenever the script is run. If you want to save previously merged data, you'll have to move the desired agency spreadsheets to a different directory.