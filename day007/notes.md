
# Questions


1. Write a few lines of text to a new file. Close it, open it in your editor, and confirm it's really there. Then read it back and print it. You've now made something that outlives your program.


2. Open that same file in "w" mode again and write a single short line. Look at the file. Everything else is gone. Sit with that for a second — then find the mode that adds to the end instead of destroying.



3. Read a file line by line and print each line with its line number. Your output will have blank lines between entries — work out why, then fix it. That's the trailing newline, and finding it yourself is the point.



4. Take the word-count program from Day 5 and point it at a real text file instead of a hardcoded sentence. Print the ten most common words. Your Day 5 cleaning — lowercase, strip punctuation — carries over. (Grab any plain-text file: paste an article into one, or use one of your own notes files.)



5. Write the results of problem 4 back out to a new file, one word,count per line. You've now built a read → process → write pipeline, which is the shape of essentially every data program ever written.



6. Try to open a file that doesn't exist. Read the error. Then write a function that reads a file if it's there and returns something sensible if it isn't — without crashing. You'll need to look up try/except; this is your first contact with error handling, and we'll do it properly soon.

