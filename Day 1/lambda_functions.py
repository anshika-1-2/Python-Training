#lambda function, map, filter, reduce


n = [1, 2, 3, 4, 5, 6]
even = filter(lambda x: x % 2 == 0, n)
print(list(even))


numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)


from functools import reduce
def add(x, y):
    return x + y

a = [1, 2, 3, 4, 5]
res = reduce(add, a)
print(res)