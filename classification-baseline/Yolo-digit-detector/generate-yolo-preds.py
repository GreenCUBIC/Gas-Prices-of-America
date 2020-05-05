import os
import numpy as np

THRESHOLDS = list(np.arange(0.01, 0.20, 0.01)) + list(np.arange(0.30, 1.10, 0.10))
print(THRESHOLDS)
for i in THRESHOLDS: 
    cmd = 'python detect-gb.py -i ../../dataverse/sample/sample-imgs/ -p ../yolo-benchmark/imgs/ -o ../yolo-benchmark/yolo-predictions/yolo-{}.json -t {}'.format(i,i)
    print(cmd)
    os.system(cmd)
