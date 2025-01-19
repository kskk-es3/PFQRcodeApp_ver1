import numpy as np
import cv2
import random
from random import randint

# モジュール一辺のピクセルサイズ.
modsize = 20

# 余白の大きさ
margin = 3*modsize

# モジュールと機能パターンの線の太さ
thickness = 14

##HiddenQRコードのパターン1を作る(2025/1/4現在はパターン1のみ)
def HiddenQRgen(backimage, qrimage):           

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

    #機能パターン以外のQRコード部分をモジュール模様に重ねる
    for i in range (0, q_height, modsize):
        for j in range (0, q_width, modsize):
            if not ((margin <= i and i <= modsize * 7 + margin and margin <= j and j <= modsize * 7 + margin) or \
            (q_height - modsize * 8 - margin <= i and i <= q_height - margin and margin <= j and j <= modsize * 7 + margin) or \
            (margin <= i and i <= modsize * 7 + margin and q_width - modsize * 8 - margin <= j and j <= q_width - margin)):
                for x in range (i, i + modsize):
                    for y in range (j, j + modsize):
                        modimage[x][y] = [qrimage[x][y][0], qrimage[x][y][1], qrimage[x][y][2]]  



    #modimageの各モジュールを縦線の縞模様にしてbackimageに転写
    for i in range (modsize//2, b_width, modsize):
        heightcount = 0
        while heightcount < b_height:

            patterncolor = [0,0,0]
            patterncolor = modimage[heightcount][i].tolist()

            if (modimage[heightcount][i] == patterncolor).all():
                backimage[heightcount: heightcount + modsize, int(i - thickness/2): int(i + thickness/2) + 1,:] = patterncolor
            heightcount += modsize


    #ファインダパターンを生成し直したいときのみ利用
    # FindpatternGen(qrimage)

    #あらかじめ用意してあるファインダパターンを読み込む
    findpattern = cv2.imread("findpattern.png",cv2.IMREAD_UNCHANGED)

    #ファインダパターンを追加
    for i in range (0, q_height):
        for j in range (0, q_width):
            if (0 <= i and i < modsize * 8 + margin and 0 <= j and j < modsize * 8 + margin) or \
            (q_height - modsize * 8 - margin <= i and i < q_height and 0 <= j and j < modsize * 8 + margin) or \
            (0 <= i and i < modsize * 8 + margin and q_width - modsize * 8 - margin <= j and j < q_width):
                if findpattern[i][j][3] == 255:
                    backimage[i][j] = [findpattern[i][j][0], findpattern[i][j][1], findpattern[i][j][2]]

    # # 余白を追加
    if not margin == 0:
        for i in range (0, q_height):
            for j in range (0, margin):
                backimage[i,j] = 255

        for i in range (0, margin):
            for j in range (0, q_width):
                backimage[i,j] = 255

        for i in range (0, q_height):
            for j in range (q_width - margin, q_width):
                backimage[i,j] = 255

        for i in range (q_height - margin, q_height):
            for j in range (0, q_width):
                backimage[i,j] = 255 
                    
    cv2.imwrite("Hiddenqr.bmp", backimage)

    return backimage

##機能パターンを加工する(必要な時のみ利用)
def FindpatternGen(qrimage):

    qrimage = cv2.cvtColor(qrimage, cv2.COLOR_BGR2BGRA)
    height, width, channel = qrimage.shape[:3]

    #ファインダパターンの黒線模様に白部分を追加するためのリスト
    findpattern_white = []

    # # 余白を消す　
    if not margin == 0:
        for i in range (0, height):
            for j in range (0, margin):
                qrimage[i,j,3] = 0 
                findpattern_white.append((i,j))

        for i in range (0, margin):
            for j in range (0, width):
                qrimage[i,j,3] = 0 
                findpattern_white.append((i,j))

        for i in range (0, height):
            for j in range (width - margin, width):
                qrimage[i,j,3] = 0 
                findpattern_white.append((i,j))

        for i in range (height - margin, height):
            for j in range (0, width):
                qrimage[i,j,3] = 0 
                findpattern_white.append((i,j))


    # # ファインダパターンを消す

    # 左上
    for i in range (margin, margin + modsize * 8):
        for j in range (margin, margin + modsize * 8):
            if (qrimage[i,j] == (255, 255, 255, 255)).all():
                findpattern_white.append((i,j))
                qrimage[i,j,3] = 0 
            else:
                qrimage[i,j,3] = 0 

    # 左下
    for i in range (height - modsize * 8 - margin, height - margin):
        for j in range (margin, margin + modsize * 8):
            if (qrimage[i,j] == (255, 255, 255, 255)).all():
                findpattern_white.append((i,j))
                qrimage[i,j,3] = 0 
            else:
                qrimage[i,j,3] = 0 

    # 右上
    for i in range (margin, margin + modsize * 8):
        for j in range (width - modsize * 8 - margin, width - margin):
            if (qrimage[i,j] == (255, 255, 255, 255)).all():
                findpattern_white.append((i,j))
                qrimage[i,j,3] = 0 
            else:
                qrimage[i,j,3] = 0 

    # ファインダパターンを別の模様にする 

    #ファインダパターンを保存する用のnp
    findpattern = np.ones((height,width),np.uint8)*255
    findpattern = cv2.cvtColor(findpattern, cv2.COLOR_BGR2BGRA)
    for i in range (0, height):
        for j in range (0, width):
            findpattern[i, j, 3] = 0

    # 黒線　左上
    # cv2.line(findpattern, (0, 0), (modsize * 8 + margin, modsize * 8 + margin), (0, 0, 0, 255), thickness) #斜め 左上⇒右下
    # cv2.line(findpattern, ( modsize * 8 + margin, 0), (0, modsize * 8 + margin), (0, 0, 0, 255), thickness) #斜め 右上⇒左下
    cv2.line(findpattern, ((modsize * 7) // 2 + margin, 0), ((modsize * 7) // 2 + margin, modsize * 8 + margin), (0, 0, 0, 255), thickness) #縦
    cv2.line(findpattern, (0, (modsize * 7) // 2 + margin), (modsize * 8 + margin, (modsize * 7) // 2 + margin), (0, 0, 0, 255), thickness) #横



    # 黒線　右上
    # cv2.line(findpattern, (width - modsize * 8 - margin, 0), (width, modsize * 8 + margin), (0, 0, 0, 255), thickness) #斜め 左上⇒右下
    # cv2.line(findpattern, (width, 0), (width - modsize * 8 - margin, modsize * 8 + margin), (0, 0, 0, 255), thickness) #斜め 右上⇒左下
    cv2.line(findpattern, ((2 * (width - margin) - modsize * 7) // 2, 0), ((2 * (width - margin) - modsize * 7) // 2, modsize * 8 + margin ), (0, 0, 0, 255), thickness) #縦
    cv2.line(findpattern, (width - modsize * 8 - margin, (modsize * 7) // 2 + margin), (width, (modsize * 7) // 2 + margin), (0, 0, 0, 255), thickness) #横

    # 黒線　左下
    # cv2.line(findpattern, (0, height - modsize * 8 - margin), (modsize * 8 + margin, height), (0, 0, 0, 255), thickness) #斜め 左上⇒右下
    # cv2.line(findpattern, (modsize * 8 + margin, height - modsize * 8 - margin), (0, height), (0, 0, 0, 255), thickness) #斜め 右上⇒左下
    cv2.line(findpattern, ((modsize * 7) // 2 + margin, height - modsize * 8 - margin), ((modsize * 7) // 2 + margin, height), (0, 0, 0, 255), thickness) #縦
    cv2.line(findpattern, (0, (2 * (height - margin) - modsize * 7) // 2), (modsize * 8 + margin, (2 * (height - margin) - modsize * 7) // 2), (0, 0, 0, 255), thickness) #横


    # 白色部分を追加
    for i in range (len(findpattern_white)):
        if(findpattern[findpattern_white[i][0]][findpattern_white[i][1]][3] == 255):
            findpattern[findpattern_white[i][0]][findpattern_white[i][1]] = 255


    # はみ出た線を消す
    for i in range (0, height):
        for j in range (0, width):
            if not((0 <= i and i < modsize * 8 + margin and 0 <= j and j < modsize * 8 + margin) or \
            (height - modsize * 8 - margin <= i and i < height and 0 <= j and j < modsize * 8 + margin) or \
            (0 <= i and i < modsize * 8 + margin and width - modsize * 8 - margin <= j and j < width)):
                findpattern[i, j, 3] = 0
                    

    cv2.imwrite("findpattern.png", findpattern)


