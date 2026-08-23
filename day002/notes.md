# WELCOME TO DAY 002

SHALL WE START!!


1. Two names, one list

Make a list. Now make a second name that points at that same list (just assign one to the other; don't copy it). Add an item using the second name. Then print the first one.

Did the first one change? Why would it, when you never touched it?

Now try the same thing with text instead of a list make a string, point a second name at it, "add" to it. Does the first one change this time?

id() shows you the identity of an object. Print it before and after in both experiments. The numbers will tell you what actually happened.

2. A list of lists

Make a list where each item is itself a list. Something like a list of three small lists.

Copy it. Then reach inside the copy, into one of the inner lists, and change something there.

Before you run it: write down in your notes what you think will happen to the original. Then run it and see if you were right.

3. What happens to a list you pass into a function

Write a function that takes a list and adds an item to it. Make a list outside the function, pass it in, call the function. Then print the list from outside.

Was it changed? You didn't return anything or reassign anything; so what does that tell you about what a function actually receives when you pass it a list?

4. The famous trap

Write a function where one of the parameters has an empty list as its default value. Inside, add an item to that list and return it.

Now call the function three times without passing anything in. Print the result each time.

Most people expect the same answer three times. You won't get that. Once you've seen it, work out why; the reason comes straight from problem 1.

5. Why computers are bad at decimals

Add 0.1 and 0.2. Print the result. It won't be what you learned in school.

Figure out why. Then search for how Python lets you do exact decimal math when you need it, and think about why a bank absolutely cannot use the normal way.