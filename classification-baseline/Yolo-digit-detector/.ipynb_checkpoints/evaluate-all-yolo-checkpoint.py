import os
import numpy as np

open('../yolo-benchmark/yolo-performance.csv', 'w').write('') # Overrwrite previous

THRESHOLDS = list(np.arange(0.01, 0.20, 0.01)) + list(np.arange(0.30, 1.10, 0.10))
#THRESHOLDS = list(np.arange(0.01, 0.15, 0.01))
print(THRESHOLDS)
for i in THRESHOLDS:
    cmd = 'python evaluate-gb.py -p ../yolo-benchmark/yolo-predictions/yolo-{}.json -g ../yolo-benchmark/ground_truth.csv -o ../yolo-benchmark/yolo-performance.csv -m yolo-{} -v'.format(i,i)
    print(cmd)
    os.system(cmd)
