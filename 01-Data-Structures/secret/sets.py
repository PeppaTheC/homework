set1 = set('Hello python')
set2 = set("wols os yhW")

print(set.union(set1, set2))
print(set.intersection(set1, set2))
print(set1.difference(set2))
print(set1.symmetric_difference(set2))
set1.update({1, 2, 3, 4})
print(set1)
set1.intersection_update({0, 1, 23})
print(set1)
set1.difference_update({1})
print(set1)
set2.symmetric_difference(['s', 'slow'])
print(set2)
set2.add(10)
print(set2)
set2.remove('s')
print(set2)
set2.discard(1)
print(set2)
set2.pop()
print(set2)
set2.clear()
print(set2)