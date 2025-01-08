import numpy as np
import cv2

##機能パターンを加工する
def qrarrange(qrimage):
    # モジュール一辺のピクセルサイズ．HiddenqrGenと合わせる．
    modsize = 20

    # ファインダパターンの線の太さ
    thickness = 14

    # 余白の大きさ
    margin = modsize

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

    #別画像でファインダパターンを作ってqrimageに重ねる
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

    cv2.imwrite("findpattern.png", findpattern)

    #findpatternをqrimageに重ねる
    for i in range (0, height):
        for j in range (0, width):
            if findpattern[i, j, 3] == 255 and qrimage[i, j, 3] == 0:
                for rgb in range (0,3):
                    qrimage[i][j] = findpattern[i][j]

    return qrimage


