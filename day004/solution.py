# 1. Write two versions of a function that adds two numbers: one that prints the result, one that returns it.
# Now try to use each one's answer — multiply it by 10 and store it in a name. One of them makes this impossible.
# Explain why in your notes.

def add_num(num1, num2):
    result = num1 + num2
    print(result)


def add_num_return(num1, num2):
    result = num1 + num2
    return result

res_1 = add_num(10, 5)
res_2 = add_num_return(10, 5)

# final_result_1 = res_1*10

final_result_2 = res_2*10

# print(final_result_1)
print(final_result_2)


# 2. Write a function with a return in the middle and some print lines after it. Call it. Observe what never runs.

def something(random_num):
    res = random_num + 1
    return res
    print("Hello")

print(something(10))

# 3. Create a name inside a function. Try to print it from outside.
# Read the error message carefully — it's telling you something true about scope. Write down what.


def name_print(name):
    xyz = "Asish"
    return name

name_print("Yo")
# print(xyz)


# 4. Write a function that takes a list of numbers and returns a new list containing only the even ones.
# Original must be unchanged — check it afterward.
# This is a "returns new data" function, the opposite of the mutating ones you wrote on Day 2.

def check_even(nums):
    even_list = []
    for i in nums:
        if i%2==0:
            even_list.append(i)
    print(nums)
    print(even_list)


check_even([1,2,3,4,5,6])


# 5. Write a function that takes someone's name and greeting, but where the greeting has a default value so you can call it with just a name.
# Then call it three ways: name only, both arguments, and both but passing them by name rather than position.
# (Look up "keyword arguments" for the third.)

def greeting(name, greet="Hello"):
    print(f"{greet}, {name}!")

greeting("X")

greeting("X", "Y")

greeting(greet="X", name="Y")


#6. Take your find_largest from Day 3. Write a second function that uses it —
# say, one that takes two lists and tells you which has the bigger maximum.
# Call your own function from inside another function. That's composition, and it's why return values matter.
def find_largest(numbers):
    if not numbers:
        return None

    largest_so_far = numbers[0]

    for current_number in numbers:
        if current_number > largest_so_far:
            largest_so_far = current_number

    return largest_so_far


my_list = [12, 45, 2, 89, 34, -5, 78]
result = find_largest(my_list)
print("The largest number is:", result)

def bigger_max(list_1, list_2):
    if not list_1 or not list_2:
        if not list_1 and not list_2:
            print("Both lists are empty.")
        elif not list_1:
            print(f'The greatest number among both the lists is {find_largest(list_2)}')
        else:
            print(f'The greatest number among both the lists is {find_largest(list_1)}')

        return
    list_1_large = find_largest(list_1)
    list_2_large = find_largest(list_2)
    if list_1_large>list_2_large:
        print(f'The greatest number among both the lists is {list_1_large}')
    elif list_2_large>list_1_large:
        print(f'The greatest number among both the lists is {list_2_large}')
    else:
        print(f'Both {list_1_large} and {list_2_large} are equal')


bigger_max([], [1,2,3])