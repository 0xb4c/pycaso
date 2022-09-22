"""
    pycaso - Simple OCR-based Captcha Solver
    
    Filename:       solver.py
    Date:           Sep 2022
    Author:         0xb4c
"""

import os
import argparse
from utils import banner, prepare_local_storage, find_possible_captcha, convert_base64_image, solve_from_image, plot_captcha

directory = "images/"
path = directory + "captcha.png"

if __name__ == '__main__':
    # Load banner
    banner()
           
    # Processing inputs 
    parser = argparse.ArgumentParser(description='pycaso - Simple OCR-based Captcha Solver.')
    parser.add_argument("-u", "--url", help="solve captcha from specif URL")
    parser.add_argument("-len", '--length', type=int, default=5, help='valid captcha length (default = 5)')
    parser.add_argument("-b", '--base64', help='solve captcha from base64 file')
    parser.add_argument("-i", "--image", help="solve captcha from specific captcha image")
    args = parser.parse_args()
    captcha_len = args.length
    if (args.url):
        if (prepare_local_storage(directory, path)):
            _url = args.url
            # Get captcha and solve
            captcha = find_possible_captcha(_url, path, captcha_len)
            if (captcha != None):
                print("\x1b[32m", "[->] Found captcha: ", "\x1b[0m", captcha)
                plot_captcha(path)
            print("[+] Quiting...")
    elif (args.base64):
        if (prepare_local_storage(directory, path)):
            b_path = args.base64
            captcha = convert_base64_image(b_path, path, captcha_len)
            if (captcha != None):
                print("\x1b[32m", "[->] Found captcha: ", "\x1b[0m", captcha)
                plot_captcha(path)
            print("[+] Quiting...")
    elif (args.image):
        i_path = args.image
        captcha = solve_from_image(i_path, captcha_len)
        if (captcha != None):
            print("\x1b[32m", "[->] Found captcha: ", "\x1b[0m", captcha)
            plot_captcha(i_path)
        print("[+] Quiting...")
    else:
        parser.print_help()
