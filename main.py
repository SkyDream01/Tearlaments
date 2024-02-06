from constants import *
from RSA import *
from config import *
from image import *
from message import *

import os


# 开始文件夹检测
def start_folder_check():
    for check_folder in all_folders:
        if not os.path.exists(check_folder):
            # 如果文件夹不存在，创建文件夹
            os.makedirs(check_folder)

def welcome():
    print(welcome_message)




def load_img():
    img_list = []
    for file in os.listdir(input_path):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".bmp") or file.endswith(".tif"):
            img_list.append(file)

    print("\nOptional pictures:")
    for n, img in enumerate(img_list):
        print(f"{n+1} : {img}")
    selection = int(input("Please select the image to load:"))
    return img_list[selection-1]


def load_public_key_name():
    public_key_list = []
    for file in os.listdir(key_path):
        if file.endswith("public_key.pem"):
            public_key_list.append(file)

    print("\nOptional public key:")
    for  n, public_key in enumerate(public_key_list):
        print(f"{n+1} : {public_key}")
    selection = int(input("Please select the public key to load:"))
    return public_key_list[selection-1]


def encode_message2img(private_key, public_key):
    image_name = load_img()
    encrypted_image = ImageProcessor(image_name)
    
    message = input("\nPlease enter the information you want to encrypt:\n")
    encrypted_message = encrypt_with_public_key(message, public_key)
    sign = sign_message(message, private_key)

    binary_ends = encrypted_image.image_decode()

    binary_message = encode_massage(encrypted_message)
    binary_sign = encode_massage(sign)

    if binary_ends.size < len(binary_message) + len(binary_sign) + 16 + 64:
        print("The image capacity is insufficient. Please select another image")
        standing_by()
        os._exit(0)

    binary_ends = overwrite_binary(binary_ends, binary_message, binary_sign)

    encrypted_image.image_encode(binary_ends)


def decode_img2message(private_key, public_key):
    image_name = load_img()
    decrypted_image = ImageProcessor(image_name)

    binary_ends = decrypted_image.image_decode()

    binary_message, binary_sign =read_binary_message(binary_ends)

    encrypted_message = decode_massage(binary_message)
    sign = decode_massage(binary_sign)
    decrypted_message = decrypt_with_private_key(encrypted_message, private_key)
    verify_signature(decrypted_message, sign, public_key)
    print("\nThe encrypted message is:")
    print(decrypted_message)


def OptionMenu():
    private_key = start_private_key()
    print("\nPlease select an action:")
    print("1. Encrypt the picture")
    print("2. Decrypt the picture")
    option = int(input("Please enter options:"))
    if option == 1:
        public_key_name = load_public_key_name()
        public_key = load_public_key(public_key_name)
        encode_message2img(private_key, public_key)
        print("The pictures are saved in the 'output' folder")
    elif option == 2:
        public_key_name = load_public_key_name()
        public_key = load_public_key(public_key_name)
        decode_img2message(private_key, public_key)
    else:
        print("Invalid option")

def standing_by():
    input("\nPress any key to continue...")

def main():
    start_folder_check()
    config_check()
    welcome()
    OptionMenu()
    standing_by()

