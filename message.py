import numpy as np


# 将字符串转换为二进制
def encode_massage(message):
    str_message = str(message)
    binary_message = ''.join(format(ord(char), '08b') for char in str_message)
    return binary_message


# 将二进制末尾转换为字符串
def decode_massage(binary_ends):
    message = ''
    for i in range(0, len(binary_ends), 8):
        byte = binary_ends[i:i+8]
        byte = list(map(str, byte))  # 将 byte 中的每个元素转换为字符串
        byte_value = int(''.join(byte), 2)
        message += chr(byte_value)
    return message


def overwrite_binary(binary_ends, binary_message, binary_sign):
    message_length = len(binary_message)
    sign_length = len(binary_sign)
    binary_message_length = bin(message_length)[2:].zfill(64)
    binary_sign_length = bin(sign_length)[2:].zfill(16)

    binary_ends = np.array(binary_ends)
    or_shape = binary_ends.shape
    binary_ends = binary_ends.ravel()

    binary_message_length = np.fromiter(binary_message_length, dtype=int)
    binary_sign_length = np.fromiter(binary_sign_length, dtype=int)
    binary_message = np.fromiter(binary_message, dtype=int)
    binary_sign = np.fromiter(binary_sign, dtype=int)

    # 在 binary_end 的前 64 字节写入长度标记
    binary_ends[:64] = binary_message_length
    # 将 binary_message 覆写到 binary_end，保留原来的部分
    binary_ends[64:64+len(binary_message)] = binary_message
    binary_ends[64+len(binary_message):64+len(binary_message)+16] = binary_sign_length
    binary_ends[64+len(binary_message)+16:64+len(binary_message)+16+len(binary_sign)] = binary_sign

    binary_ends = binary_ends.reshape(or_shape)
    return binary_ends


def read_binary_message(binary_ends):
    binary_ends = np.array(binary_ends)
    binary_ends = binary_ends.ravel()

    # 从 binary_end 中提取长度标记
    message_length = int("".join(str(i) for i in binary_ends[:64]), 2)
    # 从 binary_end 中提取 message
    binary_message = [int(i) for i in binary_ends[64:64+message_length]]
    # 从 binary_end 中提取签名长度标记
    sign_length = int("".join(str(i) for i in binary_ends[64+message_length:64+message_length+16]), 2)
    # 从 binary_end 中提取签名
    binary_sign = [int(i) for i in binary_ends[64+message_length+16:64+message_length+16+sign_length]]

    return binary_message, binary_sign
