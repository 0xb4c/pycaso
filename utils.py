"""
    pycaso - Simple OCR-based Captcha Solver
    
    Filename:       utils.py
    Date:           Sep 2022
    Author:         0xb4c
"""

from PIL import Image
import os
import pytesseract
import base64
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)

"""
Script's Banner
"""
def banner():
    print("")
    print("╔═╗┌─┐┌─┐┌┬┐┌─┐┬ ┬┌─┐  ╔═╗┌─┐┬ ┬  ┬┌─┐┬─┐")
    print("║  ├─┤├─┘ │ │  ├─┤├─┤  ╚═╗│ ││ └┐┌┘├┤ ├┬┘")
    print("╚═╝┴ ┴┴   ┴ └─┘┴ ┴┴ ┴  ╚═╝└─┘┴─┘└┘ └─┘┴└─")
    print("\x1b[31m", "           pycaso by 0xb4c", "\x1b[0m")
    print("")

"""
Checking local storage. Create if it does not exist
"""
def prepare_local_storage(directory, path):
    print("[+] Storage directory check...")
    try:
        if not os.path.exists(directory):
            print("\x1b[32m", "[->] Directory created!", "\x1b[0m")
            os.makedirs(directory)
        else:
            print("\x1b[32m", "[->] Directory existed!", "\x1b[0m")
        return True
    except Exception as e:
        print("\x1b[31m", "[->] Error!\r\n", "\x1b[0m", e)
    return False

"""
Retrieve image from an specific URL and store in local storage
"""
def retrieve(url, img_path):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    pull_image = requests.get(url, headers=headers, verify=False)
    with open(img_path, "wb+") as myfile:
        myfile.write(pull_image.content)

"""
Convert base64 string to image and store in local storage
"""
def convert(data, img_path):
    imgdata = base64.b64decode(data)
    with open(img_path, 'wb') as f:
        f.write(imgdata)
        return True
    return False

"""
Load captcha image from local storage and solve it
"""
def solve(img_path):
    code = pytesseract.image_to_string(Image.open(os.path.abspath(img_path)))
    return code

"""
Plot captcha image
"""
def plot_captcha(path):
    x = input("[+] Plot captcha image? (N/y): ")
    if ((x == 'y') | (x == 'Y')):
        im = Image.open(path)
        im.show()

"""
Try to find an possible valid captcha (Try limit: 10 times)
"""
def find_possible_captcha(url, path, captcha_len):
    count = 0
    print("[+] Get image from: ", url)
    print("[+] Captcha length: ", captcha_len)
    print("[+] Solving...")
    while True:
        retrieve(url, path)
        captcha = solve(path).strip().replace(" ", "")
        if (len(captcha) == captcha_len):
            return captcha
        if (count >= 9):
            print("\x1b[34m", "[->] Try 10 times but cannot found valid captcha. Please check the input URL or the captcha length.", "\x1b[0m")
            return None
        count += 1
    return None

"""
Load base64 from file, store as an image and solve captcha
"""
def convert_base64_image(base64_path, path, captcha_len):
    captcha = None
    print("[+] Checking base64 file path...")
    if (os.path.exists(base64_path)):
        print("\x1b[32m", "[->] Valid file path!", "\x1b[0m")
    else:
        print("\x1b[31m", "[-] Error!!! File not exist!", "\x1b[0m")
        return captcha
    print("[+] Captcha length: ", captcha_len)
    print("[+] Converting base64 data to image...")
    try:
        data = ""
        with open(base64_path) as f:
            data = f.read()
        if (convert(data, path)):
            print("\x1b[32m", "[->] Stored successfully!", "\x1b[0m")
            captcha = solve(path).strip().replace(" ", "")
            if (len(captcha) == captcha_len):
                return captcha
            else:
                print("\x1b[34m", "[->] Cannot found valid captcha", "\x1b[0m")
        else:
            print("\x1b[31m", "[-] Error!!! Cannot solve captcha from your input data.", "\x1b[0m")
    except:
        print("\x1b[31m", "[-] Error!!! Please check your input.", "\x1b[0m")
    return captcha

"""
Load captcha image from specific file and solve it
"""
def solve_from_image(img_path, captcha_len):
    captcha = None
    print("[+] Checking image file path...")
    if (os.path.exists(img_path)):
        print("\x1b[32m", "[->] Valid file path!", "\x1b[0m")
    else:
        print("\x1b[31m", "[-] Error!!! File not exist!", "\x1b[0m")
        return captcha
    print("[+] Captcha length: ", captcha_len)
    print("[+] Solving captcha...")
    try:
        captcha = solve(img_path).strip().replace(" ", "")
        if (len(captcha) == captcha_len):
            return captcha
        else:
            print("\x1b[34m", "[->] Cannot found valid captcha", "\x1b[0m")
    except:
        print("\x1b[31m", "[-] Error!!! Cannot solve captcha. Please check your file again.", "\x1b[0m")
    return captcha

