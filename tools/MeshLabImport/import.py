"""
    usage: modelFinder.py [INPUT_DIR] [OUTPUT_DIR]

    Recursively find all .obj or .stl files in INPUT_DIR and convert them to .xyz file then put it in OUTPUT_DIR

"""

import argparse
import io, os
import subprocess

verbose = False
script = ''

supported_ext = ['.3ds', '.aln', '.apts', '.asc', '.da', '.gts', '.obj', '.off', '.ply', '.pts', '.ptx', '.stl', '.tri', '.v3d', '.vrml', '.x3dv', '.x3d']

FNULL = open(os.devnull, 'w')

def process_meshlab(file_path, output_file):
    if not verbose:
        subprocess.call(['meshlabserver', '-i', file_path, '-o', output_file, '-s', script, '-om', 'vn'], stdout=FNULL, stderr=subprocess.STDOUT)
    else:
        subprocess.call(['meshlabserver', '-i', file_path, '-o', output_file, '-s', script, '-om', 'vn'])
    

def process_xyz(input_file, output_file):
    # center X & Z, Ys start at 0
    # scale everything uniformly so maxY == 1s
    try:
        with open(input_file) as i, open(output_file, 'w') as o:
            # bounding box
            maxd = [0,0,0]
            mind = [0,0,0]
            coords = []
            for line in i:
                data = [float(n.replace(',', '.')) for n in line.strip().split(" ")]
                if len(data) > 3:
                    maxd = [max(maxd[0], data[0]),
                            max(maxd[1], data[1]), 
                            max(maxd[2], data[2])
                            ]
                    mind = [min(mind[0],data[0]), 
                            min(mind[1],data[1]),
                            min(mind[2],data[2])
                            ]
                    coords.append(data)

            # correction on each axis
            # correction = (((maxd[0]+mind[0])/2), -mind[1], ((maxd[2]+mind[2])/2))
            scale = maxd[0]-mind[0]
            correction = (-mind[0]-scale/2, -mind[1], -mind[2]-(maxd[2]-mind[2])/2)
            # scale based on y dimensions

            for c in coords:
                data = []
                i = 0
                for v in c:
                    data.append('%.10f' % ((v+correction[i%3])/scale))
                    i+=1

                o.write(' '.join(data)+'\n')
        os.remove(input_file)
    except Exception as e:
        if(verbose):
            raise e
    finally:
        pass
    

def find(input_dir, output_dir):

    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    next_id = 0

    for root, subdirs, files in os.walk(output_dir):
        for filename in files:
            file_path = os.path.join(root, filename)

            fname, ext = os.path.splitext(file_path)
            ext = ext.lower()
            if(ext in ['.xyz', '.json']):
                next_id = max(next_id, int(os.path.basename(fname)))

    next_id += 1
    print("Next ID: "+ str(next_id))

    for root, subdirs, files in os.walk(input_dir):
        for filename in files:
            file_path = os.path.join(root, filename)

            fname, ext = os.path.splitext(file_path)
            ext = ext.lower()
            if(ext in supported_ext):
                print(format(next_id, '05d')+" : processing: "+filename+" ...")
                process_meshlab(file_path, os.path.join(output_dir, format(next_id, '05d')+".temp.xyz"))
                process_xyz(os.path.join(output_dir, format(next_id, '05d')+".temp.xyz"),os.path.join(output_dir, format(next_id, '05d')+".xyz"))
                next_id += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recursively find all meshfiles then convert it to .xyz pointcloud')
    requiredNamed = parser.add_argument_group('required named arguments')


    requiredNamed.add_argument('-s', '--script')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.set_defaults(script='import_poisson.mlx')
    parser.set_defaults(verbose=False)
    requiredNamed.add_argument('-i', '--input', nargs='?', required=True)
    requiredNamed.add_argument('-o', '--output', nargs='?', required=True)
    args = parser.parse_args()
    verbose = args.verbose
    script = args.script
    find(args.input, args.output)