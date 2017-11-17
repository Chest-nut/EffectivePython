from array import array

class OperateWav(object):
    def __init__(self, filename):
        self.filename = filename
        self.head = None
        self.data = None
        self.sample_nums = 0
        self._readfile()

    def _readfile(self):
        with open(self.filename, 'rb') as f:
            self.head = f.read(44)
            f.seek(0, 2)
            self.sample_nums = (f.tell()-44) // 2
            self.data = array('h', (0 for _ in range(self.sample_nums)))
            f.seek(44)
            f.readinto(self.data)

    def des_vol(self, times=10):
        """音量减小 times 倍"""
        for i in range(self.sample_nums):
            self.data[i] //= times
        with open('new_'+self.filename, 'wb') as f:
            f.write(self.head)
            self.data.tofile(f)


if __name__ == '__main__':
    o = OperateWav('demo.wav')
    o.des_vol()