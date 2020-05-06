import json
import os
import cv2
import random
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Runs the SVHN yolo digit detector on the dataverse images.')
parser.add_argument('-i', '--img_dir', required=True, 
                    help='Directory containing the GPA images.')
parser.add_argument('-o', '--out_file', required=True,
                    help='File to save the prediction results to.')
parser.add_argument('-s', '--schema', required=True,
                    help='Schema determining the detection strategy (c="constant", r="random"; followed by number).')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Increase output verbosity.')
args = parser.parse_args()

# Example: python random-model.py -i ../../dataverse/sample/sample-imgs/  -o ../yolo-benchmark/random-predictions/c3/random-1.json -s c1 -v

img_files = [os.path.join(args.img_dir, x) for x in os.listdir(args.img_dir)]
imgs = []
if args.verbose: print(f'Number of Imgs: {len(img_files)}')

for fname in img_files:
    img_name = fname.split('/')[-1].split('.')[0]

    # Skip the broken image
    if 'b11_218_9' in fname: continue

    if args.verbose: print('Loading {}'.format(img_name))
    img = cv2.imread(fname)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgs.append((img_name, img))

rand_preds = {}
for img in imgs:
    img_name = img[0]
    img = img[1]
    
    # Apply the selected schema
    num_rand = 0
    if 'c' in args.schema:
        num_rand = int(args.schema.replace('c',''))
    elif 'r' in args.schema:
        num_rand = random.randint(0,int(args.schema.replace('r',''))) 
    
    # Populate the output with random values
    box_out  = []
    for _ in range(num_rand): box_out.append(random.randint(0,9))
    prob_out = [1.0] * len(box_out)

    rand_preds[img_name] = {'boxes' : box_out,
                            'probs' : prob_out}
    
    if args.verbose: print("Output: {}\n{}".format(box_out, prob_out))

if args.verbose: print('Saving prediction data to file')
with open(args.out_file, 'w') as fp: json.dump(rand_preds, fp)
