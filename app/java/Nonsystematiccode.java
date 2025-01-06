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
import com.google.zxing.client.j2se.MatrixToImageWriter;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.qrcode.QRCodeReader;
import com.google.zxing.qrcode.QRCodeWriter;
import com.google.zxing.qrcode.decoder.DataBlock;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.common.reedsolomon.GenericGF;
import com.google.zxing.common.reedsolomon.ReedSolomonDecoder;

public class Nonsystematiccode {
    public static void nonsystematiccode(String pathname) throws Exception {


		////ロゴを重ねたQRコードを読み込んで非組織符号化を行い、ロゴを重ねた時に読み取り可能なQRコードを生成する 

	
		Analysis analysis = new Analysis();

		//ロゴをのせたQRコード画像を読み込んで格納されている符号語を抽出
		File file = new File(pathname);
		BufferedImage image = ImageIO.read(file);
		DataBlock[] datablocks = analysis.symbolgen(image);

		int[][] codewordInt = new int[datablocks.length][];
		int datablockcount = 0;
		for (DataBlock datablock : datablocks) {
			byte[] codewordBytes = datablock.getCodewords();
			codewordInt[datablockcount] = new int[codewordBytes.length];
			System.out.println(codewordBytes.length);
			for (int i = 0; i < codewordBytes.length; i++) {
				codewordInt[datablockcount][i] = codewordBytes[i] & 0xFF;
				// System.out.print(codewordInt[datablockcount][i]+" ");
				
			}
			// System.out.println();
			datablockcount++;

		}


		////消失誤り訂正を使って非組織符号化
		////消失点をn-k個選んで消失誤り訂正を行うことで選んだ消失点が検査点となる符号語が生成される
		ReedSolomonDecoder rsDecoder = new ReedSolomonDecoder(GenericGF.QR_CODE_FIELD_256);

		//消失点
		int[] erasepos0 = {33,34,42,43,51,52,60,61,69,70,78,79,87,88,96,97,105,106,133,132,131,130,129,128,127,126};
		int[][] erasepos_array = {erasepos0};

		for(int i = 0; i < erasepos_array.length; i++){
			
			int errorsCorrected = rsDecoder.erasedecodeWithECCount(codewordInt[i], erasepos_array[i], erasepos_array[i].length);
			// int errorsCorrected = rsDecoder.decodeWithECCount(codewordInt[i], 26);
			System.out.println(errorsCorrected);
		}
		

		byte[][] datablocks_byte = new byte[datablocks.length][];
		datablockcount = 0;
		for (int i = 0; i < datablocks_byte.length; i++) {
			datablocks_byte[i] = new byte[codewordInt[i].length];
			for(int j = 0; j < datablocks_byte[i].length; j++){
				datablocks_byte[i][j] = (byte)codewordInt[i][j];
				System.out.print(codewordInt[i][j]+" ");
			}
			System.out.println();
		}

		analysis.genqr2(datablocks_byte, "nonsystematicQR.png");
		  
		
    }
}