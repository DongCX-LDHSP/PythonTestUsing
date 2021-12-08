import sys
import logging


def remove_blank_line_of_file(filePath: str) -> bool:
    try:
        with open(filePath, "r", encoding="utf8") as sourceFile:
            # 读取所有内容
            lines = sourceFile.readlines()
            # 移除所有的空行
            lines = [line for line in lines if line != "\n"]

        # 将删除空行的结果写入到文件中
        with open(filePath + "without_blank_line", "w", encoding="utf8") as output:
            output.writelines(lines)
    except Exception as e:
        logging.exception(e)
        return False

    return True


if __name__ == "__main__":
    remove_blank_line_of_file(sys.argv[1])
