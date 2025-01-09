import cv2
import jpype
import numpy as np
import HiddenqrPattern1


####PFQRコード生成システム，コアプログラム

#入力1 格納するURL
def PFQRmain(contents):

    #入力2 QRコード上に配置する画像のパス
    picturepath = "uploads//picture.png"

    ##QRコードを生成　QRgen.javaで処理
    #QRgenを呼び出し
    QRgen = jpype.JClass("QRgen")
    QRgen.qrgen(contents)


    ##QRコードにロゴを重ねてモジュール模様に変換(重ねるだけ)

    modsize = 20
    margin = modsize

    #ロゴを埋め込むQRコード上の座標
    pictureposition_offset_x = 120
    pictureposition_offset_y = 100

    qrimage = cv2.imread("qr.bmp")
    picture_origin = cv2.imread(picturepath)
    mask = cv2.imread("mask.bmp",cv2.IMREAD_GRAYSCALE)

    qr_height, qr_width = qrimage.shape[:2]
    picture_height, picture_width = picture_origin.shape[:2]

    #ロゴをリサイズ
    resize_width = 460
    resize_height = round(picture_height * (resize_width / picture_width))
    resize_height = 460
    picture = cv2.resize(picture_origin,dsize=(resize_width, resize_height))

    picture_height, picture_width = picture.shape[:2]

    pixelcount = 0


    #ロゴをQRコードに重ねる。マスク部分は除く。
    for i in range (0, picture_height):
        for j in range (0, picture_width):
            if mask[i + pictureposition_offset_x][j + pictureposition_offset_y] == 255:
                qrimage[i + pictureposition_offset_x][j + pictureposition_offset_y] = [picture[i][j][0], picture[i][j][1], picture[i][j][2]]  
    


    #ロゴ入りQRコードを二値化する
    #グレースケールに変換　0.299⋅R+0.587⋅G+0.114⋅B
    qrimage_gray = cv2.cvtColor(qrimage, cv2.COLOR_BGR2GRAY)

    # 閾値の設定
    threshold = 126

    # 二値化(閾値を超えた画素を255にする。)
    ret, qrimage_bin = cv2.threshold(qrimage_gray, threshold, 255, cv2.THRESH_BINARY)

    #重ねたロゴをモジュール模様にする
    #ロゴをモジュールの格子状に区切ってモジュールの中心のピクセルをモジュールの色にする
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

    cv2.imwrite("pictureinQR_mod.bmp", qrimage_bin)


    ##非組織符号化を行って，モジュール化した画像部分と格納データのモジュールはそのままで符号化領域の上下と左側に検査点を配置したQRコードを生成
    #Nonsystematiccode.javaで処理
    #Nonsystematiccodeを呼び出し
    Nonsystematiccode = jpype.JClass("Nonsystematiccode")
    Nonsystematiccode.nonsystematiccode("pictureinQR_mod.bmp")
  

    nonsytematicQR = cv2.imread("nonsystematicQR.png")


    #HiddenQRコードを生成して保存
    backimage = cv2.imread("backimage//pattern1_backimage.bmp")
    Hiddenqr = HiddenqrPattern1.HiddenQRgen(backimage, nonsytematicQR)
    Hiddenqr_nomalFP = np.copy(Hiddenqr)

    #HiddenQRコードのファインダパターン部分だけ通常の形状に戻す
    # 左上
    for i in range (0, margin + modsize * 8):
        for j in range (0, margin + modsize * 8):
            Hiddenqr_nomalFP[i][j] = nonsytematicQR[i][j]

    # 左下
    for i in range (qr_height - modsize * 8 - margin, qr_height):
        for j in range (0, margin + modsize * 8):
            Hiddenqr_nomalFP[i][j] = nonsytematicQR[i][j]
            
    # 右上
    for i in range (0, margin + modsize * 8):
        for j in range (qr_width - modsize * 8 - margin, qr_width):
            Hiddenqr_nomalFP[i][j] = nonsytematicQR[i][j]
            



    ##各QRコードにロゴを重ね、PFQRコード，ファインダーパターンが通常形状のPFQRコード，画像入りの通常QRコードを生成する。
    pixelcount = 0
    for i in range (0, picture_height):
        for j in range (0, picture_width):
            pixelcount = pixelcount + 1
            Hiddenqr[i + pictureposition_offset_x][j + pictureposition_offset_y] = [picture[i][j][0], picture[i][j][1], picture[i][j][2]] 
            
            Hiddenqr_nomalFP[i + pictureposition_offset_x][j + pictureposition_offset_y] = [picture[i][j][0], picture[i][j][1], picture[i][j][2]] 
            
            nonsytematicQR[i + pictureposition_offset_x][j + pictureposition_offset_y] = [picture[i][j][0], picture[i][j][1], picture[i][j][2]] 


    ratio = (pixelcount*100) // (qr_width*qr_height)

    print("picture area ratio:",ratio)

    cv2.imwrite("imagedata_output//PFQRcode.bmp", Hiddenqr) #出力1
    cv2.imwrite("imagedata_output//PFQRcode_nomalFP.bmp", Hiddenqr_nomalFP) #出力2
    cv2.imwrite("imagedata_output//pictureQRcode.bmp", nonsytematicQR) #出力3