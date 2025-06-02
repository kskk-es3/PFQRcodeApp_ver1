from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import PFQRmain
import jpype
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='imagedata_output')

# アップロードされたファイルを保存するディレクトリ
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 許可するファイルの拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'bmp'}

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # ファイルがリクエストに含まれているかを確認
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']

        # ファイルが選択されているかを確認
        if file.filename == '':
            return redirect(request.url)

        # 許可されたファイル形式かを確認
        if file and allowed_file(file.filename):
            new_filename = f"picture.png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            input_text = request.form.get('text_input')
            input_picturesize = request.form.get('number')

            #PFQRを生成
            PFQRmain.PFQRmain(input_text,input_picturesize)

            # 処理完了後、結果ページへリダイレクト
            return redirect(url_for('result'))

    return render_template('index.html')


@app.route('/result')
def result():
    #結果画面に遷移
    return render_template('result.html')

@app.route('/download/PFQRcode')
def download_PFQRcode():
    # PFQRcodeをダウンロード
    return send_from_directory('./imagedata_output', 'PFQRcode.jpg', as_attachment=True)

@app.route('/download/PFQRcode_nomalFP')
def download_PFQRcode_nomalFP():
    # PFQRcode_nomalFPをダウンロード
    return send_from_directory('./imagedata_output', 'PFQRcode_nomalFP.jpg', as_attachment=True)

@app.route('/download/pictureQRcode')
def download_pictureQRcode():
    # pictureQRcodeをダウンロード
    return send_from_directory('./imagedata_output', 'pictureQRcode.jpg', as_attachment=True)


if __name__ == "__main__":

    # javaファイルを実行するためにJpypeを起動
    jpype.startJVM()
    # app中のjavaディレクトリをクラスパスに追加
    jpype.addClassPath("java")
    app.run(host = "0.0.0.0", port = 81, debug = False)
    # Jpypeを終了
    jpype.shutdownJVM()