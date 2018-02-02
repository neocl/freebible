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
