# freebible library

Free holy bibles data and toolkit for Python developers

## Project Home Page

https://github.com/neocl/freebible

## Installation

freebible package is available on PyPI, so it can be installed via pip by using

```bash
pip install freebible
# or even better
python3 -m pip install freebible
```

Please note that freebible requires **Python 3**. It does not work on ~~Python 2~~ anymore. 

## Sample code

### Accessing Kougo

```python
>>> from freebible import read_kougo
>>> kougo = read_kougo()
>>> print(len(kougo))
66
>>> print(kougo['John'])
[104] ヨハネ傳福音書
>>> print(len(kougo['John']))
21
>>> print(kougo['John'][1])
Chapter(ID='1')
>>> print(kougo['John'][1][1])
[John 1:1] 太初に言あり、言は神と偕にあり、言は神なりき。
```

### Accessing World English Bible (WEB)

```python
>>> from freebible import read_web
>>> web = read_web()
>>> print(len(web))
66
>>> print(web['John'])
[43] John
>>> print(len(web['John']))
21
>>> print(web['John'][1])
Chapter(ID='1')
>>> print(len(web['John'][1]))
51
>>> print(web['John'][1][1])
[John 1:1] In the beginning was the Word, and the Word was with God, and the Word was God.
```

## Developer setup

If you want to contribute to the source code, you can setup the development environment like this
```bash
# Create a virtual environment to install packages
python3 -venv ~/.envfreebible
# Activate the virtual environment
. ~/.envfreebible/bin/activate

# Check out the source code to your machine
git clone https://github.com/freebible freebible-project
cd freebible-project
# Install required packages
python3 -m pip install -r requirements.txt

# Run the demo to make sure that this source code work
python3 demo.py
```

## Bible sources:

Japanese Colloquial 口語訳: http://jco.ibibles.net/

World English Bible: https://github.com/scrollmapper/bible_databases
