print(len("nani"))
str1="raji"
print(len(str1))
print("hi".upper())
str="hi".upper()
print(str)
name="NaNi"
name1=name.lower()
print(name1)
var=" raji nani "
var1=var.strip()
print(var1)
temp="rajinani"
temp1=temp.replace("r","R")
print(temp1)
print("hi".replace("i","o"))
temp2="syashu"
temp3=temp2.find("s")
print(temp3)
name2="ra,ji"
name3=name2.split(",")
print(name3)
print("raji,nani,syashu".split(","))
print("raji"[::-1])
name4="nani"
name5=name4[::-1]
print(name5)
for i in range(5): # 0 to 4
    print(i)

for i in range(1, 6): # 1 to 5
    print(i)
test=input("enter string:")
temp=test
test1=temp[::-1]
if test1 == temp:
           print("the given string pallindrome string")
else:
       print("the given string is not a pallindrome string")

       
