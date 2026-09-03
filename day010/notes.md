# Problems

Create a small CSV by hand in your editor — five people, columns name,age,city. Read it with csv.reader and print each row. 
Then read it with DictReader and print each row. Compare what you get and write down which you'd rather work with.

Sum the ages. It will fail. Understand exactly why before fixing it — this is the Day 5 "29" + "32" problem arriving from a real file. Then fix it, and handle the case where a row has a non-numeric age.

Now sabotage your file. Give one person a city like "Springfield, Illinois" — with a real comma inside quotes. Read it first by splitting on commas yourself, then with csv.reader. Confirm the manual version silently produces garbage.

Write a filtered subset back out — people over 26 — using DictWriter. Open the result and check the header is there.

Write a function that reads a CSV and returns a list of dicts, but rejects bad rows: wrong field count, missing name, unparseable age. Return the good rows and a list of rejections with the line number and the reason for each.

Point it at a deliberately awful file — blank lines, a row with too few fields, a row with too many, an age of "twenty", a name that's just spaces. Confirm your count of good plus rejected equals the number of data rows in the file. If it doesn't, your counting is lying to you.