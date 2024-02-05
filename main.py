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

    print("可选的图片：")
    for n, img in enumerate(img_list):
        print(f"{n+1} : {img}")
    selection = int(input("请选择要加载的图片："))
    return img_list[selection-1]


def load_public_key_name():
    public_key_list = []
    for file in os.listdir(key_path):
        if file.endswith("public_key.pem"):
            public_key_list.append(file)

    print("可选的公钥：")
    for  n, public_key in enumerate(public_key_list):
        print(f"{n+1} : {public_key}")
    selection = int(input("请选择要加载的公钥："))
    return public_key_list[selection-1]


def encode_message2img(private_key, public_key):
    image_name = load_img()
    encrypted_image = ImageProcessor(image_name)
    
    message = input("请输入要加密的信息：")
    encrypted_message = encrypt_with_public_key(message, public_key)
    sign = sign_message(message, private_key)

    binary_ends = encrypted_image.image_decode()

    binary_message = encode_massage(encrypted_message)
    binary_sign = encode_massage(sign)

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
    print(decrypted_message)


def OptionMenu():
    private_key = start_private_key()
    print("请选择操作：")
    print("1.加密图片")
    print("2.解密图片")
    option = int(input("请输入选项："))
    if option == 1:
        public_key_name = load_public_key_name()
        public_key = load_public_key(public_key_name)
        encode_message2img(private_key, public_key)
        print("图片保存在output文件夹")
    elif option == 2:
        public_key_name = load_public_key_name()
        public_key = load_public_key(public_key_name)
        decode_img2message(private_key, public_key)
    else:
        print("无效的选项")

def standing_by():
    input("按下任意键结束程序...")

def main():
    start_folder_check()
    config_check()
    welcome()
    OptionMenu()
    standing_by()

