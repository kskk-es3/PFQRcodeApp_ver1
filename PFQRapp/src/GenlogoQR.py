from PIL import Image, ImageTk
import cv2
import numpy as np

##QRgen → LogoinQR → Nonsystematiccode → GenlogoQR → Adddot

##非組織符号化で生成したQRコードにロゴを重ね、読み取り可能なロゴ入りQRコードを生成する。

modsize = 20
margin = modsize
#ロゴを埋め込むQRコード上の座標
logoposition_offset_x = 120
logoposition_offset_y = 120

qrimage = cv2.imread("nonsystematicQR.png")
logo_origin = cv2.imread("logo_kobeuniv.png",cv2.IMREAD_UNCHANGED)
# logo_origin = cv2.imread("logo_kobeuniv_nontext.png",cv2.IMREAD_UNCHANGED)
# logo_origin = cv2.imread("morii_2.png",cv2.IMREAD_UNCHANGED)
# logo_origin = cv2.imread("morii_3.png",cv2.IMREAD_UNCHANGED)
logo_mask_origin = cv2.imread("logo_mask.png", cv2.IMREAD_UNCHANGED)

qr_height, qr_width = qrimage.shape[:2]
logo_height, logo_width = logo_origin.shape[:2]

#アスペクト比を保持してロゴをリサイズ
resize_width = 460
resize_height = round(logo_height * (resize_width / logo_width))
resize_height = 460
logo = cv2.resize(logo_origin,dsize=(resize_width, resize_height))
logo_mask = cv2.resize(logo_mask_origin,dsize=(resize_width, resize_height))

logo_height, logo_width = logo.shape[:2]

pixelcount = 0

#ロゴをQRコードに重ねる(余白込み)。
for i in range (0, logo_height):
    for j in range (0, logo_width):
        if logo[i][j][3] == 255:
            pixelcount = pixelcount + 1
            qrimage[i + logoposition_offset_x][j + logoposition_offset_y] = [logo[i][j][0], logo[i][j][1], logo[i][j][2]] 

# #ロゴをQRコードに重ねる(余白なし)。
# for i in range (0, logo_height):
#     for j in range (0, logo_width):
#         if not logo_mask[i][j][3] == 0:
#             pixelcount = pixelcount + 1
#             qrimage[i + logoposition_offset_x][j + logoposition_offset_y] = [logo[i][j][0], logo[i][j][1], logo[i][j][2]] 

ratio = (pixelcount*100) // (qr_width*qr_height)

print(ratio)

cv2.imwrite("logoQRcode.bmp", qrimage)

