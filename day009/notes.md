# Problems:





1. Write code that raises three different errors on purpose: dividing by zero, indexing past the end of a list, and converting "abc" to a number. Read all three tracebacks properly — name the exception type and identify the exact line for each.



Write a function that converts a string to a number and handles bad input gracefully. Then feed it "abc", "", "12.5" and None. Not all of them raise the same error — catch each specifically.



Take your Day 7 read_file function. It currently returns "Sorry, that file does not exist." — a string the caller can't distinguish from real content. Rewrite it two ways: one that raises, one that returns a clear signal of failure. Write down which you'd ship and why.



Go back to find_largest. It returns None for an empty list, which broke bigger_max one layer up on Day 4. Rewrite it to raise a ValueError instead. Then update bigger_max to catch it. Notice that the error is now handled where the caller knows what to do, not where it happened.



Write a function that opens a file, reads it, and uses finally to print a message that appears whether it succeeded or failed. Then make it fail on purpose and confirm the message still appears. This is why with works.



Define your own exception type — something like InvalidRecordError — and raise it when data doesn't meet a rule you choose. Then catch it specifically. This is how real codebases signal domain-specific failures.



The counter-exercise. Write a try/except that catches everything and does nothing with it. Then put a typo inside the try. Watch your own bug get silently swallowed. Write down what you'd tell someone who does this.

