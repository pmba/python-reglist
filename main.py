from reglist import reglist

numerical_list = reglist("[0-9]")
print(numerical_list)
# ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

loweralpha_list = reglist("[a-z]")
print(loweralpha_list)
# ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

upperalpha_list = reglist("[A-Z]")
print(upperalpha_list)
# ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

numerical_list = reglist("[0-9^[123]]")
print(numerical_list)
# ['0', '2', '4', '5', '6', '7', '8', '9']
