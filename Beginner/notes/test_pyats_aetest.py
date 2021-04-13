from ats import aetest, topology
import re

class CommonSetup:
    @aetest.setup
    def mysetup(self, topofile, devname):
        self.devname = devname
        tb = topology.loader.load(topofile)
        device = tb.devices[devname]
        device.connect(via='net')
        self.device = device


class CommonCleanup:
    @aetest.cleanup
    def mycleanup(self):
        self.device.disconnect()


class VersionTest(aetest.Testcase, CommonSetup, CommonCleanup):
    @aetest.test
    def loadtest(self):
        output = self.device.execute('show cpu')
        mo = re.search(r'CPU utilization for 5 seconds = ([\d.]+)%', output)
        load = float(mo.group(1)) if mo else ''

        assert load < 90, '%s device overloaded (%s%%)' % (self.devname, load)

if __name__ == '__main__':
    aetest.main(topofile='pyclass_topo.yaml', devname='ASA-01')
