from ctypes import *
from .types import *
import platform
import os

__all__ = ['Bindings']


def get_system_so_extension():
    dynamic_library_extensions = {'Windows': 'dll', 'Linux': 'so', 'Darwin': 'dynlib'}
    return dynamic_library_extensions[platform.system()]


class Bindings:
    def __init__(self, use_gpu=True):
        gpu_so_name = 'libdarknet-gpu'
        cpu_so_name = 'libdarknet'
        so_extension = get_system_so_extension()

        cpu_so_filename = f'.{os.path.sep}{cpu_so_name}.{so_extension}'
        gpu_so_filename = f'.{os.path.sep}{gpu_so_name}.{so_extension}'

        so_filename = cpu_so_filename
        if use_gpu:
            if os.path.exists(gpu_so_filename):
                so_filename = gpu_so_filename

        self.lib = CDLL(so_filename, RTLD_GLOBAL)

        # network_width
        self.network_width = self.lib.network_width
        self.network_width.argtypes = [c_void_p]
        self.network_width.restype = c_int

        # network_height
        self.network_height = self.lib.network_height
        self.network_height.argtypes = [c_void_p]
        self.network_height.restype = c_int

        # copy_image_from_bytes
        self.copy_image_from_bytes = self.lib.copy_image_from_bytes
        self.copy_image_from_bytes.argtypes = [IMAGE, c_char_p]

        # network_predict_ptr
        self.network_predict_ptr = self.lib.network_predict_ptr
        self.network_predict_ptr.argtypes = [c_void_p, POINTER(c_float)]
        self.network_predict_ptr.restype = POINTER(c_float)

        if use_gpu:
            # cuda_set_device
            self.cuda_set_device = self.lib.cuda_set_device
            self.cuda_set_device.argtypes = [c_int]

        # init_cpu
        self.init_cpu = self.lib.init_cpu

        # make_image
        self.make_image = self.lib.make_image
        self.make_image.argtypes = [c_int, c_int, c_int]
        self.make_image.restype = IMAGE

        # get_network_boxes
        self.get_network_boxes = self.lib.get_network_boxes
        self.get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float,
                                           POINTER(c_int), c_int, POINTER(c_int),
                                           c_int]
        self.get_network_boxes.restype = POINTER(DETECTION)

        # make_network_boxes
        self.make_network_boxes = self.lib.make_network_boxes
        self.make_network_boxes.argtypes = [c_void_p]
        self.make_network_boxes.restype = POINTER(DETECTION)

        # free_detections
        self.free_detections = self.lib.free_detections
        self.free_detections.argtypes = [POINTER(DETECTION), c_int]

        # free_ptrs
        self.free_ptrs = self.lib.free_ptrs
        self.free_ptrs.argtypes = [POINTER(c_void_p), c_int]

        # reset_rnn
        self.reset_rnn = self.lib.reset_rnn
        self.reset_rnn.argtypes = [c_void_p]

        # load_net
        self.load_network = self.lib.load_network
        self.load_network.argtypes = [c_char_p, c_char_p, c_int]
        self.load_network.restype = c_void_p

        # load_network_custom
        self.load_network_custom = self.lib.load_network_custom
        self.load_network_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
        self.load_network_custom.restype = c_void_p

        # do_nms_obj
        self.do_nms_obj = self.lib.do_nms_obj
        self.do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        # do_nms_sort
        self.do_nms_sort = self.lib.do_nms_sort
        self.do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        # free_image
        self.free_image = self.lib.free_image
        self.free_image.argtypes = [IMAGE]

        # letterbox_image
        self.letterbox_image = self.lib.letterbox_image
        self.letterbox_image.argtypes = [IMAGE, c_int, c_int]
        self.letterbox_image.restype = IMAGE

        # get_metadata
        self.get_metadata = self.lib.get_metadata
        self.get_metadata.argtypes = [c_char_p]
        self.get_metadata.restype = METADATA

        # load_image_color
        self.load_image_color = self.lib.load_image_color
        self.load_image_color.argtypes = [c_char_p, c_int, c_int]
        self.load_image_color.restype = IMAGE

        # rgbgr_image
        self.rgbgr_image = self.lib.rgbgr_image
        self.rgbgr_image.argtypes = [IMAGE]

        # network_predict_image
        self.network_predict_image = self.lib.network_predict_image
        self.network_predict_image.argtypes = [c_void_p, IMAGE]
        self.network_predict_image.restype = POINTER(c_float)

        # network_predict_image_letterbox
        self.network_predict_image_letterbox = self.lib.network_predict_image_letterbox
        self.network_predict_image_letterbox.argtypes = [c_void_p, IMAGE]
        self.network_predict_image_letterbox.restype = POINTER(c_float)
