import os
from click import group, argument
import ctypes

RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/librandeer.so')


@group()
def main():
    pass


@main.command()
@argument('number', type = int, default = 17)
def randomize(number: int):
    lib = ctypes.cdll.LoadLibrary(RANDEER_LIBRARY_PATH)
    lib.sample.argtypes = [ctypes.c_int64]
    lib.sample(number)
    # print(number)


if __name__ == '__main__':
    main()
