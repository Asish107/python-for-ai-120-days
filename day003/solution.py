# 1. Write a loop over a list of numbers that prints each one. Then add a line that prints something after the loop, and a line that prints something inside it.
# Change the indentation of the last line so it moves in and out of the loop. Watch the output change. Explain what the indentation is telling the computer.
#

def for_loop(numbers):
    for i in range(numbers):
        print(i)
    print("this is outside the loop")

for_loop(10)


# 2. Loop over a list of numbers and print whether each is even or odd.
# Then extend it to three categories: negative, zero, positive. Make sure exactly one label prints per number; if any number gets two labels, your branching is wrong.

def even_or_odd(num):
    if num%2==0:
        print(f"The number {num} is even")
    else:
        print(f"The number {num} is odd")

even_or_odd(4)


# Loop it over a list. Give it something like [4, 17, 0, -3, 22] and let the loop call it for each number. You've written the loop and the decision separately — combine them.

def even_or_odd(num):
    for i in num:
        if i%2==0:
            print(f"The number {i} is even")
        else:
            print(f"The number {i} is odd")

even_or_odd([4, 17, 0, -3, 22])


# Three categories: negative, zero, positive. This one needs elif. Test all three cases, especially zero — that's the one people get wrong, because it's the boundary and it's easy to write conditions that either catch it twice or miss it entirely.


def num_range_check(num):
    for i in num:
        if i==0:
            print(f"The number {i} is zero")
        elif i>0:
            print(f"The number {i} is positive")
        else:
            print(f"The number {i} is negative")

num_range_check([4, 17, 0, -3, 22])


#
# 3. Write a while loop that counts from 1 to 5.
# Then deliberately break it so it never stops, run it, and stop it yourself with Ctrl+C.
# Then fix it. Write down in your notes what you forgot that caused it to run forever; this is the single most common while bug and you should meet it on purpose.

def loops_while():
    counter = 1
    while counter <= 5:
        print(counter)
        counter += 1


loops_while()

# 4. Loop through a list of names and stop the loop entirely as soon as you find a specific one.
# Then write a second version that skips one particular name but keeps going. Two different tools; know which is which.

def target_finder(result):
    for i in result:
        if i=="Mango":
            break
        print(i)
    for i in result:
        if i=="Banana":
            continue
        print(i)

target_finder(["Apple", "Mango", "Banana"])


#
# 5. Take a list of numbers and, without using any built-in shortcut, work out the largest one using a loop.
# Think about what you need to remember as you walk through, and what it should start as.

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



