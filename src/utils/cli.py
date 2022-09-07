import argparse

def build_arg_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-H', '--host', help='WLED hostname/IP address')
    parser.add_argument('-p', '--port', help='WLED port', type=int, default=21324)
    parser.add_argument('-w', '--width', help='LED strip width (number of LEDs)', type=int, default=60)
    parser.add_argument('-f', '--flip', help='Flip LED strip direction (invert X coordinates)', action='store_true', default=False)
    parser.add_argument('-d', '--delay', help='Delay between LED updates (milliseconds)', default=100)
    parser.add_argument('-c', '--console', help='Enable animated console output', action='store_true', default=False)
    return parser
    