import os
import re
from datetime import datetime


errorFilename = re.compile(r"seg.x\d+")
cachePath = r'C:\Users\Username\AppData\Roaming\NeatDM'.replace("Username", os.getlogin(), 1)
logPath = os.path.join(cachePath, "DeleteLog.txt")
deleteCounter = 0
deleteFileSize = 0
file = open(logPath, "w", encoding="utf-8")
file.write("DCX自编写清理Neat Download Manager异常缓存清理脚本\n")
file.write("清理时间：{}\n".format(str(datetime.now())))
file.write("\n被清理的文件路径：\n")
for home, dirs, files in os.walk(cachePath):
    for filename in files:
        if errorFilename.match(filename) is not None or filename == "segments.bin":
            # 删除文件
            deleteCounter += 1
            # print(filename)
            deleteFileSize += os.stat(os.path.join(home, filename)).st_size
            os.remove(os.path.join(home, filename))
            file.write("{}. ".format(deleteCounter) + os.path.join(home, filename) + "\n")
result = f"清理结果：\n" \
         f"删除了{deleteCounter}个异常缓存文件。\n" \
         f"释放了{int(deleteFileSize / (1024 * 1024) * 1000) / 1000}MB的空间。"
file.write("\n" + result)
file.close()
print(result)
print("日志文件路径：{}".format(logPath))
input("按回车退出程序……")
