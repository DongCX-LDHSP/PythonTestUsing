import os
from os import path
import logging
import sys


# 当前的工作目录
thisFileFolder = os.getcwd()
# 保存字典文件的文件夹
wordlistsFolder = os.path.join(thisFileFolder, "wordlists")
# 已使用过的字典文件前缀
usedWordlistPrefix = "used_"
# 输出结果文件夹
outputFolder = os.path.join(thisFileFolder, "output")
# 保存 执行输出 的文件名前缀
outputFilenamePrefix = "out"

# hashcat可执行文件保存位置
hashcatFolder = r""
# 待破解的hashfile文件
hashFilePath = r""
# 进行破解的命令行模板
# 第一个占位是字典文件路径
# 第二个占位是执行输出的保存文件
commandTemplate = f'hashcat.exe -m 22000 "{hashFilePath}" "{{}}" > "{{}}"'


# 在当前目录下创建需要的临时文件夹
def init():
    cwd = os.getcwd()
    os.chdir(thisFileFolder)

    print('检查 hashcat.exe 文件所在目录...')
    if hashcatFolder == '':
        print('    请设置变量 hashcatFolder 的值为 hashcat.exe 可执行文件所在的目录')
    print('检查 hash 文件路径...')
    if hashFilePath == '':
        print('    请先设置变量 hashFilePath 的值为要使用的 hash 文件的绝对路径')
    os.mkdir(wordlistsFolder) if path.exists(wordlistsFolder) is False else None
    print('已创建字典文件保存文件夹，请将字典文件移动到当前工作目录下的 wordlists 文件夹')
    os.mkdir(outputFolder) if path.exists(outputFolder) is False else None
    print('已创建保存指令输出的文件夹，你可以在当前工作目录下的 output 查看指令输出的内容，\n'
          '    输出文件命名格式：out-字典文件名')

    os.chdir(cwd)
    print("初始化结束")


# 将所有被标记为已使用的字典修改为原始名称
def reset():
    print('开始恢复字典文件名')
    # 备份当前的工作目录
    cwd = os.getcwd()
    # 切换工作目录到字典文件夹
    os.chdir(wordlistsFolder)
    # 获取字典目录下的
    fileOrDirs = os.listdir()
    # 筛选出字典文件
    wordlists = [fileOrDir for fileOrDir in fileOrDirs if path.isfile(fileOrDir)]
    print(f"检测到 {len(wordlists)} 个字典文件")
    # 筛选出被标记为已使用的字典文件
    usedWordlists = [wordlist for wordlist in wordlists if wordlist.startswith(usedWordlistPrefix)]
    print(f"共 {len(usedWordlists)} 个被标记为已使用")
    # 恢复原始名称失败的字典文件
    resetFailedWordlistsCount = 0
    # 重命名被标记为已使用的字典文件为原始名称
    for usedWordlist in usedWordlists:
        try:
            os.rename(usedWordlist, usedWordlist.replace(usedWordlistPrefix, ""))
        except Exception as e:
            logging.exception(e)
            resetFailedWordlistsCount += 1

    print(f'共 {resetFailedWordlistsCount} 个恢复失败')
    print('恢复字典文件名结束')

    # 恢复工作目录
    os.chdir(cwd)


# 基于所有字典文件进行破解
def crack():
    # 获取所有未被使用的字典文件
    wordlists = sorted(os.listdir(wordlistsFolder))
    # 筛选出未被使用过的字典文件
    unusedWordlists = [wordlist for wordlist in wordlists if wordlist.startswith(usedWordlistPrefix) is False]
    wordlistNum = len(unusedWordlists)
    # 切换工作目录到hashcat.exe所在的目录
    os.chdir(hashcatFolder)
    for i, wordlist in enumerate(unusedWordlists):
        try:
            print(f"进度：{i + 1}/{wordlistNum}")
            # 构造字典文件的绝对路径
            wordlistFilePath = path.join(wordlistsFolder, wordlist)
            # 构造命令输出保存文件的绝对路径
            outputFilePath = path.join(outputFolder, f"{outputFilenamePrefix}-{wordlist}.log")
            # 构造待执行的命令
            executeCommand = commandTemplate.format(wordlistFilePath, outputFilePath)
            print(f"执行命令：{executeCommand}")
            result = os.system(executeCommand)
            print(f"执行完毕，返回值：{result}")

            # 检查是否成功破解
            with open(outputFilePath, "r") as outputFile:
                if "Status...........: Cracked" in outputFile.read():
                    print(f'{"=" * 4} 破解成功 {"=" * 4}')
                else:
                    print(f'{"=" * 4} 破解失败 {"=" * 4}')

            # 移动字典文件
            os.rename(wordlistFilePath, path.join(wordlistsFolder, f'{usedWordlistPrefix}{wordlist}'))
        except Exception as e:
            logging.exception(e)


def usage():
    print(f'usage:\n'
          f'  python3 {__file__} init     # 在当前工作目录创建依赖的文件夹\n'
          f'  python3 {__file__} crack    # 使用字典文件针对指定的hash文件进行破解\n'
          f'  python3 {__file__} reset    # 将被标记为已使用的字典文件恢复原始名称\n'
          f'  python3 {__file__} usage    # 输出这条消息\n'
          f'\n'
          f'caution:\n'
          f'  确保变量 hashcatFolder hashFilePath 保存了相应的路径\n'
          f'  确保变量 commandTemplate 是你想要执行的破解模式\n'
          f'\n'
          f'step:\n'
          f'  1. 使用 init 进行初始化并检测所需变量的值是否设置\n'
          f'  2. 使用 crack 进行破解\n'
          f' *3. 使用 reset 恢复被标记为已使用的字典文件名称')


if __name__ == "__main__":
    if len(sys.argv) == 2:
        func = sys.argv[1]
        if func == "init":
            init()
        elif func == "crack":
            crack()
        elif func == "reset":
            reset()
        else:
            print('未知参数') if func != "usage" else None
            usage()
    else:
        usage()
