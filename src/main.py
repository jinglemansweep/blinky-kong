#!/usr/bin/env python

import random
import socket
import sys
import time

from pynput import keyboard
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

from utils.cli import build_arg_parser
from utils.wled import WLEDStrip, WLEDSprite, WLEDPixel, send_wled_udp

APP_NAME = 'blinkykong'
APP_DESC = 'Blinky Kong'

KEY_LEFT = "a"
KEY_RIGHT = "d"

parser = build_arg_parser(description=APP_DESC)
args = parser.parse_args(sys.argv[1:])

console = Console()

pxr = WLEDPixel(255, 0, 0)
pxg = WLEDPixel(0, 255, 0)
pxb = WLEDPixel(0, 0, 255)

strip = WLEDStrip(width=args.width, flip=args.flip)

ply1 = WLEDSprite(pxr, 0)
ply2 = WLEDSprite(pxg, 1)

sprites = [ply1, ply2]

async def on_press(key):
    if key == KEY_LEFT:
        ply1.move(strip, -1)
    if key == KEY_RIGHT:
        ply1.move(strip, 1)
    print(key)

async def on_release(key):
    pass

keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
).start()

while True:
   
    pixels = strip.process(sprites) 
    
    if args.console:
        rendered = strip.render_console(pixels)
        console.clear(home=True)
        out = strip.render_console(pixels)
        console.print(Panel(out, width=args.width + 4))

    if args.host and args.port: 
        send_wled_udp(args.host, args.port, pixels)

    time.sleep(args.delay / 1000)

