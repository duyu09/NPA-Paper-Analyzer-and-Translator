import os
import tempfile

# 当程序准备好（例如，主窗口即将显示或已显示）时，执行以下代码关闭splash screen
def close_splash_screen():
    if "NUITKA_ONEFILE_PARENT" in os.environ:
        splash_filename = os.path.join(
            tempfile.gettempdir(),
            f"onefile_{int(os.environ['NUITKA_ONEFILE_PARENT'])}_splash_feedback.tmp"
        )
        if os.path.exists(splash_filename):
            os.unlink(splash_filename)
