def geobox2rect(geobox):
    x, y, w, h = geobox
    return x - int(w / 2), y - int(h / 2), w, h


def geobox2ptrect(geobox):
    x, y, w, h = geobox2rect(geobox)
    return x, y, x + w, y + h


def rect2geobox(x, y, w, h):
    return x + int(w / 2), y + int(h / 2), w, h


def ptrect2geobox(x1, y1, x2, y2):
    return rect2geobox(x1, y1, x2 - x1, y2 - y1)


def bbox2rect(bbox):
    return geobox2rect(bbox2geobox(bbox))


def bbox2lt(bbox):
    x1, y1, x2, y2 = geobox2ptrect(bbox2geobox(bbox))
    return x1, y1


def bbox2lb(bbox):
    x1, y1, x2, y2 = geobox2ptrect(bbox2geobox(bbox))
    return x1, y2


def bbox2rt(bbox):
    x1, y1, x2, y2 = geobox2ptrect(bbox2geobox(bbox))
    return x2, y1


def bbox2rb(bbox):
    x1, y1, x2, y2 = geobox2ptrect(bbox2geobox(bbox))
    return x2, y2


def bbox2name(bbox):
    return bbox[0]


def bbox2score(bbox):
    return bbox[1]


def bbox2geobox(bbox):
    return bbox[2]


def bbox2center(bbox):
    return bbox[2][:2]


def to_box(name, score, geobox):
    return name, score, geobox


def margin_geobox(geobox, margin_ratio):
    x, y, w, h = geobox
    w_margin = int(w * margin_ratio)
    h_margin = int(h * margin_ratio)
    return x, y, w + (2 * w_margin), h + (2 * h_margin)


def margin_box(box, margin_ratio):
    name, score, geobox = box
    geobox = margin_geobox(geobox, margin_ratio)
    return to_box(name, score, geobox)

