/*
 * Copyright 2007 ZXing authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.google.zxing.common.reedsolomon;

/**
 * <p>Implements Reed-Solomon decoding, as the name implies.</p>
 *
 * <p>The algorithm will not be explained here, but the following references were helpful
 * in creating this implementation:</p>
 *
 * <ul>
 * <li>Bruce Maggs.
 * <a href="http://www.cs.cmu.edu/afs/cs.cmu.edu/project/pscico-guyb/realworld/www/rs_decode.ps">
 * "Decoding Reed-Solomon Codes"</a> (see discussion of Forney's Formula)</li>
 * <li>J.I. Hall. <a href="www.mth.msu.edu/~jhall/classes/codenotes/GRS.pdf">
 * "Chapter 5. Generalized Reed-Solomon Codes"</a>
 * (see discussion of Euclidean algorithm)</li>
 * </ul>
 *
 * <p>Much credit is due to William Rucklidge since portions of this code are an indirect
 * port of his C++ Reed-Solomon implementation.</p>
 *
 * @author Sean Owen
 * @author William Rucklidge
 * @author sanfordsquires
 */
public final class ReedSolomonDecoder {

  private final GenericGF field;

  public ReedSolomonDecoder(GenericGF field) {
    this.field = field;
  }

  /**
   * <p>Decodes given set of received codewords, which include both data and error-correction
   * codewords. Really, this means it uses Reed-Solomon to detect and correct errors, in-place,
   * in the input.</p>
   *
   * @param received data and error-correction codewords
   * @param twoS number of error-correction codewords available
   * @throws ReedSolomonException if decoding fails for any reason
   */
  public void decode(int[] received, int twoS) throws ReedSolomonException {
    decodeWithECCount(received, twoS);
  }

  /**
   * <p>Decodes given set of received codewords, which include both data and error-correction
   * codewords. Really, this means it uses Reed-Solomon to detect and correct errors, in-place,
   * in the input.</p>
   *
   * @param received data and error-correction codewords
   * @param twoS number of error-correction codewords available
   * @return the number of errors corrected
   * @throws ReedSolomonException if decoding fails for any reason
   */
  public int decodeWithECCount(int[] received, int twoS) throws ReedSolomonException {
    GenericGFPoly poly = new GenericGFPoly(field, received);
    int[] syndromeCoefficients = new int[twoS];
    boolean noError = true;
    for (int i = 0; i < twoS; i++) {
      int eval = poly.evaluateAt(field.exp(i + field.getGeneratorBase()));
      syndromeCoefficients[syndromeCoefficients.length - 1 - i] = eval;
      if (eval != 0) {
        noError = false;
      }
    }
    if (noError) {
      return 0;
    }
    GenericGFPoly syndrome = new GenericGFPoly(field, syndromeCoefficients);
    GenericGFPoly[] sigmaOmega =
        runEuclideanAlgorithm(field.buildMonomial(twoS, 1), syndrome, twoS);
    GenericGFPoly sigma = sigmaOmega[0];
    GenericGFPoly omega = sigmaOmega[1];
    int[] errorLocations = findErrorLocations(sigma);
    int[] errorMagnitudes = findErrorMagnitudes(omega, errorLocations);
    for (int i = 0; i < errorLocations.length; i++) {
      int position = received.length - 1 - field.log(errorLocations[i]);
      if (position < 0) {
        throw new ReedSolomonException("Bad error location");
      }
      received[position] = GenericGF.addOrSubtract(received[position], errorMagnitudes[i]);
    }
    return errorLocations.length;
  }

