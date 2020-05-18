### 装饰器函数
>python的装饰器模式在源码中经常遇见，应用非常广泛。
>对装饰器一知半解，影响了学习时候阅读源码的效率，导致很多地方理解不了。
>因此有必要对装饰器进行学习和总结，加深理解。
>
>最好的记录即是用代码样例来表达~

在面向对象（OOP）的设计模式中，decorator被称为装饰模式。
Python能直接从语法层次支持decorator。Python的decorator可以用函数实现，也可以用类实现。


下面是用函数实现的装饰器示例：


```
# 定义装饰器函数
import functools

# 编写一个decorator，只支持@log1。 能在函数调用的前后打印出'begin call'和'end call'的日志。
def log1(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('begin call %s' % func.__name__)
        fun = func(*args, **kwargs)
        print('end call %s' % func.__name__)
        return fun
    return wrapper


# 编写一个decorator，只支持@log2('execute')。 能在函数调用的前后打印出'begin call'和'end call'的日志。
def log2(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(text)
            print('begin call %s' % func.__name__)
            fun = func(*args, **kwargs)
            print('end call %s' % func.__name__)
            return fun
        return wrapper
    return decorator


# 编写一个decorator，既支持@log3，又支持@log3('execute'), 还支持@log3()。 能在函数调用的前后打印出'begin call'和'end call'的日志。
def log3(*text):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if len(text) > 0 and type(text[0]) == str:
                    print(text[0])
                print('begin call %s' % func.__name__)
                fun = func(*args, **kwargs)
                print('end call %s' % func.__name__)
                return fun
            return wrapper
        if len(text) > 0:
            if type(text[0]) == str:
                return decorator
            else:
                return decorator(text[0])
        else:
            return decorator


if __name__ == '__main__':
    #### 测试:
    @log1
    def test_func1(x, y):
        print(x + y)

    @log2('开始运行:')
    def test_func2(x, y):
        print(x ** y)

    @log3
    def test_func3(x, y):
        print(x * y)

    @log3('execute:')
    def test_func4(x, y):
        print(x - y)

    @log3()
    def test_func5(x, y):
        print(x / y)

    test_func1(3, 4)
    test_func2(4, 2)
    test_func3(2, 9)
    test_func4(8, 5)
    test_func5(9, 2)

```