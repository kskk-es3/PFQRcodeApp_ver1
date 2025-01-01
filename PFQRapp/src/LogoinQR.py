from PIL import Image, ImageTk
import cv2
import numpy as np

##QRgen → LogoinQR → Nonsystematiccode → GenlogoQR → Adddot

##QRコードにロゴを重ねてモジュール模様に変換(重ねるだけ)

modsize = 20
margin = modsize

#ロゴを埋め込むQRコード上の座標
logoposition_offset_x = 120
logoposition_offset_y = 100

qrimage = cv2.imread("qr.bmp")
logo_origin = cv2.imread("logo_kobeuniv.png",cv2.IMREAD_UNCHANGED)
# logo_origin = cv2.imread("logo_kobeuniv_nontext.png",cv2.IMREAD_UNCHANGED)
# logo_origin = cv2.imread("morii_2.png",cv2.IMREAD_UNCHANGED)
# logo_origin = cv2.imread("morii_3.png",cv2.IMREAD_UNCHANGED)
logo_mask_origin = cv2.imread("logo_mask.png", cv2.IMREAD_UNCHANGED)
mask = cv2.imread("mask.bmp",cv2.IMREAD_GRAYSCALE)

qr_height, qr_width = qrimage.shape[:2]
logo_height, logo_width = logo_origin.shape[:2]

#アスペクト比を保持してロゴをリサイズ
resize_width = 460
resize_height = round(logo_height * (resize_width / logo_width))
resize_height = 460
logo = cv2.resize(logo_origin,dsize=(resize_width, resize_height))
logo_mask = cv2.resize(logo_mask_origin,dsize=(resize_width, resize_height))
cv2.imwrite("logoresize.bmp", logo)
cv2.imwrite("logo_mask_resize.png", logo_mask)

logo_height, logo_width = logo.shape[:2]

pixelcount = 0


#ロゴをQRコードに重ねる(余白込み)。マスク部分は除く。
for i in range (0, logo_height):
    for j in range (0, logo_width):
        if logo[i][j][3] == 255:
            pixelcount = pixelcount + 1
            if mask[i + logoposition_offset_x][j + logoposition_offset_y] == 255:
                qrimage[i + logoposition_offset_x][j + logoposition_offset_y] = [logo[i][j][0], logo[i][j][1], logo[i][j][2]]  
   

# #ロゴをQRコードに重ねる(余白なし)。マスク部分は除く。
# for i in range (0, logo_height):
#     for j in range (0, logo_width):
#         if not logo_mask[i][j][3] == 0:
#             pixelcount = pixelcount + 1
#             if mask[i + logoposition_offset_x][j + logoposition_offset_y] == 255:
#                 qrimage[i + logoposition_offset_x][j + logoposition_offset_y] = [logo[i][j][0], logo[i][j][1], logo[i][j][2]] 

ratio = (pixelcount*100) // (qr_width*qr_height)

print(ratio)

cv2.imwrite("logoinQR_color.bmp", qrimage)



#ロゴ入りQRコードを二値化する
#グレースケールに変換　Y←0.299⋅R+0.587⋅G+0.114⋅B
qrimage_gray = cv2.cvtColor(qrimage, cv2.COLOR_BGR2GRAY)

cv2.imwrite("logoinQR_gray.bmp", qrimage_gray)

# 閾値の設定
threshold = 126

# 二値化(閾値126を超えた画素を255にする。)
ret, qrimage_bin = cv2.threshold(qrimage_gray, threshold, 255, cv2.THRESH_BINARY)
cv2.imwrite("logoinQR_bin.bmp", qrimage_bin)


#重ねたロゴをモジュール模様にする
#とりあえずロゴをモジュールの格子状に区切ってモジュールの中心のピクセルをモジュールの色にする
#モジュールの中心はモジュールを3×3の格子にしたときの中心とする。中心の色はピクセルの多い方
for i in range (margin, qr_height - margin, modsize):
    for j in range (margin, qr_width - margin, modsize):
        blackpixel = 0
        whitepixel = 0
        for x in range (i + modsize//3, i + 2*modsize//3):
            for y in range (j + modsize//3, j + 2*modsize//3):
                if (qrimage_bin[x][y] == 0):
                    blackpixel += 1
                else:
                    whitepixel += 1
        
        if(blackpixel >= whitepixel):
            cv2.rectangle(qrimage_bin, (j, i), (j + modsize, i + modsize), 0, thickness=-1)
        
        else:
            cv2.rectangle(qrimage_bin, (j, i), (j + modsize, i + modsize), 255, thickness=-1)

cv2.imwrite("logoinQR_mod.bmp", qrimage_bin)


