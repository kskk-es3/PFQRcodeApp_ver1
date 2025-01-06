from app.app import app
import jpype


if __name__ == "__main__":
    # javaファイルを実行するためにJpypeを起動
    jpype.startJVM()
    # カレントディレクトリをクラスパスに追加
    jpype.addClassPath(".")
    app.run(host = "127.0.0.1", port = 5000, debug = True)
    # Jpypeを終了
    jpype.shutdownJVM()