import numpy as np
import ctypes


def encode_list(items: tuple):
    return np.array(items).ctypes.data_as(ctypes.POINTER(ctypes.c_long))
    # return np.array(items).__array_interface__['data'][0]
