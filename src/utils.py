import socket
from itertools import chain

STRIP_LENGTH = 300
STRIP_INVERT = False
STRIP_PROTO_RGB = 2
STRIP_TIMEOUT = 5

STRIP_MARKER_EMPTY = 0
STRIP_MARKER_START = 10
STRIP_MARKER_END = 20
STRIP_MARKER_CHAR = 30

STRIP_RENDER_TEXT_EMPTY = "_"
STRIP_RENDER_TEXT_START = "["
STRIP_RENDER_TEXT_END = "]"
STRIP_RENDER_TEXT_CHAR = "@"

STRIP_RENDER_LED_EMPTY = (0, 0, 0)      # off
STRIP_RENDER_LED_START = (0, 255, 0)    # red
STRIP_RENDER_LED_END = (255, 0, 0)      # blue
STRIP_RENDER_LED_CHAR = (255, 255, 255) # white

MAP_WIDTH = 80
MAP_OFFSET = 10
CHAR_X = int(MAP_WIDTH / 2)

def get_x(x, width, invert=False):
    return (width - x if invert else x) - 1

def build_strip(strip_length=STRIP_LENGTH, strip_invert=STRIP_INVERT, map_width=MAP_WIDTH, map_offset=MAP_OFFSET, char_x=CHAR_X):
    map_start_x = 0 + map_offset
    map_end_x = map_start_x + map_width
    # Set X locations of Map Start/End and Character
    x_start = get_x(map_start_x, strip_length, strip_invert)
    x_end = get_x(map_end_x, strip_length, strip_invert)
    x_char = get_x(map_start_x + char_x, strip_length, strip_invert)
    # Clear strip
    strip = [STRIP_MARKER_EMPTY for i in range(0, strip_length)]
    # Populate map array
    strip[x_start] = STRIP_MARKER_END if strip_invert else STRIP_MARKER_START
    strip[x_end] = STRIP_MARKER_START if strip_invert else STRIP_MARKER_END
    strip[x_char] = STRIP_MARKER_CHAR
    return strip

def render_strip_text(strip):
    out = []
    for i in strip:
        if i == STRIP_MARKER_START:
            out.append(STRIP_RENDER_TEXT_START)
        elif i == STRIP_MARKER_END:
            out.append(STRIP_RENDER_TEXT_END)
        elif i == STRIP_MARKER_CHAR:
            out.append(STRIP_RENDER_TEXT_CHAR)
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
        elif i == STRIP_MARKER_CHAR:
            out.append(STRIP_RENDER_LED_CHAR)
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
