import os

SCHEMA = 'c10' # 'r10'

NUM_ITERATIONS = 100
for i in range(NUM_ITERATIONS): os.system('python random-model.py -i ../../dataverse/sample/sample-imgs/  -o ../yolo-benchmark/random-predictions/{}/random-{}.json -s {}'.format(SCHEMA, i, SCHEMA))
