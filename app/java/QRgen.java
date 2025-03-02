import java.awt.image.BufferedImage;
import java.io.File;
import java.util.EnumMap;
import java.util.Map;

import javax.imageio.ImageIO;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.Binarizer;
import com.google.zxing.BinaryBitmap;
import com.google.zxing.ChecksumException;
import com.google.zxing.LuminanceSource;
import com.google.zxing.EncodeHintType;
import com.google.zxing.FormatException;
import com.google.zxing.NotFoundException;
import com.google.zxing.Result;
import com.google.zxing.aztec.detector.Detector;
import com.google.zxing.client.j2se.MatrixToImageWriter;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.common.DetectorResult;
import com.google.zxing.qrcode.QRCodeReader;
import com.google.zxing.qrcode.QRCodeWriter;
import com.google.zxing.qrcode.decoder.BitMatrixParser;
import com.google.zxing.qrcode.decoder.DataBlock;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;

public class QRgen {
    public static void qrgen(String contents) {
        //// URLを受け取ってQRコードを生成する
        
		System.out.println(contents);

		int version = 5;
		ErrorCorrectionLevel EClevel = ErrorCorrectionLevel.L;

		int mask_pattern = 0;
		int margin = 3;
		int modulesize = 20; //適宜変更
		int dimension = modulesize * (17 + 4 * version + 2 * margin);
		try {
			Map<EncodeHintType, Object> hints = new EnumMap<>(EncodeHintType.class);
			hints.put(EncodeHintType.QR_VERSION, version);
			hints.put(EncodeHintType.ERROR_CORRECTION, EClevel);
			hints.put(EncodeHintType.QR_MASK_PATTERN, mask_pattern);
			hints.put(EncodeHintType.MARGIN, margin);
			QRCodeWriter writer = new QRCodeWriter();
			BitMatrix bitMatrix = writer.encode(contents, BarcodeFormat.QR_CODE, dimension, dimension, hints);
			BufferedImage image = MatrixToImageWriter.toBufferedImage(bitMatrix);
			ImageIO.write(image, "BMP", new File("app/qr.bmp"));

			
		
			//contentsのシンボル数をカウント
			Analysis analysis = new Analysis();
			byte[] allcodeword = analysis.codeword(contents);
			byte[] contentdata = analysis.datacodeword(contents);
			System.out.println("codewordnum:" + allcodeword.length);
			System.out.println("contentsize:" + contentdata.length);

			DataBlock[] datablocks = analysis.symbolgen(image);

			int rsblocknum = datablocks.length;

			System.out.println("Blocknum:" + datablocks.length);
			for(int i = 0; i < datablocks.length; i++){
				byte[] data = datablocks[i].getCodewords();
				System.out.println("datablock"+ i + ":" + "(" + data.length + "," + datablocks[i].getNumDataCodewords() + ")");

			}

			int largecodenum = 0;
			boolean largecodecheck = false;
			for (int i = 1; i < datablocks.length; i++){
				if (datablocks[i].getNumDataCodewords() != datablocks[i-1].getNumDataCodewords()){
					largecodecheck = true;
				}
				if (largecodecheck == true){
					largecodenum++;
				}
			}
			int smallcodenum  = datablocks.length - largecodenum;

			System.out.println("largecodenum:" + largecodenum);
			

			//資料としてシンボルを図示した図を生成
			
			//１モジュール1bitのbitmatrixを生成
			Map<EncodeHintType, Object> hints2 = new EnumMap<>(EncodeHintType.class);
			hints2.put(EncodeHintType.QR_VERSION, version);
			hints2.put(EncodeHintType.ERROR_CORRECTION, EClevel);
			hints2.put(EncodeHintType.QR_MASK_PATTERN, mask_pattern);
			hints2.put(EncodeHintType.MARGIN, 0);
			int dimension_mod = 17 + 4 * version;
			QRCodeWriter writer2 = new QRCodeWriter();
			BitMatrix bitmatrix_mod = writer2.encode(contents, BarcodeFormat.QR_CODE, dimension_mod, dimension_mod, hints2);

			BitMatrixParser parser = new BitMatrixParser(bitmatrix_mod);
			BufferedImage symbol = new BufferedImage(dimension_mod, dimension_mod,1);

			//シンボルの座標
			int[][][] Symbol = parser.ModuleToSymbol();


			// int[][] blockcolor = {{255,0,0},{0,255,0},{0,0,255},{255,255,0},{255,0,255},{0,255,255},{255,255,255},
			// 					  {191,0,0},{0,191,0},{0,0,191},{191,191,0},{191,0,191},{0,191,191},{191,191,191},
			// 					  {127,0,0},{0,127,0},{0,0,127},{127,127,0},{127,0,127},{0,127,127},{127,127,127},
			// 					  {63,0,0},{0,63,0},{0,0,63},{63,63,0},{63,0,63},{0,63,63},{63,63,63}};
			// //各rsブロックのシンボルごとに塗分け

			// int colornum = 0;
			// for(int i = 0; i < datablocks[0].getNumDataCodewords()*rsblocknum; i++){
			// 	for(int j = 0; j < Symbol[i].length; j++){
			// 		setRGB(symbol, Symbol[i][j][0], Symbol[i][j][1], blockcolor[colornum]);
			// 	}
			// 	colornum++;
			// 	if(colornum == rsblocknum){
			// 	colornum = 0;
			// 	}

			// }

			// colornum = smallcodenum;
			// for (int i = datablocks[0].getNumDataCodewords()*rsblocknum; i < datablocks[0].getNumDataCodewords()*rsblocknum + largecodenum; i++){
			// 	for(int j = 0; j < Symbol[i].length; j++){
			// 		setRGB(symbol, Symbol[i][j][0], Symbol[i][j][1], blockcolor[colornum]);
			// 	}
			// 	colornum++;
			// 	if(colornum == rsblocknum){
			// 	colornum = datablocks.length - largecodenum;
			// 	}
			// }

			// colornum = 0;
			// for (int i = datablocks[0].getNumDataCodewords()*rsblocknum + largecodenum; i < Symbol.length; i++){
			// 	for(int j = 0; j < Symbol[i].length; j++){
			// 		setRGB(symbol, Symbol[i][j][0], Symbol[i][j][1], blockcolor[colornum]);
			// 	}
			// 	colornum++;
			// 	if(colornum >= rsblocknum){
			// 	colornum = 0;
			// 	}
			// }

			// BufferedImage symbol_resize = new BufferedImage(symbol.getWidth()*modulesize, symbol.getHeight()*modulesize,1);

			// //拡大して保存
			// for(int i = 0; i < symbol.getWidth(); i++){
			// 	for(int j = 0; j < symbol.getHeight(); j++){
			// 		int[] modcolor = getRGB(symbol, i, j);
			// 		for(int s = i*modulesize; s < (i+1)*modulesize; s++){
			// 			for(int t = j*modulesize; t < (j+1)*modulesize; t++){
			// 				setRGB(symbol_resize, s, t, modcolor);
			// 			}
			// 		}				
			// 	}
			// }
			
			// ImageIO.write(symbol_resize, "BMP", new File("symbol.bmp"));


			////URL部分と各種機能パターン，形式情報をマスク
			////Nonsystematiccode.javaに読み込むロゴ入りQRはURLと機能パターン，形式情報だけそのままの必要がある
			BitMatrix mask_bit = new BitMatrix(bitmatrix_mod.getHeight());

			//機能パターンと形式情報をマスク
			for(int i = 0; i < mask_bit.getHeight(); i++){
				for(int j = 0; j < mask_bit.getWidth(); j++){
					mask_bit.set(i, j);
				}
			}
			for(int i = 0; i < Symbol.length; i++){
				for(int j = 0; j < Symbol[i].length; j++){
					mask_bit.unset(Symbol[i][j][0], Symbol[i][j][1]);
				}
			}

			//URL部分をマスク
			int datacodecheck = 0;
			int reset = 0;
			for(int i = reset; i < Symbol.length; i = i + rsblocknum){

				if(datacodecheck == datablocks[reset].getNumDataCodewords()){
					reset++;
					i = reset;
				}

				for(int j = 0; j < Symbol[i].length; j++){
					mask_bit.set(Symbol[i][j][0], Symbol[i][j][1]);
				}

				datacodecheck++;
				if(datacodecheck >= contentdata.length){
					break;
				}
			}

			//拡大して保存
			BitMatrix mask_bit_resize = new BitMatrix((mask_bit.getHeight() + 2*margin) * modulesize);
			
			for(int i = 0; i < mask_bit.getHeight(); i++){
				for(int j = 0; j < mask_bit.getWidth(); j++){
					if(mask_bit.get(i, j)){
						for(int s = (i+margin)*modulesize; s < (i+1+margin)*modulesize; s++){
							for(int t = (j+margin)*modulesize; t < (j+1+margin)*modulesize; t++){
								mask_bit_resize.set(s, t);
							}
						}
					}
				}
			}

			BufferedImage mask = MatrixToImageWriter.toBufferedImage(mask_bit_resize);
			ImageIO.write(mask, "BMP", new File("app/mask.bmp"));

			// ////機能パターンを黒くマスク
			// BitMatrix fun_mask_bit = new BitMatrix(bitmatrix_mod.getHeight());

			// for(int i = 0; i < fun_mask_bit.getHeight(); i++){
			// 	for(int j = 0; j < fun_mask_bit.getWidth(); j++){
			// 		fun_mask_bit.set(i, j);
			// 	}
			// }
			// for(int i = 0; i < Symbol.length; i++){
			// 	for(int j = 0; j < Symbol[i].length; j++){
			// 		fun_mask_bit.unset(Symbol[i][j][0], Symbol[i][j][1]);
			// 	}
			// }

			// //拡大して保存
			// BitMatrix fun_mask_bit_resize = new BitMatrix((fun_mask_bit.getHeight() + 2*margin) * modulesize);
			
			// for(int i = 0; i < fun_mask_bit.getHeight(); i++){
			// 	for(int j = 0; j < fun_mask_bit.getWidth(); j++){
			// 		if(fun_mask_bit.get(i, j)){
			// 			for(int s = (i+margin)*modulesize; s < (i+1+margin)*modulesize; s++){
			// 				for(int t = (j+margin)*modulesize; t < (j+1+margin)*modulesize; t++){
			// 					fun_mask_bit_resize.set(s, t);
			// 				}
			// 			}
			// 		}
			// 	}
			// }

			// BufferedImage funmask = MatrixToImageWriter.toBufferedImage(fun_mask_bit_resize);
			// ImageIO.write(funmask, "BMP", new File("funmask.bmp"));

		} catch (Exception e) {
			e.printStackTrace();
		}


    }

	////biの(x,y)に指定のRGBをセット
	public static void setRGB(BufferedImage bi, int x, int y, int[] rgb) {
        int pixel = 0xff000000 | rgb[0] << 16 | rgb[1] << 8 | rgb[2];
        bi.setRGB(x, y, pixel);
    }

	public static int[] getRGB(BufferedImage bi, int x, int y) {
        int pixel = bi.getRGB(x, y);
        int red = pixel >> 16 & 0xff;
        int green = pixel >> 8 & 0xff;
        int blue = pixel & 0xff;
        return new int[]{red, green, blue};
    }
}
