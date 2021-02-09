from ctypes import *

__all__ = ['BOX', 'DETECTION', 'IMAGE', 'METADATA']


class BOX(Structure):
    _fields_ = [('x', c_float),
                ('y', c_float),
                ('w', c_float),
                ('h', c_float)]


class DETECTION(Structure):
    _fields_ = [('bbox', BOX),
                ('common', c_int),
                ('prob', POINTER(c_float)),
                ('mask', POINTER(c_float)),
                ('objectness', c_float),
                ('sort_class', c_int),
                ('uc', POINTER(c_float)),
                ('points', c_int),
                ('embeddings', POINTER(c_float)),
                ('embedding_size', c_int),
                ('sim', c_float),
                ('track_id', c_int)]


class IMAGE(Structure):
    _fields_ = [('w', c_int),
                ('h', c_int),
                ('c', c_int),
                ('data', POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [('common', c_int),
                ('names', POINTER(c_char_p))]
