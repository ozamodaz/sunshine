import os
import mh_z19

mh_z19.set_serialdevice("/dev/ttyS0")

metrics_file = '/var/lib/prometheus/node-exporter/mh_z19.prom'
metrics = []


for retry in range(5):
    try:
        print('try ', retry)
        metrics.append('mh_z19_co2{location="box"} %s\n' % mh_z19.read()['co2'])
        with open(metrics_file, 'w') as f:
            f.writelines(metrics)
        break
    except:
        pass