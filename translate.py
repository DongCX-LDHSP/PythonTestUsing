#!/usr/bin/python3
from google_trans_new import google_translator
import logging
import sys
import os


def translate(sourceFilename, fromLanguage, toLanguage) -> bool:
    resultFilename = os.path.join(os.path.dirname(sourceFilename), f"翻译结果-{os.path.basename(sourceFilename)}")
    try:
        # 读取源文本
        with open(sourceFilename, "r", encoding="utf8") as sourceFile:
            # 读取所有行并去除换行符
            sourceLines = [sourceLine.strip() for sourceLine in sourceFile.readlines()]

        translator = google_translator(timeout=1000)
        # 翻译文本并将结果写入到文件中
        with open(resultFilename, "w", encoding="utf8") as resultFile:
            totalLines = len(sourceLines)
            for i in range(totalLines):
                # 获取翻译结果
                result = translator.translate(sourceLines[i], toLanguage, fromLanguage)
                print(result)
                resultFile.write(f"{result}\n")
                if i % 100 == 0:
                    print(f"{i}/{totalLines}")
    
    except Exception as e:
        logging.exception(e)
        return False

    return True


def usage() -> None:
    print(f"usage:\n"
          f"{__file__} filePath ez|ze\n"
          f"翻译方向：\n"
          "    - ez: 英译中\n"
          "    - ze: 中译英")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        result = False
    else:
        if sys.argv[2] == "ez":
            result = translate(sys.argv[1], "en", "zh")
        elif sys.argv[2] == "ze":
            result = translate(sys.argv[1], "zh", "en")
        else:
            print("未知的第一个参数")
            result = False

    print("成功!" if result is True else "失败!")
