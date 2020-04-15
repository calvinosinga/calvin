"""
todo
split into more parts -> field by field basis
handle missing files
handle missing keys -> happens on jupyterlab version as well
figure out how to see how that propagates when combining the fields
"""
import numpy as np
import h5py as hp
import sys
########## INPUTS #################
grid = (2048,2048,2048)
CHUNK = sys.argv[1]
RUN = sys.argv[2]
LUM_MIN, LUM_THRESH = -16, -20 #detection minimum and threshold for breaking into dim/bright bins, from Swanson
SNAPSHOT = 99
# RUN can be 'blue','red'
BOXSIZE = 75 #Mpc/h
def isred(gr, rband):#color definition as given in Swanson
    return gr> .9 - .03*(rband+23)
###################################
try:
    f = hp.File('fof_subhalo_tab_0'+str(SNAPSHOT)+'.'+str(CHUNK)+'.hdf5','r')
except IOError:
    print('failed to open file')
else:

    has_key = True
    if RUN=='color' or RUN=='magnitude':
        field = []
    else:
        field = np.zeros(grid, dtype=np.float32)
    
    try:
        pos = f['Subhalo']['SubhaloCM']
        mass = f['Subhalo']['SubhaloMass']
        photo = f['Subhalo']['SubhaloStellarPhotometrics']
    except KeyError:
        print('chunk was empty')
        has_key=False
    if has_key:
        edges = np.linspace(0,BOXSIZE*1000, grid[0]) #definitions of bins
        bins = np.digitize(pos,edges)
        for j,b in enumerate(bins):
            rmag = photo[j][5]
            gmag = photo[j][4]
            if RUN=='color':
                field.append(gmag-rmag)
            elif RUN=='magnitude':
                field.append(rmag)
            elif RUN=='red':
                if rmag<=LUM_MIN and isred(gmag-rmag,rmag):
                    field[b[0],b[1],b[2]]+= mass[j]
            elif RUN=='blue':
                if rmag<=LUM_MIN and not isred(gmag-rmag,rmag):
                    field[b[0],b[1],b[2]]+= mass[j]
            elif RUN=='dim':
                if rmag<=LUM_MIN and not rmag<=LUM_THRESH:
                    field[b[0],b[1],b[2]]+= mass[j]
            elif RUN=='bright':
                if rmag<=LUM_THRESH:
                    field[b[0],b[1],b[2]]+= mass[j]
            elif RUN=='nondetection':
                if not rmag<=LUM_MIN:
                    field[b[0],b[1],b[2]]+= mass[j]     
    w = hp.File('subhalo_'+str(CHUNK)+'_'+RUN+'.hdf5', 'w')
    w.create_dataset(RUN,data=field)
    
        