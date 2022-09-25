import time
import logging
import platform
from typing import Callable, List
from enum import Enum

import pyperclip
from nltk.corpus import wordnet

from single_instance import SingleInstance


class PlatformType(Enum):
    windows = 'Windows'
    linux = 'Linux'
    mac = 'Mac'
    unknown = 'Unknown'


class Platform:
    @staticmethod
    def name() -> PlatformType:
        try:
            return PlatformType(platform.system())
        except Exception as e:
            logging.exception(e)
            return PlatformType.unknown


class ConstValue:
    __line_break_map: dict = {
        PlatformType.windows: '\r\n',
        PlatformType.linux: '\n',
        PlatformType.mac: '\r',
        PlatformType.unknown: '\r\n',
    }
    line_break: str = __line_break_map[Platform.name()]


ProcessMethodType = Callable[[str], str]


class ProcessFunc(SingleInstance):
    """注册并管理处理函数"""

    # 处理函数列表
    __process_functions: List[ProcessMethodType] = []

    @staticmethod
    def register(func: ProcessMethodType) -> Callable:
        """将一个函数添加到处理函数列表中，并对该函数作一层包装，强制进行参数类型检查"""

        # 将该函数添加到 处理函数 列表中
        ProcessFunc.__process_functions.append(func)

        # 对处理函数进行装饰
        def wrapper(string):
            """对函数进行装饰，在调用函数前检查函数的输入参数是否是字符串类型，不是则打印异常日志"""
            if isinstance(string, str) is False:
                logging.error('不支持的参数类型')
                return ''
            else:
                return func(string)

        return wrapper

    @staticmethod
    def functions() -> List[ProcessMethodType]:
        return ProcessFunc.__process_functions.copy()


def make_choice(menu: List[str], choice_range: List[int]) -> int:
    """让用户做出选择，并作合法性检查"""
    print("\n\nMAKE YOUR CHOICE")
    for item in menu:
        print(item)
    while True:
        choice = input('请输入编号以选择功能：')
        if choice.isdigit():
            if int(choice) in choice_range:
                print("")
                return int(choice)
        print('！非法选择，请重新选择！')


def select_process_method() -> ProcessMethodType:
    """
    基于传入的处理函数列表，让用户切换不同的处理功能
    TODO 考虑是否支持用户一次选择多种处理函数
    """
    functions: List[ProcessMethodType] = ProcessFunc.functions()
    count: int = len(functions)
    methods_info: dict = {i: (method.__name__, method.__doc__, method) for i, method in enumerate(functions)}
    methods_info[count] = ('结束程序', '结束程序', None)

    # 让用户选择功能
    while True:
        menu: List[str] = [f'{key}: {value[0]}, 功能：{value[1]}' for key, value in methods_info.items()]
        return methods_info[make_choice(menu, list(methods_info.keys()))][2]


def listen_clipboard() -> None:
    # 首先让用户选择功能
    process: ProcessMethodType = select_process_method()
    if process is None:
        return

    wait_count = 0
    dealt_count = 0
    error_count = 0
    # 最近一次的剪贴板内容
    recent: str = ''

    # 轮询时用于告知用户程序正常运行的字符序列
    waiting_characters: list = ['\\', '|', '/', '-']

    # 监视剪贴板的主循环
    while True:
        try:
            print(f'\r{process.__name__}: 轮询中{waiting_characters[wait_count % len(waiting_characters)]}', end='')
            wait_count += 1

            current: str = pyperclip.paste()
            # 剪贴板没有新增内容，或内容与上次的内容完全一致，则不处理
            if current == recent:
                time.sleep(0.5)
                continue

            # 处理当前值
            processed = process(current)
            # 更新最近值
            recent = processed
            dealt_count += 1
            if processed == '' or processed == current:
                print(f'\n\n第 {dealt_count} 次命中：不需处理')
                continue

            # 处理之后的结果发生了变化，将处理结果拷贝到剪贴板
            pyperclip.copy(processed)
            print(f'\n\n第 {dealt_count} 次命中: \n{processed}\n')
        except KeyboardInterrupt:
            process = select_process_method()
            if process is None:
                print(f'\n统计结果：\n'
                      f'轮询次数：{wait_count}\n'
                      f'处理次数：{dealt_count}\n'
                      f'出错次数：{error_count}\n')
                break
        except Exception as e:
            error_count += 1
            logging.exception(e)
            print('处理失败')


@ProcessFunc.register
def remove_space(string: str) -> str:
    """无脑删除文本中的所有：空格、制表符、换行符、回车符"""
    spaces: str = ' \t\n\r'
    for ch in spaces:
        string = string.replace(ch, '')
    return string


@ProcessFunc.register
def remove_line_break(string: str) -> str:
    """无脑删除文本中的所有换行，会基于平台的不同，自动选择换行符"""
    return string.replace(ConstValue.line_break, '')


@ProcessFunc.register
def remove_space_and_line_break(string: str) -> str:
    """无脑删除文本中的所有换行以及空白字符，是 remove_line_break 和 remove_space 的合并调用"""
    return remove_space(remove_line_break(string))


@ProcessFunc.register
def strip(string: str) -> str:
    """对该字符串调用 strip 函数，去除首尾的空白符"""
    return string.strip()


@ProcessFunc.register
def remove_blank_line(string: str) -> str:
    """删除文本中的所有空行"""
    result: List[str] = []
    for line in string.split(ConstValue.line_break):
        if line == '':
            continue
        result.append(line)
    return ConstValue.line_break.join(result)


@ProcessFunc.register
def remove_line_break_english(string: str) -> str:
    """基于行尾和行首的字符能否构成单词来移除换行符"""
    # 使用换行符将输入字符串拆分为多行字符串
    original_lines: List[str] = [line.strip() for line in string.split(ConstValue.line_break)]

    # TODO: 逻辑错误，需要进行修改
    # 移除行尾的连字符 '-'，并将该行与下一行进行拼接
    temp_lines: List[str] = []
    length = len(original_lines)
    i = 0
    while i < length:
        temp_lines.append(original_lines[i])
        # 若该行以连字符结尾，则循环考察之后的行是否也以 '-' 结尾，若具有则将其拼接到最后一行中
        if original_lines[i].endswith('-') is True:
            # 循环考察之后的字符串是否也具有 '-'，若具有则将其直接拼接到最新的一行中
            i += 1
            last_index = len(temp_lines) - 1
            while original_lines[i].endswith('-') is True:
                temp_lines[last_index] += original_lines[i]
                i += 1
            # 统一移除最新一行中的 '-'
            temp_lines[last_index] = temp_lines[last_index].replace('-', '')
            continue
        i += 1

    return ' '.join(temp_lines)


if __name__ == '__main__':
    listen_clipboard()
