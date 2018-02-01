# freebible

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
