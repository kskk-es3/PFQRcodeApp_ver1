from flask import Flask, request, redirect, url_for, render_template
import os
import PFQRmain
import jpype
from werkzeug.utils import secure_filename

app = Flask(__name__)

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
            PFQRmain.PFQRmain(input_text)
    
    return render_template('index.html')



if __name__ == "__main__":
    # javaファイルを実行するためにJpypeを起動
    jpype.startJVM()
    # app中のjavaディレクトリをクラスパスに追加
    jpype.addClassPath("java")
    app.run(host = "127.0.0.1", port = 5000, debug = True)
    # Jpypeを終了
    jpype.shutdownJVM()