# Problems:

1. Take a list of numbers. Build a new list of their squares; first with a loop and append, then as a comprehension. Put them side by side and read both out loud.

2. From a list of numbers, build a list containing only the even ones. Then only the even ones, squared. Notice where the condition goes versus where the transformation goes.

3. Go back to your Day 6 palindrome function. You wrote a loop that built up a cleaned string character by character; the slow, immutability-violating version. Rewrite the cleaning as a comprehension joined at the end.

4. Take your people dictionary from Day 5. Build a new dictionary mapping each name to just their city. Then one containing only the people over 26. That's a dict comprehension with a filter.

5. Take a sentence and build a set of the unique word lengths in it. Then a dict mapping each word to its length. Compare how much code your Day 6 deduplication took.

6. Now explain your own Day 5 line:
Counter(word.lower().strip(string.punctuation) for word in sentence.split())
Why parentheses and not brackets? What is it handing to Counter, and how is that different from handing it a list? 

7. The counter-exercise. Write a comprehension so dense it's genuinely hard to read; nested, with conditions. 
Then rewrite it as a plain loop. Decide which you'd rather find in your own code in six months, and write down the rule you'd give someone else.