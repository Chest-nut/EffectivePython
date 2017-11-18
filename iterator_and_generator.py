weather_data = {'广州': '25-30°C', '梅州': '20-25°C',
                '深圳': '15-20°C', '北京': '5-10°C', }

from collections import Iterable, Iterator
from copy import deepcopy


class WeatherIterator(object):
    """迭代器:不可重复迭代"""
    def __init__(self, cities):
        self.cities = cities
        self.index = 0

    def get_weather(self, city):
        return weather_data[city]

    def __next__(self):
        if self.index == len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        weather = self.get_weather(city)
        self.index += 1
        return weather

    def __iter__(self):
        return self


class WeatherIterable(object):
    """可迭代对象:可重复迭代"""
    def __init__(self, cities):
        self.cities = cities

    def __iter__(self):
        return WeatherIterator(self.cities)


class PrimeNumbers(object):
    """使用生成器返回[start, end]区间的素数"""
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_prime_num(self, num):
        if num < 4:
            return False
        for i in range(2, num):
            if num % i == 0:
                return False
        return True

    def __iter__(self):
        for k in range(self.start, self.end+1):
            if self.is_prime_num(k):
                yield k

def test1():
    print(weather_data, '\n')

    print('迭代器:不可重复迭代')
    w = WeatherIterator(['北京', '梅州'])
    print('第一次迭代:')
    for i in w:
        print(i)
    print('第二次迭代:')
    for i in w:
        print(i)

    print('\n可迭代对象:可重复迭代')
    w = WeatherIterable(['北京', '梅州'])
    print('第一次迭代:')
    for i in w:
        print(i)
    print('第二次迭代:')
    for i in w:
        print(i)


if __name__ == '__main__':
    # test1()
    g = PrimeNumbers(1, 10)
    for i in g:
        print(i)
    for i in g:
        print(i)