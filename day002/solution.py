list_a = [1, 2, 3, "abc"]
list_b = list_a
print(f"ID for list a before the operation : {id(list_a)}")
print(f"ID for list b before the operation : {id(list_b)}")
list_b.append(911)
print(list_a)
print(f"ID for list a after the operation : {id(list_a)}")
print(f"ID for list b after the operation : {id(list_b)}")

str_a = "john_doe"
str_b = str_a
print(str_a == str_b)
print(f"ID for str a before the operation : {id(str_a)}")
print(f"ID for str b before the operation : {id(str_b)}")
str_b = str_b + "what's up?"
print(str_a)
print(id(str_a))
print(f"ID for str a after the operation : {id(str_a)}")
print(f"ID for str b after the operation : {id(str_b)}")

import copy

list_1 = [[1, 2, 3], [2, 3, 4], [4, 5, 6]]
list_2 = copy.deepcopy(list_1)
list_2[1].append("abc")
print(list_1)
print(list_2)
print(id(list_1) == id(list_2))
print(id(list_1[1]) == id(list_2[1]))

def add_to_list(my_list):
    my_list.append("new_item")

numbers = [1, 2, 3]
add_to_list(numbers)
print(numbers)

def add_to_inventory(inventory=[]):
    inventory.append("item")
    return inventory

print(add_to_inventory())
print(add_to_inventory())
print(add_to_inventory())

def add_to_inventory_fixed(inventory=None):
    if inventory is None:
        inventory = []
    inventory.append("item")
    return inventory

print(add_to_inventory_fixed())
print(add_to_inventory_fixed())
print(add_to_inventory_fixed())

print(0.1 + 0.2)

from decimal import Decimal

amount_1 = Decimal("0.1")
amount_2 = Decimal("0.2")
total = amount_1 + amount_2
print(total)
