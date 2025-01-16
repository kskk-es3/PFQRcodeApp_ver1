import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

import javax.imageio.ImageIO;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.Binarizer;
import com.google.zxing.BinaryBitmap;
import com.google.zxing.EncodeHintType;
import com.google.zxing.FormatException;
import com.google.zxing.LuminanceSource;
import com.google.zxing.NotFoundException;
import com.google.zxing.WriterException;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.client.j2se.MatrixToImageWriter;
import com.google.zxing.common.BitMatrix;
import com.google.zxing.common.DecoderResult;
import com.google.zxing.common.DetectorResult;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.common.reedsolomon.GenericGF;
import com.google.zxing.qrcode.QRCodeReader;
import com.google.zxing.qrcode.QRCodeWriter;
import com.google.zxing.qrcode.decoder.BitMatrixParser;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;
import com.google.zxing.qrcode.decoder.Version;
import com.google.zxing.qrcode.decoder.DataBlock;
import com.google.zxing.qrcode.detector.Detector;

public class Analysis {

	////QRコードの解析に用いる関数をまとめたクラス
	
	GenericGF field = GenericGF.QR_CODE_FIELD_256;

	int version = 5;
	ErrorCorrectionLevel eLevel = ErrorCorrectionLevel.L;
	int mask_pattern1 = 0;
	int margin = 1;
	int modulesize = 20; //適宜変更
	int dimension = modulesize * (17 + 4 * version + 2 * margin);

	//符号語からQRコードを生成
	public void genqr1(byte[][] codewords, String pathname) throws IOException, WriterException{
		Map<EncodeHintType, Object> hints = new EnumMap<>(EncodeHintType.class);
		//誤り訂正レベル
		hints.put(EncodeHintType.ERROR_CORRECTION, eLevel);
		//バージョン
		hints.put(EncodeHintType.QR_VERSION, version);
		hints.put(EncodeHintType.MARGIN, margin);

		QRCodeWriter writer = new QRCodeWriter();
		//apform = 0なら通常の形状それ以外の数値なら変更した形状(MatrixUtil.java)
		int apform = 0;
		BitMatrix bitMatrix = writer.encodecodeword(codewords, BarcodeFormat.QR_CODE, mask_pattern1, dimension, dimension, apform, hints);
		BufferedImage image = MatrixToImageWriter.toBufferedImage(bitMatrix);
		ImageIO.write(image, "png", new File(pathname));

	}

	//符号語からQRコードを生成,アライメントパターンを少し変更変更した形状はMatrixUtil.javaで定義
	public void genqr2(byte[][] codewords, String pathname) throws IOException, WriterException{
		Map<EncodeHintType, Object> hints = new EnumMap<>(EncodeHintType.class);
		//誤り訂正レベル
		hints.put(EncodeHintType.ERROR_CORRECTION, eLevel);
		//バージョン
		hints.put(EncodeHintType.QR_VERSION, version);
		hints.put(EncodeHintType.MARGIN, margin);

		QRCodeWriter writer = new QRCodeWriter();

		//apform = 0なら通常の形状それ以外の数値なら変更した形状(MatrixUtil.java)
		int apform = 1;
		BitMatrix bitMatrix = writer.encodecodeword(codewords, BarcodeFormat.QR_CODE, mask_pattern1, dimension, dimension, apform, hints);
		BufferedImage image = MatrixToImageWriter.toBufferedImage(bitMatrix);
		ImageIO.write(image, "png", new File(pathname));

	}


	//URLから符号語を生成
	public byte[] codeword(String content) throws WriterException{

		Map<EncodeHintType, Object> hints = new EnumMap<>(EncodeHintType.class);
		hints.put(EncodeHintType.ERROR_CORRECTION, eLevel);
		hints.put(EncodeHintType.QR_VERSION, version);
		QRCodeWriter writer = new QRCodeWriter();
		byte[] result = writer.encodebytearray(content, BarcodeFormat.QR_CODE, 256, 256, hints);

		return result;

	}

