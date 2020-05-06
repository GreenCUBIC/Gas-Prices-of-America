import os

SCHEMA = 'c1'

NUM_ITERATIONS = 100
for i in range(NUM_ITERATIONS): os.system('python evaluate-gb.py -p ../yolo-benchmark/random-predictions/{}/random-{}.json -g ../yolo-benchmark/ground_truth.csv -o ../yolo-benchmark/random-performance-{}.csv -m random-{}'.format(SCHEMA,i,SCHEMA,i))
