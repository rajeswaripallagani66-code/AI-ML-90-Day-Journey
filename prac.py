def tuple_to_dice(s):
d={}
for i in range(0,len(s),2):
d [s[i]]=s[i+1]
return s

tup=(1,2,3,4)
print(tuple_to_dice(tup))

