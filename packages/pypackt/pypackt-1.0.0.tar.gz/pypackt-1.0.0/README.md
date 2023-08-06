# pypackt

**pypackt** is a command line tool to easily claim daily free ebooks from [www.packtpub.com](https://www.packtpub.com/packt/offers/free-learning) into your packtpub account - my personal collection consists of over 350 books and still grows! :)

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [Support](#support)
6. [License](#license)
7. [Troubleshooting](#troubleshooting)
8. [Acknowledgements](#acknowledgements)

## Requirements
pypackt works on Linux and Windows (tested on Linux Mint 18.1 and Windows 7) and is both Python 2 and Python 3 compatible (tested on `python2.7` and `python3.5+`).

#### Dependencies:
* `Scrapy` - to interact with packtpub.com (login and ebook claim)
* `requests` - for URLs manipulation
* `python-crontab` - to add job to user's crontab

## Installation
pypackt can be easily installed using `pip`:
```
pip install -U pypackt
```

## Usage
#### Basic usage
To run pypackt simply type `pypackt` in your terminal:
```
~$ pypackt
```
If you are running pypackt for the very first time you will be asked to provide your login details to www.packtpub.com:
```
~$ pypackt
Login data for packtpub.com is not set - please set it now:
Set Packtpub login details
Login: your_email@example.com
Password:
```
_(**NOTE**: Your login details are used ONLY to login into www.packtpub.com and are stored in `user.ini` file in package installation directory)_  

If you have a working Internet connection and provided correct login details, after a moment you should see a title of the claimed ebook, for example:
```
Learning Robotics Using Python
```

#### Available commands
To see list of available commands just type `pypackt -h`:
```
usage: pypackt [-h] [-c | -l | -ls | -cr | -s]

Tool to claim your daily free eBooks at www.packtpub.com with ease.

optional arguments:
  -h, --help       show this help message and exit
  -c, --configure  Configure login and password to www.packtpub.com.
  -l, --last       Show last claimed book.
  -ls, --list      List all books claimed with pypackt.
  -cr, --cron      Add job to user's crontab to claim free ebooks daily.
  -s, --show       Show login settings.
```

## Contributing
Contributions are always welcome - just:  
1. Fork the project.  
2. Commit your changes on a feature branch.  
3. Push them.  
4. Submit a pull request.  
5. Have your changes merged :)

## Support
If you need assistance, want to report a bug or request a feature, please raise an issue [here](https://bitbucket.org/kchomski/pypackt/issues) or contact me directly at [krzysztof.chomski@gmail.com](mailto:krzysztof.chomski@gmail.com).  
Please attach `pypackt.log` file located in package installation directory if your request is bug related. 

## License
pypackt is released under the terms of the MIT License. Please refer to the `LICENSE.txt` file for more details.

## Troubleshooting  
On Windows you can encounter some problems during the installation process, which are - luckily - quite easy to solve:

**Problem**:
```
error: Microsoft Visual C++ 9.0 is required. Get it from http://aka.ms/vcpython27
```
**Solution**:  
Open URL mentioned in the error message and install Microsoft Visual C++ Compiler for Python 2.7.

**Problem**:
```
Unhandled error in Deferred:
```
**Solution**:  
It's a problem related to `win32api`. To solve it just install:  
```
pip install -U pypiwin32
```

**Problem**:
```
error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools":  
http://landinghub.visualstudio.com/visual-cpp-build-tools
```
**Solution**:  
Again - follow URL from error message, download and install Microsoft Visual C++ Build Tools.

## Acknowledgements
Great thanks to [Packtpub.com](https://www.packtpub.com/) for sharing free ebooks every day!
