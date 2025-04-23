def print_map(map):
    for row in map:
        for e in row:
            print(e, end=' ')
        print()
    print()

def column(environent, index):
    return [row[index] for row in environent]
