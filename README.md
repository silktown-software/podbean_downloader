# Podbean page downloader

Give a podcasters url on podbean it will download bulk all the podcasts. It defaults to the first page 
(this is typically the last ten podcasts). However you can specify the number of pages you wish to go back and download. 

## Usage

```
$ podbean-downloader -u <podbean url> -p 2
```

## Installation From Source

The python scripts are intended to be installed as an executable module.

While there is nothing operating system specific about the downloader (it is pure python code). There are some prerequisites that are required for installation from source.

### Prerequisites 

The installation has been verified using:

* `Python >= 3.9`
* `pip`
* `setuptools`

Many distros allow you to install these separately through their provided package manager. This will differ between distros.

#### **Ubuntu and derivatives**

```bash
$ sudo apt install python3 python3-pip python3-setuptools
```

**Note**: This has been tested on Ubuntu 22.04 which is currently the latest as of writing.

#### **Arch Linux**

```bash
$ sudo pacman -S python python-pip python-setuptools
```

### Building and installing the package

A package can be created by either cloning the repo and then running setuptools:

```bash
$ git clone https://github.com/silktown-software/podbean_downloader.git
$ cd podbean_downloader
```

*or* you can simply download the zip file, unzip it and then cd into it:

```bash
$ wget https://github.com/silktown-software/podbean_downloader/archive/refs/heads/master.zip
$ unzip master.zip
$ cd podbean_downloader-master
```

You can then create the package using setuptools:

```bash
$ python setup.py sdist
```

**Note:** On Ubuntu and some other distros you may need to used `python3` instead of `python`

Then you can install it:

```bash
$ pip install --user dist/podbean_downloader-0.0.1.tar.gz
```

**Note:** 

If you don't have your python user scripts directory in your path you will need to add it. You will need to add this path to be able to call the script from the command line. **NOTE:** this path is system specific.

Please see below in the [troubleshooting](#troubleshooting) section.

## Development Requirements

* `Python >= 3.9`
* `pip`
* `virtualenv`
* `setuptools` - (not strictly required but you will want it for building the dist package)

Again many distros allow you to install these separately through their provided package manager. This will differ between distros.

#### **Ubuntu and derivatives**

```bash
$ sudo apt install python3 python3-pip python3-setuptools python3-virtualenv
```

#### **Arch Linux**

```bash
$ sudo pacman -S python python-pip python-setuptools python-virtualenv
```

### Setup

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Running

While the virtualenv is active you can the downloader with the following command

```bash
$ python -m podbean_downloader
```

## Troubleshooting

### Can't find the executable / `podbean_download: command not found`

When installing the package using `pip install --user`. It will place a small bash script that will make the script appear as an executable.

If you don't have the python console scripts location in your path you will find a warning at the bottom of the output of `pip install --user`. It will look something like the following:

```
Installing collected packages: podbean-downloader
  WARNING: The script podbean-downloader.exe is installed in 'C:\Users\<youruser>\AppData\Roaming\Python\Python39\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

IF you are on Linux it may look like this:

```
WARNING: The script tqdm is installed in '/home/<youruser>/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  WARNING: The script podbean-downloader is installed in '/home/<youruser>/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

It is important to take note of this path. **You will** need to add this directory to your `PATH` as the above warning is telling you.

e.g. If we take the last example from above. It is telling you that your local bin folder is at `~/.local/bin/`.

Assuming you are using `bash` all you are required to do is add the following to the bottom of your `~/.bashrc`.

```bash
PATH="$HOME/.local/bin:$PATH"
export PATH
```