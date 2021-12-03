from PyPDF2 import PdfFileWriter, PdfFileReader
import getpass
import sys
import os
import logging


'''
将传入的pdf文件加密，并在文件名前添加"encode_"，
然后将输出文件保存到当前目录下
加密成功返回True，失败则返回False
'''
def encode(originalFilepath: str) -> bool:
    # 检查原始文件是否存在
    if os.path.exists(originalFilepath) is False:
        print("原始文件未找到，加密失败！")
        return False
    # 原始文件
    originalFile = PdfFileReader(originalFilepath)
    # 加密后文件
    encodedFile = PdfFileWriter()

    try:
        # 将原始文件的内容拷贝到新文件中
        for i in range(originalFile.numPages):
            encodedFile.addPage(originalFile.getPage(i))

        # 获取密码
        password: str = getpass.getpass("请输入你想要设置的密码：")

        # 加密输出文件
        encodedFile.encrypt(password)

        # 写入到文件中
        with open(f"encode_{os.path.basename(originalFilepath)}", "wb") as out:
            encodedFile.write(out)

    except Exception as e:
        print("加密时遇到未知问题，加密失败！")
        logging.exception(e)
        return False

    return True


# 输出脚本的使用方法
def usage() -> None:
    print(f'使用方法：\n'
          f'python3 {__file__} pdf_file_path\n'
          f'输出文件名：encode_pdf_filename')


if __name__ == "__main__":
    # 检查参数传入
    if len(sys.argv) < 2:
        print("请传入要加密的文件名！")
        usage()
        result: bool = False
    else:
        result: bool = encode(sys.argv[1])

    print("成功！" if result is True else "失败！")
