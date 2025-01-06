import numpy as np
import cv2
import random
from random import randint

##HiddenQRコードのパターン1を作る(2025/1/4現在はパターン1のみ)
def HiddenQRgen(backimage, qrimage):           
    # モジュール一辺のピクセルサイズ.
    modsize = 20

    # 余白の大きさ
    margin = modsize

    # モジュールの線の太さ
    thickness = 14

    # 背景の中でQRコードを配置する位置QRコードの左上の座標
    backimageoffset_x = 0
    backimageoffset_y = 0

    q_height, q_width = qrimage.shape[:2]
    b_height, b_width = backimage.shape[:2]



    ##モジュール模様作成(ファインダパターン部分の背景を作るため)
    modimage = np.ones((b_height, b_width, 3),np.uint8)*255

    for i in range(0, b_height, modsize):
        for j in range(0, b_width, modsize):
            randcolor = randint(0, 1)
            color = [0,255]
            for x in range(i, i + modsize):
                for y in range(j, j + modsize):
                    modimage[x][y] = color[randcolor]

    #余白と機能パターン以外のQRコード部分をモジュール模様に重ねる
    for i in range (margin, q_height - margin, modsize):
        for j in range (margin, q_width - margin, modsize):
            if not ((margin <= i and i <= modsize * 7 + margin and margin <= j and j <= modsize * 7 + margin) or \
            (q_height - modsize * 8 - margin <= i and i <= q_height - margin and margin <= j and j <= modsize * 7 + margin) or \
            (margin <= i and i <= modsize * 7 + margin and q_width - modsize * 8 - margin <= j and j <= q_width - margin)):
                for x in range (i, i + modsize):
                    for y in range (j, j + modsize):
                        if qrimage[x][y][3] == 255:
                            modimage[x + backimageoffset_x][y + backimageoffset_y] = [qrimage[x][y][0], qrimage[x][y][1], qrimage[x][y][2]]  



    ##modimageの各モジュールを縦線の縞模様にしてbackimageに転写
    for i in range (modsize//2, b_width, modsize):
        heightcount = 0
        while heightcount < b_height:

            patterncolor = [0,0,0]
            patterncolor = modimage[heightcount][i].tolist()

            if (modimage[heightcount][i] == patterncolor).all():
                backimage[heightcount: heightcount + modsize, int(i - thickness/2): int(i + thickness/2) + 1,:] = patterncolor
            heightcount += modsize


    #ファインダパターンを追加
    for i in range (0, q_height):
        for j in range (0, q_width):
            if (0 <= i and i < modsize * 8 + margin and 0 <= j and j < modsize * 8 + margin) or \
            (q_height - modsize * 8 - margin <= i and i < q_height and 0 <= j and j < modsize * 8 + margin) or \
            (0 <= i and i < modsize * 8 + margin and q_width - modsize * 8 - margin <= j and j < q_width):
                if qrimage[i][j][3] == 255:
                    backimage[i + backimageoffset_x][j + backimageoffset_y] = [qrimage[i][j][0], qrimage[i][j][1], qrimage[i][j][2]]
                    
    cv2.imwrite("Hiddenqr.bmp", backimage)

    return backimage