	//URLからデータコード語を生成
	public byte[] datacodeword(String content) throws WriterException{

		Map<EncodeHintType, Object> hints = new EnumMap<>(EncodeHintType.class);
		hints.put(EncodeHintType.ERROR_CORRECTION, eLevel);
		hints.put(EncodeHintType.QR_VERSION, version);
		QRCodeWriter writer = new QRCodeWriter();
		byte[] result = writer.encodedatacodeword(content, BarcodeFormat.QR_CODE, 256, 256, hints);

		return result;

	}

	//QRコードを読んで、マスクを剥がして、格納されているシンボルの系列を出力(復号ではなく系列を出力するだけ)
	public DataBlock[] symbolgen(BufferedImage qrimage) throws NotFoundException, FormatException{

		//QRコード画像から1モジュール1bitのbitmatrixを生成
		LuminanceSource source = new BufferedImageLuminanceSource(qrimage);
		Binarizer binarizer = new HybridBinarizer(source);
		BinaryBitmap bitmap = new BinaryBitmap(binarizer);
		DetectorResult detectorResult = new Detector(bitmap.getBlackMatrix()).detect();
		BitMatrix bitmatrix = detectorResult.getBits();

		//bitmatrixからシンボル系列を抽出
		BitMatrixParser parser = new BitMatrixParser(bitmatrix);

		//bitmatrixからバージョンと誤り訂正レベルを抽出
		Version version = parser.readVersion();
		ErrorCorrectionLevel ecLevel = parser.readFormatInformation().getErrorCorrectionLevel();
		byte[] codewords = parser.readCodewords();

		// バージョンと誤り訂正レベルからデータブロックを生成
		DataBlock[] result = DataBlock.getDataBlocks(codewords, version, ecLevel);

		return result;
	}


	//符号語を2進数で表示
	public void codewordBinary(byte[] codeword){
		for(int i = 0; i < codeword.length; i++){
			System.out.println(toBinaryString2(codeword[i]));
		}
	}

	//byte型を二進数にした時の1の数をカウントする
	public int count1(byte b){
		int result = Integer.bitCount(Byte.toUnsignedInt(b));
		return result;
	}

	//byte型の配列をint型の配列に変換
	public int[] tointarray(byte[] bytearray){
		int[] result = new int[bytearray.length];
		for(int i = 0; i < result.length; i++){
			result[i] = Byte.toUnsignedInt(bytearray[i]);
		}

		return result;
	}


	//bの n bit目を反転する。n = 0~7
	public byte bitchange(byte b, int n){
		byte result = 0;
		if(n == 0){
			result = (byte)(b ^ 0b00000001);
		}if (n == 1) {
			result = (byte)(b ^ 0b00000010);
		}if (n == 2) {
			result = (byte)(b ^ 0b00000100);	
		}if (n == 3) {
			result = (byte)(b ^ 0b00001000);
		}if (n == 4) {
			result = (byte)(b ^ 0b00010000);
		}if (n == 5) {
			result = (byte)(b ^ 0b00100000);
		}if (n == 6) {
			result = (byte)(b ^ 0b01000000);
		}if (n == 7) {
			result = (byte)(b ^ 0b10000000);
		}

		return result;
	}
	

	//byte型をString型で2進数に変更
	public static String toBinaryString2(byte b) {
		int[] i = new int[8];
		StringBuffer bs = new StringBuffer();
		i[0] = (b & 0b10000000) >>> 7;
		i[1] = (b & 0b01000000) >>> 6;
		i[2] = (b & 0b00100000) >>> 5;
		i[3] = (b & 0b00010000) >>> 4;
		i[4] = (b & 0b00001000) >>> 3;
		i[5] = (b & 0b00000100) >>> 2;
		i[6] = (b & 0b00000010) >>> 1;
		i[7] = (b & 0b00000001) >>> 0;
		for (int j = 0; j < 8; j++) {
			bs.append(i[j]);
		}
		return bs.toString();
	}
    
}
