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
    print("img: " + img_path)
    
    
    
    print("D:\\CS\\Software_Engineering\\2022_SE\\upload\\score.jpg")
    #out = repr(img_path)
    #print(type(out))'D:\\CS\\Software_Engineering\\SW_project\\score.jpg'
    "D:\\CS\\Software_Engineering\\2022_SE\\upload\\score.jpg"
    img = cv2.imread(img_path)
    print(type(img))
    result = []
    predict1 = reader.readtext(img, allowlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') # 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ID_eng = str(predict1[0][1])

    predict2 = reader.readtext(img, allowlist = '0123456789') # 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ID_num = str(predict2[1][1])
    ID_num = ID_num.replace(" ", "") # remove space
    ID = ID_eng + ID_num
    print("ID:"+ID)
    
    score = predict2[2][1]
    #score = 90
    print(score)
    result.append(ID)
    result.append(score)
    
    return result

