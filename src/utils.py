import socket
from itertools import chain

STRIP_LENGTH = 300
STRIP_INVERT = False
STRIP_PROTO_RGB = 2
STRIP_TIMEOUT = 5

STRIP_MARKER_EMPTY = 0
STRIP_MARKER_START = 10
STRIP_MARKER_END = 20

STRIP_RENDER_TEXT_EMPTY = "_"
STRIP_RENDER_TEXT_START = "["
STRIP_RENDER_TEXT_END = "]"

STRIP_RENDER_LED_EMPTY = (0, 0, 0)   # off
STRIP_RENDER_LED_START = (0, 255, 0) # red
STRIP_RENDER_LED_END = (255, 0, 0)   # blue

MAP_WIDTH = 80
MAP_OFFSET = 10

def get_x(x, width, invert=False):
    return (width - x if invert else x) - 1

def build_strip(strip_length=STRIP_LENGTH, strip_invert=STRIP_INVERT, map_width=MAP_WIDTH, map_offset=MAP_OFFSET):
    idx_start = 0 + map_offset
    idx_end = idx_start + map_width
    strip = [STRIP_MARKER_EMPTY for i in range(0, strip_length)]
    # set map start
    start_x = get_x(idx_start, strip_length, strip_invert)
    print("start x", start_x)
    strip[get_x(idx_start, strip_length, strip_invert)] = STRIP_MARKER_END if strip_invert else STRIP_MARKER_START
    # set map end
    strip[get_x(idx_end, strip_length, strip_invert)] = STRIP_MARKER_START if strip_invert else STRIP_MARKER_END
    return strip

def render_strip_text(strip):
    out = []
    for i in strip:
        if i == STRIP_MARKER_START:
            out.append(STRIP_RENDER_TEXT_START)
        elif i == STRIP_MARKER_END:
            out.append(STRIP_RENDER_TEXT_END)
        elif i == STRIP_MARKER_EMPTY:
            out.append(STRIP_RENDER_TEXT_EMPTY)
    return "".join(out)

def render_strip_led(strip):
    out = []
    for i in strip:
        if i == STRIP_MARKER_START:
            out.append(STRIP_RENDER_LED_START)
        elif i == STRIP_MARKER_END:
            out.append(STRIP_RENDER_LED_END)
        elif i == STRIP_MARKER_EMPTY:
            out.append(STRIP_RENDER_LED_EMPTY)
    return out

def send_wled_udp(host, port, pixels, proto=STRIP_PROTO_RGB, timeout=STRIP_TIMEOUT):
    message = [proto, timeout]
    for r, g, b in pixels:
        message.append(r)
        message.append(g)
        message.append(b)
    sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytearray(message), (host, port))
