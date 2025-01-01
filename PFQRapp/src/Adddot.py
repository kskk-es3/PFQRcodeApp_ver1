from PIL import Image, ImageTk
import cv2
import numpy as np

##QRgen → LogoinQR → Nonsystematiccode → GenlogoQR → Adddot

##情報が読み取れるようにドットを付与する

modsize = 20
margin = modsize

# qr = cv2.imread("nonsystematicQR.png", cv2.IMREAD_GRAYSCALE)
qr = cv2.imread("qr.bmp", cv2.IMREAD_GRAYSCALE)
logoqr = cv2.imread("logoQRcode.bmp")
mask = cv2.imread("mask.bmp", cv2.IMREAD_GRAYSCALE)
funmask = cv2.imread("funmask.bmp", cv2.IMREAD_GRAYSCALE)
logomask = cv2.imread("logo_mask_resize.png", cv2.IMREAD_GRAYSCALE)


#3枚とも同じ大きさのはずなのでそれぞれの縦横の長さ変数は統一
height, width = qr.shape[:2]

#ドットを保存するための画像．最初はすべてのピクセル透過
dot = np.ones((height, width, 3),np.uint8)*255
dot = cv2.cvtColor(dot, cv2.COLOR_BGR2BGRA)
for i in range (0, height):
    for j in range (0, height):
        dot[i][j][3] = 0


#ロゴ入りQRコードを二値化する
#グレースケールに変換　Y←0.299⋅R+0.587⋅G+0.114⋅B
logoqr_gray = cv2.cvtColor(logoqr, cv2.COLOR_BGR2GRAY)

# 閾値の設定
threshold = 126

# 二値化(閾値126を超えた画素を255にする。)
ret, logoqr_bin = cv2.threshold(logoqr_gray, threshold, 255, cv2.THRESH_BINARY)

#ロゴ入りQRコードにドットを付与する
#マスク部分においてロゴ入りと元のQRコードのモジュールを比較して明暗が異なればドットを付与する


dotsize = 8

# #データのみにドットを付与
# dotcount = 0
# for i in range (margin, height - margin, modsize):
#     for j in range (margin, width - margin, modsize):
#         if mask[i][j] == 0:
#             blackpixel = 0
#             whitepixel = 0
#             for x in range (i + modsize//3, i + 2*modsize//3,):
#                 for y in range (j + modsize//3, j + 2*modsize//3):
#                     if (logoqr_bin[x][y] == 0):
#                         blackpixel += 1
#                     else:
#                         whitepixel += 1

#             #元のQRが白なのにロゴが黒
#             if(blackpixel >= whitepixel)and(qr[i + modsize//2][j + modsize//2] >= 126):
#                 cv2.rectangle(logoqr, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (255,255,255), thickness=-1)
#                 cv2.rectangle(dot, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (255,255,255,255), thickness=-1)
#                 dotcount += 1

#             #元のQRが黒なのにロゴが白
#             elif(blackpixel < whitepixel)and(qr[i + modsize//2][j + modsize//2] < 126):
#                 cv2.rectangle(logoqr, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (0,0,0), thickness=-1)
#                 cv2.rectangle(dot, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (0,0,0,255), thickness=-1)
#                 dotcount += 1

# ##ロゴ部分のモジュールの中心において，モジュールの中心が白黒判定が難しい場合にドットを付与
# ##ドットの色の決定、二値化した時に白にしたい場合はロゴのドット部分のピクセルを調べ、126以上のピクセルの平均を取りドットの色とする
# ##黒の場合は126より小さいピクセルを調べる
# dotcount = 0
# for i in range (margin, height - margin, modsize):
#     for j in range (margin, width - margin, modsize):
#         if not funmask[i][j] == 0:
#         # if not (logomask[i + modsize//3][j + modsize//3] == 0 or logomask[i + 2*modsize//3][j + 2*modsize//3] == 0):
#             if logomask[i + modsize//2][j + modsize//2] == 0:
#                 blackpixel = 0.0
#                 whitepixel = 0.0

#                 blackred = 0
#                 blackgreen = 0
#                 blackblue = 0

#                 whitered = 0
#                 whitegreen = 0
#                 whiteblue = 0
#                 for x in range (i + modsize//3, i + 2*modsize//3,):
#                     for y in range (j + modsize//3, j + 2*modsize//3):
#                         if (logoqr_bin[x][y] == 0):
#                             blackpixel += 1
#                             blackred = blackred + logoqr[x][y][0]
#                             blackgreen = blackgreen + logoqr[x][y][1]
#                             blackblue = blackblue + logoqr[x][y][2]
#                         else:
#                             whitepixel += 1
#                             whitered = whitered + logoqr[x][y][0]
#                             whitegreen = whitegreen + logoqr[x][y][1]
#                             whiteblue = whiteblue + logoqr[x][y][2]

#                 ratio = blackpixel/(blackpixel+whitepixel)

#                 if  (0.3 <= ratio and ratio < 0.7):
#                     if qr[i + modsize//2][j + modsize//2] >= 126:

#                         whitered = whitered/whitepixel
#                         whitegreen = whitegreen/whitepixel
#                         whiteblue = whiteblue/whitepixel

#                         cv2.rectangle(logoqr, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (whitered,whitegreen,whiteblue), thickness=-1)
#                         cv2.rectangle(dot, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (whitered,whitegreen,whiteblue,255), thickness=-1)
#                         dotcount += 1
                    
#                     elif qr[i + modsize//2][j + modsize//2] < 126:

#                         blackred = blackred/blackpixel
#                         blackgreen = blackgreen/blackpixel
#                         blackblue = blackblue/blackpixel

#                         cv2.rectangle(logoqr, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (blackred,blackgreen,blackblue), thickness=-1)
#                         cv2.rectangle(dot, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (blackred,blackgreen,blackblue,255), thickness=-1)
#                         dotcount += 1

                

##すべてのモジュールにドット
dotcount = 0
for i in range (margin, height - margin, modsize):
    for j in range (margin, width - margin, modsize):

        # 元のQRが白
        if(qr[i + modsize//2][j + modsize//2] >= 126):
            cv2.rectangle(logoqr, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (255,255,255), thickness=-1)
            cv2.rectangle(dot, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (255,255,255,255), thickness=-1)
            dotcount += 1

        #元のQRが黒
        elif(qr[i + modsize//2][j + modsize//2] < 126):
            cv2.rectangle(logoqr, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (0,0,0), thickness=-1)
            cv2.rectangle(dot, (j + modsize//2 - dotsize//2, i + modsize//2 - dotsize//2), (j + modsize//2 + dotsize//2, i + modsize//2 + dotsize//2), (0,0,0,255), thickness=-1)
            dotcount += 1

print("dotnum:", dotcount)     

cv2.imwrite("dot.png", dot)
cv2.imwrite("logoQRdot.bmp", logoqr)