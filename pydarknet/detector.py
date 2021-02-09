from .bindings import *
from ctypes import *
import cv2

__all__ = ['Detector']


class Detector:
    binder = Bindings()

    def __init__(self, cfg_filename, weights_filename, names_filename=None):
        cfe, wfe = cfg_filename.encode('utf8'), weights_filename.encode('utf8')
        self.__net = self.binder.load_network_custom(cfe, wfe, 0, 1)

        self.__names = []
        if names_filename:
            with open(names_filename) as f:
                self.__names = [s.strip() for s in f.readlines()]

        self.__input_shape = (self.binder.network_width(self.__net), self.binder.network_height(self.__net))
        self.__darknet_image = self.binder.make_image(self.__input_shape[0], self.__input_shape[1], 3)

    def __set_input_internal(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_fitted = cv2.resize(img_rgb, self.__input_shape)
        self.binder.copy_image_from_bytes(self.__darknet_image, img_fitted.tobytes())

    def __detect_internal(self, obj_thresh, hier_thresh, nms_thresh):
        num = c_int(0)
        pnum = pointer(num)
        self.binder.network_predict_image(self.__net, self.__darknet_image)
        letter_box = 0

        w, h = self.__darknet_image.w, self.__darknet_image.h
        dets = self.binder.get_network_boxes(self.__net, w, h, obj_thresh, hier_thresh, None, 0, pnum, letter_box)
        num = pnum[0]
        if nms_thresh:
            self.binder.do_nms_sort(dets, num, len(self.__names), nms_thresh)

        res = []
        for j in range(num):
            for i in range(len(self.__names)):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    name_tag = self.__names[i] if self.__names else str(i)
                    res.append((name_tag, dets[j].prob[i], (b.x, b.y, b.w, b.h)))

        res = sorted(res, key=lambda x: -x[1])
        self.binder.free_detections(dets, num)
        return res

    def __fit_scale_internal(self, detections, img):
        img_w, img_h = img.shape[1], img.shape[0]
        input_w, input_h = self.__input_shape

        def scale_box(box):
            x, y, w, h = box
            return (x / input_w) * img_w, (y / input_h) * img_h, (w / input_w) * img_w, (h / input_h) * img_h

        def convert_box_to_int(box):
            return tuple([int(v) for v in box])

        return tuple([(name, score, convert_box_to_int(scale_box(box))) for name, score, box in detections])

    def detect(self, img, obj_thresh=0.2, hier_thresh=0.5, nms_thresh=0.4, obj_filter=None):
        from .bbox import bbox2name
        self.__set_input_internal(img)
        detections = self.__detect_internal(obj_thresh, hier_thresh, nms_thresh)
        if obj_filter:
            detections = [d for d in detections if bbox2name(d) in obj_filter]
        return self.__fit_scale_internal(detections, img)
