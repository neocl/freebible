from freebible import read_kougo

kougo = read_kougo()
john = kougo['John']
print(john, len(john))
print(kougo['John'][1][1])

kougo.summarise()
