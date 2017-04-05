import time


def save_voxels_xyz(voxels):
    with open(filepath, 'w') as outfile:
        s = voxels.shape
        a0 = s[0]
        a1 = s[1]
        a2 = s[2]

        for x in range(a0):
            for y in range(a1):
                for z in range(a2):
                    if a[x][y][z] > 0.5:
                        outfile.write(str(x)+" "+str(y)+" "+str(z))
                    

def save_coordinates_xyz(coords):
    files = {}
    timestr = time.strftime("%Y%m%d-%H%M%S")
    if len(coords.shape) == 3:
        index = 0
        for f in coords: 
            files[timestr+"."+str(index)] = f
    elif len(coords.shape) == 2:
        f[timestr] = coords
    
    for file, data in f:
        with open(file+".xyz", 'w') as outfile:
            for coord in data:
                data = ""
                for c in coord:
                    data += str(c)
                outfile.write(data)
        