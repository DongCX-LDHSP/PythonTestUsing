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