  // make erasedecode
  public int erasedecodeWithECCount(int[] received,int[] eraseposition, int twoS) throws ReedSolomonException {
    GenericGFPoly poly = new GenericGFPoly(field, received);

    ////シンドロームの計算
    int[] syndromeCoefficients = new int[twoS];
    boolean noError = true;
    for (int i = 0; i < twoS; i++) {
      int eval = poly.evaluateAt(field.exp(i + field.getGeneratorBase()));
      syndromeCoefficients[syndromeCoefficients.length - 1 - i] = eval;
      if (eval != 0) {
        noError = false;
      }
    }
    if (noError) {
      return 0;
    }
    GenericGFPoly syndrome = new GenericGFPoly(field, syndromeCoefficients);

    //// 消失位置多項式λを構成
    int erasenum = eraseposition.length;

    //消失位置多項式の因数を格納
    int[][] erasepoly_factor = new int[erasenum][2];

    //消失位置は反転 exp..受信語の長さが10,消失位置が0ならば0→9
    //シンドロームが反転して計算されるため 
    int eraseposition_reverse;

    //消失位置のべき乗を根に持つ因数を生成し逐次的にかける
    int[] one = {1};
    GenericGFPoly lamda = new GenericGFPoly(field, one);
    for (int i = 0; i < erasenum; i++) {
      eraseposition_reverse = received.length - 1 - eraseposition[i];
      erasepoly_factor[i][0] = field.exp(eraseposition_reverse);
      erasepoly_factor[i][1] = 1;
      GenericGFPoly poly_factor = new GenericGFPoly(field, erasepoly_factor[i]);
      lamda = lamda.multiply(poly_factor);
    }

    ////シンドローム×消失位置多項式(S(x)×λ(x):2t次以上の項は切り捨て)を計算
    GenericGFPoly sramda = new GenericGFPoly(field, one);
    sramda = sramda.multiply(syndrome);
    sramda = sramda.multiply(lamda);
    int[] sramda_array = new int[syndromeCoefficients.length];
    GenericGFPoly sramda_unnder2t;
    // System.out.print("sramda,sramdaarray:" + sramda.getDegree());
    if(sramda.getDegree() < sramda_array.length - 1){
      sramda_unnder2t = sramda;

    }else{
      for (int i = 0; i < sramda_array.length; i++) {
        // System.out.print(sramda.getDegree() + sramda_array.length - 1 - i);
        sramda_array[i] = sramda.getCoefficient(sramda_array.length - 1 - i);
    }

      sramda_unnder2t = new GenericGFPoly(field, sramda_array);
    }

    ////ユークリッドアルゴリズムによって誤り位置多項式σと誤り、消失の大きさに関わるψを求める
    GenericGFPoly[] sigmapsi =
        runEuclideanAlgorithm(field.buildMonomial(twoS, 1), sramda_unnder2t, twoS + erasenum);
    GenericGFPoly sigma = sigmapsi[0];
    GenericGFPoly psi = sigmapsi[1];

    int[] errorLocations = findErrorLocations(sigma);
    int[] eraseLocations = findErrorLocations(lamda);
  
    
    int[] errorMagnitudes = findErrorMagnitudes(psi, errorLocations);
    for (int i = 0; i < errorMagnitudes.length; i++) {
      int lamda_inverse = lamda.evaluateAt(field.inverse(errorLocations[i]));
      errorMagnitudes[i] = field.divide(lamda_inverse, errorMagnitudes[i]);
    }

    int[] eraseMagnitudes = findErrorMagnitudes(psi, eraseLocations);
    for (int i = 0; i < eraseMagnitudes.length; i++) {
      int sigma_inverse = sigma.evaluateAt(field.inverse(eraseLocations[i]));
      eraseMagnitudes[i] = field.divide(sigma_inverse, eraseMagnitudes[i]);
    }
  
    
    for (int i = 0; i < errorLocations.length; i++) {
      int errorpos = received.length - 1 - field.log(errorLocations[i]);
      if (errorpos < 0) {
        throw new ReedSolomonException("Bad error location");
      }
      received[errorpos] = GenericGF.addOrSubtract(received[errorpos], errorMagnitudes[i]);
    }

    for (int i = 0; i < eraseLocations.length; i++) {
      int erasepos = received.length - 1 - field.log(eraseLocations[i]);
      if (erasepos < 0) {
        throw new ReedSolomonException("Bad error location");
      }
      received[erasepos] = GenericGF.addOrSubtract(received[erasepos], eraseMagnitudes[i]);
    }

    GenericGFPoly poly2 = new GenericGFPoly(field, received);

    int[] syndromecheck = new int[twoS];
    boolean noErrorcheck = true;
    for (int i = 0; i < twoS; i++) {
      int eval = poly2.evaluateAt(field.exp(i + field.getGeneratorBase()));
      syndromecheck[syndromecheck.length - 1 - i] = eval;
      if (eval != 0) {
        noErrorcheck = false;
      }
    }
    if (!noErrorcheck) {
      throw new ReedSolomonException("syndrome was not zero");
    }
  
    return errorLocations.length;
    
    
  }


