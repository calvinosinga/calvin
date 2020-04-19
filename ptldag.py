"""
creating the particle dag file -> ends with particle fields

do I need the chunkno stuff or does the .sub file handle that? -> yes if I don't want to have to wait for it
all to finish
"""
from io import open
f = open('ptl.dag','w')
n = 448
ss = '99'

for i in range(n):
    name = 'PTL_'+str(i)
    f.write(str('JOB '+name+' ptl.sub\n'))
    f.write(str('VARS '+name+' chunk=\"'+str(i)+'\" ss=\"'+ss+'\"\n'))
# output file names -> ptl_[snapshot]_[chunk].hdf5

for i in range(int(n/4)): #112
    name = 'PTLCOMBINE0_'+str(i)
    vars = 'VARS ' + name + ' run=\"mass\"'
    parent = 'PARENT'
    for j in range(4):
        vars+= ' file'+str(j)+'=\"ptl_'+ss+'_'+str(4*i+j)+'.hdf5'
        parent += ' PTL_'+str(j+4*i)
    vars+= ' output=\"ptlcombine0_'+ss+'_'+str(i)+'\"\n'
    f.write(str('JOB '+name+' combine.sub\n'))
    f.write(str(vars))
    f.write(str(parent+ ' CHILD '+name+'\n'))

# output file names -> ptlcombine0_[snapshot]_[process].hdf5
for i in range(int(n/16)):#28
    name = 'PTLCOMBINE1_'+str(i)
    vars = 'VARS ' + name + ' run=\"mass\"'
    parent = 'PARENT'
    for j in range(4):
        vars+= ' file'+str(j)+'=\"ptlcombine0_'+ss+'_'+str(4*i+j)+'.hdf5'
        parent += ' PTLCOMBINE0_'+str(j+4*i)
    vars+= ' output=\"ptlcombine1_'+ss+'_'+str(i)+'\"\n'
    f.write(str('JOB '+name+' combine.sub\n'))
    f.write(str(vars))
    f.write(str(parent+ ' CHILD '+name+'\n'))
# output file names -> ptlcombine1_[snapshot]_[process].hdf5
for i in range(int(n/16/4)):#7
    name = 'PTLCOMBINE2_'+str(i)
    vars = 'VARS ' + name + ' run=\"mass\"'
    parent = 'PARENT'
    for j in range(4):
        vars+= ' file'+str(j)+'=\"ptlcombine1_'+ss+'_'+str(4*i+j)+'.hdf5'
        parent += ' PTLCOMBINE1_'+str(j+4*i)
    vars+= ' output=\"ptlcombine2_'+ss+'_'+str(i)+'\"\n'
    f.write(str('JOB '+name+' combine.sub\n'))
    f.write(str(vars))
    f.write(str(parent+ ' CHILD '+name+'\n'))

name = 'PTLCOMBINE3'
vars = 'VARS '+name+' run=\"mass\"'
parent = 'PARENT'
for j in range(4):
    vars+= ' file'+str(j)+'=\"ptlcombine2_'+ss+'_'+str(j)+'.hdf5'
    parent += ' PTLCOMBINE1_'+str(j)
vars += ' output=\"ptlcombine3_'+ss+'.hdf5'
f.write(str('JOB '+name+' combine.sub\n'))
f.write(str(vars+'\n'))
f.write(str(parent+ ' CHILD '+name+'\n'))
# output -> ptlcombine3_99.hdf5

name= 'PTLCOMBINEFINAL'
vars = 'VARS '+name+' run=\"mass\"'
parent = 'PARENT PTLCOMBINE3 PTLCOMBINE2_4 PTLCOMBINE2_5 PTLCOMBINE2_6'
files = 'file0=\"ptlcombine3_99.hdf5\" file1=\"ptlcombine2_99_4.hdf5\" file2=\"ptlcombine2_99_5.hdf5\" file3=\"ptlcombine2_99_6.hdf5\"'

f.write(str('JOB '+name+' combine.sub\n'))
f.write(str(vars+' output=\"ptlfinal_'+ss+'.hdf5\"\n'))
f.write(str(parent+ ' CHILD '+name+'\n'))