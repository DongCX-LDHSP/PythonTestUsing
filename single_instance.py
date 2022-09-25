class SingleInstance(object):
    """
    通过覆写 __new__ 方法实现单例模式，
    但是值得注意的是，python对象的构建过程是：
        先调用 __new__ 方法，然后是 __init__ 方法，
        所以某些只需要初始化一次的东西需要特别关注一下，避免重复初始化

    使用方法：继承这个类，就可以使得目标类成为单例
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            original = super(SingleInstance, cls)
            cls._instance = original.__new__(cls, *args, **kwargs)
        return cls._instance
