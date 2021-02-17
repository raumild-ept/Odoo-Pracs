# #decorator.
# def decorate_functions(func):
#     def inner(func):
#         print('this1')
#         func()
#         print('this2')
#     return inner(func)
#
#
# @decorate_functions
# def do_things():
#     print("main functions.")
#
# do_things()
#

def calculate_time(func):
    def inner1(*args, **kwargs):
        print("thsi1")
        func(*args, **kwargs)
        print("thsi2")
    return inner1

@calculate_time
def factorial():
    print("success")

factorial()
