from top import Top


class Softirqs(Top):
    def __init__(self, filename='/proc/softirqs'):
        Top.__init__(self, filename)

    def parse(self):
        with open(self.filename) as fd:
            metrics = [line.strip().split(':') for line in fd.readlines() if ':' in line]
            return dict((k, map(int, v.strip().split())) for k, v in metrics)

    @staticmethod
    def __active_cpu_count__(data):
        return len([metric for metric in data.get('TIMER') if metric > 0])

    def eval(self):
        self.diff = dict((key, self.list_diff(data, self.previous[key])) for key, data in self.current.iteritems())

    def __repr__(self):
        net_rx = ["CPU{0}: {1}".format(cpu, softirq) for cpu, softirq in enumerate(self.diff.get('NET_RX'))]
        return "\n".join(map(str, [self.header] + net_rx))


if __name__ == '__main__':
    Softirqs().run()
