# ------------------------------------------------------------------------------
# Easy mode
# ------------------------------------------------------------------------------

from freebible import bibles

# Quote everything
bibles.print("Gen")
bibles.print("Gen", 1)
bibles.print("Gen", 1, 1)

# Quote from a specific bible
bibles.kougo.quote("John")  # this returns a book object
bibles.kougo.quote("John", 1)  # this returns a chapter object
bibles.kougo.quote("John", 1, 1)  # this returns a verse object
bibles.web.quote("John")
bibles.web.quote("John", 1)
bibles.web.quote("John", 1, 1)

# ------------------------------------------------------------------------------
# Advanced access
# ------------------------------------------------------------------------------
from freebible import read_kougo, read_web

kougo = read_kougo()
print("Japanese Colloquial Bible - 口語訳")
print("-" * 20)
kougo.summarise()
print()

# Demo reading WEB
print("World English Bible")
print("-" * 20)
web = read_web()
web.summarise()
print()

# demo quoting
kg_john = kougo['John']
print("Kougo\\{}: {} chapters".format(kg_john, len(kg_john)))
web_john = web['John']
print("WEB\\{}: {} chapters".format(web_john, len(web_john)))
print()

print("Quoting bibles")
print("-" * 20)
print(web['John'][1][1])
print(kougo['John'][1][1])
