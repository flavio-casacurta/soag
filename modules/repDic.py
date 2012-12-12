# coding:utf-8
"""
   >>> l1 = 'a b x y e f'.split()
   >>> d1 = {'x':'c', 'y':'d'}
   >>> rd = repDic(d1)
   >>> for n, l in enumerate(l1):
   ...     rd.change(l1, n, l)
   ...
   >>> l1
   ['a', 'b', 'c', 'd', 'e', 'f']

   >>> l2 = 'a b bx x y e f'.split()
   >>> for n, l in enumerate(l2):
   ...     rd.change(l2, n, l)
   ...
   >>> l2
   ['a', 'b', 'bc', 'c', 'd', 'e', 'f']

   >>> l3 = 'a b xy x y e f'.split()
   >>> for n, l in enumerate(l3):
   ...     rd.change(l3, n, l)
   ...
   >>> l3
   ['a', 'b', 'cd', 'c', 'd', 'e', 'f']
"""

class repDic(object):

   def __init__(self, dic = {}):
       self.dic = dic

   def change(self, obj, oco, ite):
       for k, v in self.dic.items():
           obj[oco] = ite.replace(k, v)
           ite = obj[oco]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

