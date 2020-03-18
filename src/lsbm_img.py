from PIL import Image
import numpy as np
from random import randint

def load_image(img):
    img = Image.open(img)
    arr = np.array(img)
    return arr.shape, arr.flatten()

def convert_digit_in_num(num):
    converted_num = ''
    for digit in str(num):
        converted_num += format(int(digit), '04b')
    return converted_num
        
def convert_image(img_to_embed):
    img_shape, img_arr = load_image(img_to_embed)
    # convert image details into 4 bits
    if len(img_shape) == 2:
        bits_to_embed = format(0, '04b')
    else:
        bits_to_embed = format(3, '04b')
    bits_to_embed += convert_digit_in_num(img_shape[0])
    bits_to_embed += format(10, '04b')
    bits_to_embed += convert_digit_in_num(img_shape[1])
    bits_to_embed += format(12, '04b')
    #print("Details len: {}".format(len(bits_to_embed)))
    # convert image pixels into 8 bits
    for pix in img_arr:
        bits_to_embed += format(pix, '09b')
    bits_to_embed += "1"
    #print("Pixels len: {}".format(len(bits_to_embed)))
    return bits_to_embed

def change_bit(img_pix, msg_bit):
    new_pix = int(img_pix[:-1] + str(msg_bit), 2)
    return new_pix

def encode_img(img_to_embed, cover_img):
    binary_img = convert_image(img_to_embed)
    shape, img = load_image(cover_img)

    sign = [-1, 1]
    for i in range(len(binary_img)):
        if (img[i]%2) != int(binary_img[i]):
            img[i] += sign[randint(0,1)]
    return Image.fromarray(np.reshape(img, shape))

def convert_digit_to_num(digit_list):
    num = ''
    for digit in digit_list:
        num+=str(digit)
    return(int(num))

def decode_img(stego_img):
    shape, img = load_image(stego_img)
    # Get embedded image details
    extract_num = ''
    img_details = []
    for i in range(len(img)):
        if len(extract_num) == 4:
            if int(extract_num, 2) == 12:
                details_stop = i
                break
            img_details.append(int(extract_num, 2))
            extract_num = ''
        extract_num += str(img[i]%2)
    img_type = img_details[0]
    img_row = convert_digit_to_num(img_details[1:img_details.index(10)])
    img_col = convert_digit_to_num(img_details[img_details.index(10)+1:])
    # Get embedded image pixels
    extract_num = ''
    img_pixels = []
    for i in range(details_stop, len(img)+1):
        if len(extract_num) == 9:
            if extract_num[0] == '1':
                break
            img_pixels.append(int(extract_num, 2))
            extract_num = ''
        extract_num += str(img[i]%2)
    #print("Pixels len: {}".format(len(img_pixels)))
    if img_type:
        return Image.fromarray(np.reshape(img_pixels, (img_row, img_col, img_type)))
    return Image.fromarray(np.reshape(img_pixels, (img_row, img_col)))

if __name__=="__main__":
    opt = input("1: Encode, 2: Decode\n")
    if opt == '1':
        cover_img = input("Enter image to be encoded(with extension): ")
        ext = "."+cover_img.split(".")[-1]
        img_to_embed = input("Enter image to encode: ")
        img = encode_img(img_to_embed, cover_img)
        img.save(input("Enter filename to save encoded image(without extension): ") + ext)
    elif opt == '2':
        img = input("Enter image to be decoded(with extension): ")
        img = decode_img(img)
        img.show()
        img.save(input("Enter filename to save encoded image(with extension): "))
