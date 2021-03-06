import lvgl as lv
import time
import rng
from .components import QrA

def feed_touch():
    point = lv.point_t()
    indev = lv.indev_get_act()
    lv.indev_get_point(indev, point)
    # now we can take bytes([point.x % 256, point.y % 256])
    # and feed it into hash digest
    t = time.ticks_cpu()
    random_data = t.to_bytes(4,'big') + bytes([point.x % 256, point.y % 256])
    rng.feed(random_data)

def feed_rng(func):
    def wrapper(o,e):
        if e == lv.EVENT.PRESSING:
            feed_touch()
        func(o,e)
    return wrapper

def on_release(func):
    def wrapper(o, e):
        if e == lv.EVENT.PRESSING:
            feed_touch()
        elif e == lv.EVENT.RELEASED:
            if QrA.isQRplaying:
                QrA.stop()
            func()
    return wrapper

def cb_with_args(callback, *args, **kwargs):
    def cb():
        if callback is not None:
            callback(*args, **kwargs)
    return cb
