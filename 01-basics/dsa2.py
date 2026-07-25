color=("red","red","black","white")
print(color)
print(color[1])
print(len(color))
print(color.count("red"))
#print(color.index(1))
print(tuple([1,2]))

name="rahul"
count =0

for char in name:
    count = count + 1
print("Length:", count)  # Output: Length: 5

my_list = [1, 2, 3, "rahul", 5.5]
print(len(my_list))  # Output: 5