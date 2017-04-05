"""
    usage: modelFinder.py [INPUT_DIR] [OUTPUT_DIR]

    Recursively find all .obj or .stl files in INPUT_DIR and convert them to .xyz file then put it in OUTPUT_DIR

"""

from stltovoxel.stltovoxel import doExport
import argparse
import os.path
import io
import os
import subprocess

FNULL = open(os.devnull, 'w')


def process_obj(file_path, output_file):
    # meshlab server stuff
    # call(['meshlabserver', '-i', file_path, '-o', output_file])
    subprocess.call(['meshlabserver', '-i', file_path, '-o', output_file, '-s', 'closeHoles2.mlx'], stdout=FNULL, stderr=subprocess.STDOUT)

def process_stl(file_path, output_file):
    try:
        doExport(file_path, output_file, 100)
    except Exception as e:
        œpass
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
            if(ext in ['.stl', '.obj']):
                print("Processing: "+file_path+" ...")
                if(ext == '.obj' or True):
                    process_obj(file_path, "/tmp/" + str(next_id) + ".stl")
                    file_path = "/tmp/" + str(next_id) + ".stl"
                process_stl(file_path, os.path.join(output_dir, str(next_id)+".xyz"))
                next_id += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recursively find all .obj or .stl then convert it to .xyz')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-i', '--input', nargs='?', required=True)
    requiredNamed.add_argument('-o', '--output', nargs='?', required=True)
    args = parser.parse_args()
    find(args.input, args.output)