  private GenericGFPoly[] runEuclideanAlgorithm(GenericGFPoly a, GenericGFPoly b, int R)
      throws ReedSolomonException {
    // Assume a's degree is >= b's
    if (a.getDegree() < b.getDegree()) {
      GenericGFPoly temp = a;
      a = b;
      b = temp;
    }

    GenericGFPoly rLast = a;
    GenericGFPoly r = b;
    GenericGFPoly tLast = field.getZero();
    GenericGFPoly t = field.getOne();

    // Run Euclidean algorithm until r's degree is less than R/2
    while (2 * r.getDegree() >= R) {
      GenericGFPoly rLastLast = rLast;
      GenericGFPoly tLastLast = tLast;
      rLast = r;
      tLast = t;

      // Divide rLastLast by rLast, with quotient in q and remainder in r
      if (rLast.isZero()) {
        // Oops, Euclidean algorithm already terminated?
        throw new ReedSolomonException("r_{i-1} was zero");
      }
      r = rLastLast;
      GenericGFPoly q = field.getZero();
      int denominatorLeadingTerm = rLast.getCoefficient(rLast.getDegree());
      int dltInverse = field.inverse(denominatorLeadingTerm);
      while (r.getDegree() >= rLast.getDegree() && !r.isZero()) {
        int degreeDiff = r.getDegree() - rLast.getDegree();
        int scale = field.multiply(r.getCoefficient(r.getDegree()), dltInverse);
        q = q.addOrSubtract(field.buildMonomial(degreeDiff, scale));
        r = r.addOrSubtract(rLast.multiplyByMonomial(degreeDiff, scale));
      }

      t = q.multiply(tLast).addOrSubtract(tLastLast);

      if (r.getDegree() >= rLast.getDegree()) {
        throw new IllegalStateException("Division algorithm failed to reduce polynomial? " +
          "r: " + r + ", rLast: " + rLast);
      }
    }

    int sigmaTildeAtZero = t.getCoefficient(0);
    if (sigmaTildeAtZero == 0) {
      throw new ReedSolomonException("sigmaTilde(0) was zero");
    }

    int inverse = field.inverse(sigmaTildeAtZero);
    GenericGFPoly sigma = t.multiply(inverse);
    GenericGFPoly omega = r.multiply(inverse);
    return new GenericGFPoly[]{sigma, omega};
  }

  private int[] findErrorLocations(GenericGFPoly errorLocator) throws ReedSolomonException {
    // This is a direct application of Chien's search
    int numErrors = errorLocator.getDegree();
    if (numErrors == 1) { // shortcut
      return new int[] { errorLocator.getCoefficient(1) };
    }
    int[] result = new int[numErrors];
    int e = 0;
    for (int i = 1; i < field.getSize() && e < numErrors; i++) {
      if (errorLocator.evaluateAt(i) == 0) {
        result[e] = field.inverse(i);
        e++;
      }
    }
    if (e != numErrors) {
      throw new ReedSolomonException("Error locator degree does not match number of roots");
    }
    return result;
  }

  private int[] findErrorMagnitudes(GenericGFPoly errorEvaluator, int[] errorLocations) {
    // This is directly applying Forney's Formula
    int s = errorLocations.length;
    int[] result = new int[s];
    for (int i = 0; i < s; i++) {
      int xiInverse = field.inverse(errorLocations[i]);
      int denominator = 1;
      for (int j = 0; j < s; j++) {
        if (i != j) {
          //denominator = field.multiply(denominator,
          //    GenericGF.addOrSubtract(1, field.multiply(errorLocations[j], xiInverse)));
          // Above should work but fails on some Apple and Linux JDKs due to a Hotspot bug.
          // Below is a funny-looking workaround from Steven Parkes
          int term = field.multiply(errorLocations[j], xiInverse);
          int termPlus1 = (term & 0x1) == 0 ? term | 1 : term & ~1;
          denominator = field.multiply(denominator, termPlus1);
        }
      }
      result[i] = field.multiply(errorEvaluator.evaluateAt(xiInverse),
          field.inverse(denominator));
      if (field.getGeneratorBase() != 0) {
        result[i] = field.multiply(result[i], xiInverse);
      }
    }
    return result;
  }

}
