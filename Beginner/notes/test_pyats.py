from ats import topology
import re

devname = 'ASA-01'
tb = topology.loader.load('pyclass_topo.yaml')
device = tb.devices[devname]
device.connect(via='net')
output = device.execute('show cpu')
device.disconnect()
print()

mo = re.search(r'CPU utilization for 5 seconds = ([\d.]+)%', output)
load = float(mo.group(1)) if mo else ''

assert load < 90, 'device %s overloaded (%s%%)' % (devname, load)

print('All tests passed.')
