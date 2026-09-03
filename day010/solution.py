    # Create a small CSV by hand in your editor — five people, columns name,age,city. Read it with csv.reader and print each row.
    # Then read it with DictReader and print each row. Compare what you get and write down which you'd rather work with.
    import csv

    with open("test_csv.csv", newline="", encoding="utf-8") as file:
        result = csv.reader(file)

        for row in result:
            print(row)



    with open("test_csv.csv", newline="", encoding="utf-8") as file:
        result = csv.DictReader(file)

        for row in result:
            print(row)

    with open("test_csv.csv", newline="", encoding="utf-8") as file:
        for line in file.readlines():
            result = line.strip().split(",")
            print(result)

    # Sum the ages. It will fail. Understand exactly why before fixing it —
    # this is the Day 5 "29" + "32" problem arriving from a real file. Then fix it, and handle the case where a row has a non-numeric age.

    import csv

    total = 0

    with open("test_csv.csv", newline="", encoding="utf-8") as file:
        result = csv.DictReader(file)

        for row in result:
            try:
                total += int(row["Age"])
            except ValueError:
                print(f"Invalid age: {row['Age']}")

    print(total)



    # Now sabotage your file. Give one person a city like "Springfield, Illinois" — with a real comma inside quotes.
    # Read it first by splitting on commas yourself, then with csv.reader. Confirm the manual version silently produces garbage.




    with open("test_csv.csv", newline="", encoding="utf-8") as file:
        for line in file.readlines():
            result = line.strip().split(",")
            print(result)

    with open("test_csv.csv", newline="", encoding="utf-8") as file:
        result = csv.reader(file)

        for row in result:
            print(row)


    # Write a filtered subset back out — people over 26 — using DictWriter. Open the result and check the header is there.

    import csv

    # Open the original CSV
    with open("test_csv.csv", "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        # Open a new CSV to write to
        with open("filtered.csv", "w", newline="", encoding="utf-8") as new_file:

            writer = csv.DictWriter(new_file, fieldnames=reader.fieldnames)

            # Write the header
            writer.writeheader()

            # Go through each person
            for row in reader:

                # Age from CSV is a string, so convert it to int
                age = int(row["Age"])

                # Only write people over 26
                if age > 26:
                    writer.writerow(row)


    # Write a function that reads a CSV and returns a list of dicts, but rejects bad rows:
    # wrong field count, missing name, unparseable age. Return the good rows and a list of rejections with the line number and the reason for each.
    import csv

    def read_csv(filename):
        good_rows = []
        rejections = []

        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, restkey="extra")

            for line_num, row in enumerate(reader, start=2):

                # Wrong number of fields
                if "extra" in row or None in row:
                    rejections.append((line_num, "wrong field count", row))
                    continue

                # Missing or blank name
                if not row["Name"] or not row["Name"].strip():
                    rejections.append((line_num, "missing name", row))
                    continue

                # Bad or empty age
                try:
                    row["Age"] = int(row["Age"])
                except (ValueError, TypeError):
                    rejections.append((line_num, "bad age", row))
                    continue

                # Good row
                good_rows.append(row)

        return good_rows, rejections


    good_rows, rejections = read_csv("text.csv")

    print("Rows accepted:", len(good_rows))
    print("Rows rejected:", len(rejections))
    print("Rows read:", len(good_rows) + len(rejections))

    print("\nRejections:")

    for rejection in rejections:
        print(rejection)