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


import os
from flask import send_file
from io import BytesIO
import zipfile
import time

def create_zip_from_directory(directory_path):
    memory_file = BytesIO()

    # ZIPファイルを作成
    with zipfile.ZipFile(memory_file, 'w') as zf:
        # ディレクトリ内のすべてのファイルを取得
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)  # フルパスを生成
                relative_path = os.path.relpath(file_path, directory_path)  # ZIP内の相対パス
                zip_info = zipfile.ZipInfo(relative_path)
                zip_info.date_time = time.localtime(time.time())[:6]
                zip_info.compress_type = zipfile.ZIP_DEFLATED
                # ファイルをZIPに書き込む
                with open(file_path, 'rb') as f:
                    zf.writestr(zip_info, f.read())
    
    # ファイルポインタを先頭に戻す
    memory_file.seek(0)
    return send_file(memory_file, download_name='output.zip', as_attachment=True)


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


@app.route('/download_zip')
def download_zip():
    directory_path = './imagedata_output'
    return create_zip_from_directory(directory_path)



if __name__ == "__main__":
    # javaファイルを実行するためにJpypeを起動
    jpype.startJVM()
    # app中のjavaディレクトリをクラスパスに追加
    jpype.addClassPath("java")
    app.run(host = "0.0.0.0", port = 5000, debug = True)
    # Jpypeを終了
    jpype.shutdownJVM()