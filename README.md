# Podbean page downloader

Give a podcasters url on podbean it will download bulk all the podcasts. It defaults to the first page 
(this is typically the last ten podcasts). However you can specify the number of pages you wish to go back and download. 

## Requirements

* Python 3.9.1
* pip
* virtualenv

## Installation

A package can be created by clone the repo and then running setup tools e.g.

```
$ git clone git@github.com:silktown-software/podbean_downloader.git
$ cd podbean_downloader
$ python setup.py sdist
$ cd dist
$ pip install --user podbean_downloader-0.0.1.tar.gz
```

If you don't have the python console scripts location in your path you will find a warning such as below:

```
Installing collected packages: podbean-downloader
  WARNING: The script podbean-downloader.exe is installed in 'C:\Users\<someuser>\AppData\Roaming\Python\Python39\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

You will need to add this path to be able to call the script from the command line.

## Usage

```
$ podbean-downloader -u <podbean url> -p 2
```

## TODO

Currently this only support creator pages e.g. name.podbean.com and drills down to the mp3 download page through there.
