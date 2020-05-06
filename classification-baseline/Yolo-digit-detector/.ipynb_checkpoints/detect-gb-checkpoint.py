import json
import cv2
from yolo.backend.utils.box import draw_scaled_boxes
import os
import yolo
from yolo.frontend import create_yolo
import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Runs the SVHN yolo digit detector on the dataverse images.')
parser.add_argument('-i', '--img_dir', required=True, 
                    help='Directory containing the GPA images.')
parser.add_argument('-p', '--pred_dir', required=True,
                    help='Directory containing the resultant images.')
parser.add_argument('-o', '--out_file', required=True,
                    help='File to save the prediction results to.')
parser.add_argument('-t', '--threshold', default=0.05, type=float, 
                    help='The yolo threshold value.')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Increase output verbosity.')
args = parser.parse_args()

# Example: python detect-gb.py -i ../../dataverse/sample/sample-imgs/ -p ../yolo-benchmark/imgs/ -o ../yolo-benchmark/yolo-predictions-0.05.json -t 0.05

yolo_detector = create_yolo("ResNet50", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], 416)
DEFAULT_WEIGHT_FILE = os.path.join(yolo.PROJECT_ROOT, "weights.h5")
yolo_detector.load_weights(DEFAULT_WEIGHT_FILE)

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

yolo_preds = {}
for img in imgs:
    img_name = img[0]
    img = img[1]
    boxes, probs = yolo_detector.predict(img, float(args.threshold))
    
    box_out  = []
    prob_out = []
    for i in range(len(boxes)):
        box_out.append(int(np.where(probs[i] == max(probs[i]))[0][0]))
        prob_out.append(float(max(probs[i])))

    yolo_preds[img_name] = {'boxes' : box_out,
                            'probs' : prob_out}
    
    image = draw_scaled_boxes(img,
                              boxes,
                              probs,
                              ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

    if args.verbose: 
        print("{}-boxes are detected.".format(len(boxes)))
        print("Probabilities: {}".format(probs))
        print("Output: {}\n{}".format(box_out, prob_out))
    plt.imsave(os.path.join(args.pred_dir, img_name + '.png'), image)

if args.verbose: print('Saving prediction data to file')
with open(args.out_file, 'w') as fp: json.dump(yolo_preds, fp)
