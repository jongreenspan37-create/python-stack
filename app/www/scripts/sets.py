# Practice: Python sets (union, intersection, difference). Run directly; not an API endpoint.
set1={1,2,3}
set2={3,4,5}
set3=set1.union(set2)
set4=set1.intersection(set2)
print(set3)
print(set4)
set5=set1.difference(set2)
print(set5)
set1.add(6)
print(set1)
set1.remove(2)
print(set1) 
set1.discard(10)
print(set1)
set2.discard(12)
print(set2)