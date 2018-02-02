# freebible library

Free holy bibles data and toolkit for Python developers

# Installation

freebible package is available on PyPI, so it can be installed via pip by using

```
pip install freebible
```

# Sample code
```
from freebible import read_kougo

# read Japanese bible
kougo = read_kougo()

# display bible's information
kougo.summarise()

# to quote a verse
print(kougo['John'][1][1])
```
# Bible sources:

Japanese Colloquial 口語訳: http://jco.ibibles.net/

World English Bible: https://github.com/scrollmapper/bible_databases
