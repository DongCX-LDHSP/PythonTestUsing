import sys
import pyperclip
import logging
import time


def remove_function() -> None:
    wait_count = 0
    dealt_count = 0
    error_count = 0
    recent_value = ''
    while True:
        try:
            current_value = pyperclip.paste()
            # 剪贴板内容没有变化
            if current_value == recent_value:
                if wait_count % 10 == 0:
                    print(f'第 {wait_count} 次轮询...')
                wait_count += 1
                time.sleep(0.5)
                continue

            # 剪贴板内容发生变化
            result = current_value.replace('\r\n', '')
            # 检查是否是英文文本，若不是则移除其中的所有空格
            if not (len(result) > 0 and ('A' <= result[0] <= 'Z' or 'a' <= result[0] <= 'z')):
                result = result.replace(' ', '')
            recent_value = result
            dealt_count += 1
            if result == '' or result == current_value:
                print(f'第 {dealt_count} 次命中：不需处理')
                continue
            pyperclip.copy(result)
            print(f'\n第 {dealt_count} 次命中: \n{result}\n')
        except KeyboardInterrupt:
            print(f'\n统计结果：\n'
                  f'轮询次数：{wait_count}\n'
                  f'处理次数：{dealt_count}\n'
                  f'出错次数：{error_count}\n')
            print('退出中...')
            break
        except Exception as e:
            error_count += 1
            logging.exception(e)
            print('处理失败')


if __name__ == '__main__':
    remove_function()
    