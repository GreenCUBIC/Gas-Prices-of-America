import json
import argparse

parser = argparse.ArgumentParser(description='Evaluates the performance of predictions for the GPA dataset.')
parser.add_argument('-p', '--pred_file', required=True,
                    help='File containing the dataset predictions.')
parser.add_argument('-g', '--gt_file', required=True,
                    help='File containing the ground truth labels.')
parser.add_argument('-m', '--model_id', required=True,
                    help='An id for the model.')
parser.add_argument('-o', '--output', required=True,
                    help='File to save the average PR predictions to.')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Increase output verbosity.')
args = parser.parse_args()

# Example: python evaluate-gb.py -p ../yolo-benchmark/yolo-predictions-0.01.json -g ../yolo-benchmark/ground_truth.csv -o ../yolo-benchmark/yolo-performance.csv -m yolo-0.01 -v

def compute_precision_and_recall(actual, pred):
    # If empty digits or gt, a division by zero results.
    if len(actual) == 0 or len(pred) == 0: return None, None
    TP = 0
    for p in pred:
        for pos, a in enumerate(actual):
            if p==a:
                TP += 1 
                del actual[pos] # can't match to the same actual digit more than once
                break # Don't want to match this prediction again
        
    FP = len(pred) - TP # subtract the number of matches from the total # pred
    FN = len(actual) # any 'actual' remaining are FN
  
    recall = float(TP)/(TP+FN)
    prec = float(TP)/(TP+FP)
    return (prec, recall)    

gts = {}
for line in open(args.gt_file, 'r').readlines(): gts[line.split(',')[0].strip().split('.')[0]] = [int(char) for char in line.split(',')[1].strip() if char != '.' and char != '-']

preds = {}
with open(args.pred_file, 'rb') as json_file: preds = json.load(json_file)

precisions = []
recalls    = []
f1s        = []
for img_id in preds:
    digits = preds[img_id]['boxes']
    gt     = gts.get(img_id.split('.')[0], None)
    if gt == None: continue

    # Compute Precision and Recall for this Image
    precision, recall = compute_precision_and_recall(gt, digits)
    
    if precision == None: continue

    if args.verbose: print('Precision: {}\tRecall: {}'.format(precision, recall))
    precisions.append(precision)
    recalls.append(recall)

if args.verbose: print('Average Precision: {}'.format(sum(precisions) / len(precisions)))
if args.verbose: print('Average Recall: {}'.format(sum(recalls) / len(recalls)))

open(args.output, 'a').write('{},{},{}\n'.format(args.model_id, sum(precisions) / len(precisions), sum(recalls) / len(recalls)))
