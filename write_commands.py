f = open("commands.txt", "w")
fileno = 50
for i in range(fileno):
    if i==fileno-1:
        f.write("python3 /lustre/cosinga/HIColor/hiptl/hiptl.py " +str(i))
    else:
        f.write("python3 /lustre/cosinga/HIColor/hiptl/hiptl.py "+str(i)+"\n")
