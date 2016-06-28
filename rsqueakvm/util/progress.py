import os

DATA = [
    '\x0a', ' ' * 10,
    '\xe2\x96\x84\xe2\x96\x88\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x84',
    '\x2c', ' ' * 46,
    '\xe2\x96\x84\xc3\x89\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2',
    '\x96\x84', ' ' * 10, '\x0a', ' ' * 9, '\xe2\x95\x9f\xe2\x96\x80',
    ' ' * 5, '\x60\xe2\x96\x80\xe2\x96\x84', ' ' * 41,
    '\xe2\x95\x93\xe2\x96\x88\xe2\x96\x80', ' ' * 6,
    '\xe2\x95\x9a\xe2\x96\x84', ' ' * 9, '\x0a', ' ' * 9, '\xe2\x96\x8c',
    ' ' * 9, '\xe2\x96\x80\xe2\x96\x84', ' ' * 37, '\x2c\xe2\x96\x88\x60',
    ' ' * 9, '\xe2\x96\x93', ' ' * 9, '\x0a', ' ' * 8, '\x5d\xe2\x96\x8c',
    ' ' * 10, '\x27\xe2\x96\x88\xe2\x96\x84', ' ' * 34,
    '\xe2\x96\x84\xe2\x96\x80', ' ' * 11, '\xe2\x96\x93', ' ' * 9, '\x0a',
    ' ' * 8, '\xe2\x95\x98\xe2\x96\x8c', ' ' * 12, '\xe2\x95\x99\xe2\x96\x8c',
    ' ' * 31, '\xe2\x95\x93\xe2\x96\x88', ' ' * 13, '\xe2\x96\x93', ' ' * 9,
    '\x0a', ' ' * 9, '\xe2\x96\x8c', ' ' * 14, '\xe2\x96\x88\x2c', ' ' * 28,
    '\xe2\x96\x84\xe2\x96\x80', ' ' * 14, '\xe2\x96\x93', ' ' * 9, '\x0a',
    ' ' * 9, '\xe2\x96\x93', ' ' * 15, '\xe2\x96\x80\xe2\x96\x84', ' ' * 26,
    '\xe2\x96\x93\x60', ' ' * 14, '\x6a\xe2\x96\x8c', ' ' * 9, '\x0a', ' ' * 9,
    '\xe2\x95\x9f\xc2\xb5', ' ' * 15, '\xe2\x95\x99\xe2\x96\x8c', ' ' * 24,
    '\xe2\x96\x88', ' ' * 16, '\xe2\x95\x9f\xe2\x94\x80', ' ' * 9, '\x0a',
    ' ' * 10, '\xe2\x96\x8c', ' ' * 58, '\xe2\x96\x93', ' ' * 10, '\x0a',
    ' ' * 10, '\xe2\x96\x93', ' ' * 57, '\xe2\x96\x90\xe2\x96\x80', ' ' * 10,
    '\x0a', ' ' * 10, '\xe2\x95\x99\xe2\x96\x8c', ' ' * 18, '\x2c\x2c',
    ' ' * 36, '\xe2\x96\x93', ' ' * 11, '\x0a', ' ' * 11, '\xe2\x96\x88',
    ' ' * 15,
    '\xe2\x95\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93',
    '\xe2\x96\x93\xe2\x95\x95', ' ' * 11,
    '\x2c\xe2\x96\x84\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x84',
    ' ' * 15, '\xe2\x96\x90\xe2\x8c\x90', ' ' * 11, '\x0a', ' ' * 12,
    '\xe2\x96\x8c', ' ' * 13,
    '\x5d\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x80',
    ' ' * 1, '\x5e\xe2\x96\x93\xc2\xb5', ' ' * 9,
    '\xe2\x96\x84\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x80',
    '\xe2\x96\x80\xe2\x96\x93\xe2\x96\x84', ' ' * 13, '\xe2\x96\x93', ' ' * 12,
    '\x0a', ' ' * 12, '\xe2\x96\x90\xc2\xb5', ' ' * 12,
    '\xe2\x95\x9f\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\x2c',
    ' ' * 2, '\xe2\x96\x93\xe2\x96\x8c', ' ' * 9,
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x8c',
    ' ' * 2, '\xe2\x96\x90\xe2\x96\x93', ' ' * 12, '\xe2\x95\xac\xc2\xac',
    ' ' * 12, '\x0a', ' ' * 27,
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93',
    '\xe2\x96\x93\xe2\x96\x93', ' ' * 10,
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x84',
    '\xe2\x96\x84\xe2\x96\x93\xe2\x96\x8c', ' ' * 26, '\x0a', ' ' * 28,
    '\xe2\x96\x80\xe2\x96\x88\xe2\x96\x93\xe2\x96\x93\xe2\x96\x88\xe2\x96\x80',
    ' ' * 11,
    '\x60\xe2\x96\x88\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96',
    '\x93\xe2\x96\x80', ' ' * 27, '\x0a', ' ' * 48,
    '\x27\xe2\x94\x94\xe2\x94\x94', ' ' * 29, '\x0a', ' ' * 17,
    '\x2c\x2c\x2c\x2c', ' ' * 59, '\x0a', ' ' * 4,
    '\x2c\xe2\x96\x84\xe2\x96\x84\x23\xc3\x86\xe2\x96\x80\xe2\x96\x80\xe2\x96',
    '\x80\xe2\x96\x80\xe2\x96\x80\xe2\x94\x94\xe2\x94\x94\xe2\x94\x94\x7e\x2e',
    '\x2e\x2e\xe2\x94\x94\xe2\x94\x94\xe2\x94\x94\x5e\xe2\x96\x80\xe2\x96\x80',
    '\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xc3\xa0\xe2\x96\x84\xc2\xb5',
    ' ' * 3,
    '\xe2\x96\x84\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93',
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x84', ' ' * 4,
    '\x2c\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\x23\x23\x4d\xe2\x96\x80\xe2\x96',
    '\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96',
    '\x80\xe2\x96\x80\xc2\xa5\x52\xc3\xa8\xe2\x95\x97\xe2\x96\x84\xe2\x96\x84',
    '\xe2\x96\x84', ' ' * 8,
    '\x0a\x4d\xe2\x96\x80\xe2\x96\x80\x60\xe2\x94\x94', ' ' * 13,
    '\x2c\x2c\x2c\xe2\x95\x93\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\x2c\xe2\x95',
    '\x93\x2c\x2c\x2c\x2c', ' ' * 4,
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93',
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93', ' ' * 2,
    '\x60\x2e', ' ' * 22,
    '\x2e\x60\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xc3\xa0\xe2\x96\x84\xe2\x96',
    '\x84\x0a', ' ' * 10,
    '\xe2\x96\x84\xe2\x96\x84\x23\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x94',
    '\x94\xe2\x94\x94\x2e\xe2\x94\x94\x2e', ' ' * 5,
    '\x2e\x60\xe2\x94\x94\x2e\x2e\x2e', ' ' * 3,
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93',
    '\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x93\xe2\x96\x88', ' ' * 2,
    '\xe2\x95\x99\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80',
    '\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80',
    '\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\x52\xc3\xa8\xe2\x95\x97\xe2\x96\x84',
    '\xe2\x95\x93', ' ' * 12, '\x0a', ' ' * 5,
    '\x2c\xe2\x96\x84\xc3\x86\xe2\x96\x80\x60\x2e', ' ' * 9,
    '\x2c\x2c\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2\x96\x84\xe2',
    '\x96\x84\xe2\x96\x84\x2c\x2c', ' ' * 5,
    '\x5e\xe2\x96\x80\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96\x88\xe2\x96',
    '\x88\xe2\x96\x80\xe2\x94\x94', ' ' * 22,
    '\x2e\x60\xe2\x96\x80\xe2\x96\x80\xe2\x95\xa6\xe2\x96\x84',
    ' ' * 7, '\x0a', ' ' * 2, '\x2c\xe2\x96\x84\xe2\x96\x80\x60', ' ' * 9,
    '\x2c\xe2\x96\x84\xc3\x89\xe2\x96\x80\xe2\x96\x80\xe2\x94\x94\x2e',
    ' ' * 7, '\x27\xe2\x94\x94\x2e', ' ' * 16,
    '\xe2\x95\x99\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80',
    '\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80\xe2\x96\x80',
    '\x52\xe2\x95\x97\xe2\x96\x84', ' ' * 10,
    '\xe2\x95\x99\xe2\x96\x80\xe2\x96\x84\x2c', ' ' * 3, '\x0a', ' ' * 12,
    '\x2c\xe2\x96\x84\xe2\x96\x80\xe2\x94\x94', ' ' * 47,
    '\x60\xe2\x96\x80\xe2\x95\xa6\x2c', ' ' * 9, '\xe2\x94\x94\xe2\x96\x80',
    ' ' * 2, '\x0a', ' ' * 12, '\x5e', ' ' * 53,
    '\xe2\x94\x94\xe2\x96\x80\x6d', ' ' * 11,
]


class Progress(object):

    def __init__(self, stages):
        self._stages = float(stages)
        self._stage = 0
        self._total_steps = 0
        self._current_steps = 0

        self._data = ''.join(DATA)
        self._maxval = len(self._data)
        self._current_index = 0

    def next_stage(self, steps):
        self._total_steps = float(steps)
        self._current_steps = 0
        if self._stage < self._stages:
            self._stage += 1

    def _index(self):
        stage = (self._stage - 1) / self._stages
        steps = 0
        if self._total_steps > 0:
            steps = self._current_steps / self._total_steps
        return int(self._maxval * (stage + steps * 1 / self._stages))

    def update(self, new_steps=-1):
        if new_steps < 0:
            self._current_steps += 1
        else:
            self._current_steps = new_steps

        new_index = self._index()
        if self._current_index < new_index:
            os.write(2, self._data[self._current_index:new_index])
            self._current_index = new_index