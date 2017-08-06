aa=[[1],[2],[5,2,3],[4],[5]]



for a in aa:
    if a[0]==5:
        aa.remove(a)
print(aa)

print(len(aa))