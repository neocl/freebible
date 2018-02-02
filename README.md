# freebible library

Free holy bibles data and toolkit for Python developers

# Installation

freebible package is available on PyPI, so it can be installed via pip by using

```
pip install freebible
```

# Sample code

## Accessing Kougo

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

## Accessing World English Bible (WEB)

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

# Bible sources:

Japanese Colloquial 口語訳: http://jco.ibibles.net/

World English Bible: https://github.com/scrollmapper/bible_databases
