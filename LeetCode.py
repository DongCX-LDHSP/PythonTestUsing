import os
import sys


def getFolderName(name: str, num: str) -> str:
    # 构造文件夹名称
    converterFile = os.popen(f"nameconverter {name.split('/')[-2]}", "r")
    # 读取命令执行结果并移除执行结果首尾的换行符
    stringName: str = converterFile.read().rstrip('\n')
    converterFile.close()
    return f"{num}. {stringName}"

def openInCode(folderPath: str):
    # 是否在code中打开文件夹
    choose: str = input("要在Code中打开这个文件夹吗？(n/N不打开，输入任意字符打开): ")
    if choose.upper() != "N":
        maxTryTimes: int = 100
        while maxTryTimes > 0:
            if os.system(f"code {folderPath}") == 0:
                print("打开目录成功")
                break
            maxTryTimes -= 1
        else:
            print("打开目录失败")


if __name__ == "__main__":
    # 获取命令行参数
    args = sys.argv

    # 获取文件夹名称
    folderName: str = getFolderName(args[1], args[2])
    # 构造绝对路径
    absolutePathForProgram: str = os.path.join(r"D:\Projects\LeetCode", folderName)
    absolutePathForCommandline: str = f'"{absolutePathForProgram}"'

    # 创建目标文件夹
    maxTryTimes: int = 100
    # 若存在则不进行后续操作，直接询问是否在code中打开
    if os.path.exists(absolutePathForProgram) is True:
        print("文件夹已存在")
        openInCode(absolutePathForCommandline)
        print("完成")
        sys.exit(0)
    # 文件夹不存在则进行创建
    else:
        while maxTryTimes > 0:
            if os.system(f"mkdir {absolutePathForCommandline}") == 0:
                print("创建文件夹成功")
                break
            maxTryTimes -= 1
        else:
            print("创建文件夹失败")

    # 若创建文件夹成功则继续
    if maxTryTimes > 0:
        # 复位操作次数限制
        maxTryTimes: int = 100
        # 模板文件夹路径
        templatePath: str = r'D:\Projects\LeetCode\"0. C++Template"'
        # 拷贝模板目录中的所有文件
        while maxTryTimes > 0:
            if os.system(f"xcopy /e {templatePath} {absolutePathForCommandline}") == 0:
                print("拷贝模板文件成功")
                break
            maxTryTimes -= 1
        else:
            print("拷贝模板文件失败")

    # 若拷贝模板文件成功则继续
    if maxTryTimes > 0:
        # 删除license文件及Debug目录下的.keep文件，git仓库是隐藏文件夹没有被复制
        os.system("del /Q {}".format(os.path.join(absolutePathForCommandline, "LICENSE")))
        os.system("del /Q {}".format(os.path.join(absolutePathForCommandline, r"Debug\.keep")))

        # 询问是否需要在code中打开文件夹
        openInCode(absolutePathForCommandline)

    print("完成")
