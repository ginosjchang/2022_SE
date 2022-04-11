import easyocr
import cv2
import re

def loadModel():
    """
    Load OCR model to memory.
    Needs to run only once before use recongnize() function.
    """
    return easyocr.Reader(['en'], gpu = True)

def recongnize(reader, img_path):
    
    img_path = img_path.strip('\'')

    img = cv2.imread(img_path)
    
    result = []
    predict1 = reader.readtext(img, allowlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') # 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ID_eng = str(predict1[0][1])

    predict2 = reader.readtext(img, allowlist = '0123456789') # 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ID_num = str(predict2[1][1])
    ID_num = ID_num.replace(" ", "") # remove space
    ID = ID_eng + ID_num
    
    score = predict2[2][1]

    result.append(ID)
    result.append(score)
    
    return result

