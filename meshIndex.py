with open("MESH_keyword.txt", "r") as fp:
    line = fp.readline()
    cnt = 1
    while line:
        synonym = line.split("\t")
        print(len(synonym))
        line = fp.readline()
