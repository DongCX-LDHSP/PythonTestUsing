# Python相关的测试代码

一些Python的小代码段

## `TimeLengthGetter`

1. 该模块用于获取数据库的MOOC总时长
2. 源数据是 `./resource/TimeLengthSourceData.txt`
3. 实现原理是基于课程章节名中包含了视频时长，所以得以进行

## `DatetimeNowMethodAndDefaultParameterTest`

1. 该模块用于测试 `Python` 函数的默认参数的表现
2. 发现了一个大坑，`Python` 函数的默认参数的值不会随着时间改变，除非再次运行

## `NeatDMErrorCacheDelete`

1. 今天发现使用`Neat Download Manager`下载东西如果不正常结束会产生大量无用缓存
2. 遂编写了一个脚本用于清理这些无用缓存

```bash
nuitka编译代码
nuitka --follow-imports --standalone --recurse-all --show-progress --show-scons --output-dir=./release --windows-icon=./NeatDMErrorCacheDeleteIcon.ico NeatDMErrorCacheDelete.py
```

## `LeetCode`

1. 该文件是一个小工具，被用于创建并格式化命名基于`C++`的`LeetCode`[答题模板](https://github.com/DongCX-LDHSP/LeetcodeAnswerTemplateForCPP)文件夹，同时将答题模板下的文件夹及文件拷贝到该目录下

2. 同时询问用户是否需要在`Code`中打开该目录，需要用户配置好`Code`的环境变量

3. 依赖：

    1. 保存在本地的[答题模板](https://github.com/DongCX-LDHSP/LeetcodeAnswerTemplateForCPP)，并在代码中设置答题模板路径

        ```python
        # 将这个变量修改为你的答题模板的绝对路径
        templatePath: str = r'D:\Projects\LeetCode\"0. C++Template"'
        ```

    2. 名称格式化工具

        - 使用我编写的`NameConverter`，将在`release`中上传，使用前需要配置好环境变量
        - 修改`getFolderName`方法，适配自己的需求

4. 使用范例，针对这道题：[所有子字符串美丽值之和](https://leetcode-cn.com/problems/sum-of-beauty-of-all-substrings/)

    在此之前，请先修改目标文件夹的前驱路径，如下代码块所示：

    ```python
    # 构造绝对路径
    absolutePathForProgram: str = os.path.join(r"D:\Projects\LeetCode", folderName)
    ```

    使用范例：

    ```cmd
    python LeetCode.py https://leetcode-cn.com/problems/sum-of-beauty-of-all-substrings/ 1781
    ```

    一种可能的输出：

    ```
    创建文件夹成功
    D:\Projects\LeetCode\0. C++Template\LICENSE
    D:\Projects\LeetCode\0. C++Template\Main.cpp
    D:\Projects\LeetCode\0. C++Template\Solution.hpp
    D:\Projects\LeetCode\0. C++Template\.vscode\launch.json
    D:\Projects\LeetCode\0. C++Template\.vscode\settings.json
    D:\Projects\LeetCode\0. C++Template\.vscode\tasks.json
    D:\Projects\LeetCode\0. C++Template\Debug\.keep
    D:\Projects\LeetCode\0. C++Template\Tools\ListNode.hpp
    D:\Projects\LeetCode\0. C++Template\Tools\Print.hpp
    D:\Projects\LeetCode\0. C++Template\Tools\TreeNode.hpp
    复制了 10 个文件
    拷贝模板文件成功
    要在Code中打开这个文件夹吗？(n/N不打开，输入任意字符打开): n
    完成
    ```