import bisect
from bisect import bisect_left
from itertools import islice
import sys
import time
from datetime import timedelta

start_time = time.monotonic()
input_file = "words for problem.txt"
#input_file = "words_test.txt"

with open(input_file) as cache:
    lines = [line.rstrip('\n') for line in cache]
print("Time to read file and store in list: %s", timedelta(seconds=time.monotonic() - start_time))


def word_exists(wordlist, word_fragment):
    try:
        return wordlist[bisect_left(wordlist, word_fragment)].startswith(word_fragment)
    except IndexError:
        return False  # word_fragment is greater than all entries in wordlist


def find_cat_str_binary(lines):
    outfile = open('outfile_find_cat_str_binary.txt', 'w')
    # outfile.write("binary_search_implementation")
    database = list()
    idx = 0
    for item1 in lines:
        sys.stdout.write("\r[---%d%%---]" % (((idx + 1) / len(lines)) * 100))  # Progress Bar
        sys.stdout.flush()
        # outfile.write("\nitem1: "+item1)
        for item2 in islice(lines[idx + 1:], bisect.bisect_left(lines[idx:], item1), None):  # item2 where
            # for item2 in lines:
            if item2 not in database:
                if item2 == item1:
                    continue
                    # outfile.write("\nrepeated: " + item1)

                elif item2[0:len(item1)] == item1:
                    # print ("suspected: %s", item2)
                    # outfile.write("\nsuspected: " + item2)
                    for item3 in islice(lines, bisect.bisect_left(lines, item2[len(item1)]), None):
                        # for item3 in lines:
                        # outfile.write("\nitem3:"+item3)
                        # outfile.write("\nitem3:"+item3+"compare_str:"+item2[len(item1):len(item3)+len(item1)])
                        if item2.startswith(item3, len(item1), len(item3) + len(item1)):
                            outfile.write("\n" + item2)
                            # if item2[len(item1):len(item3)+len(item1)] == item3:
                            database.append(item2)
                            break


                else:
                    # print("item1 in database:", item1)
                    # outfile.write("\nitem2: "+item2 + " item1: "+item1)
                    continue
            else:
                # print("item2 in database:", item2)
                continue
        idx += 1

    outfile.close()
    # print(database)
    database = list(set(database))
    return database


def find_cat_strings(lines):
    outfile = open('outfile_find_cat_strings.txt', 'w')
    index = 0
    database = list()
    possible_words = list(items for items in lines if lines.count(items) > 1)
    print("possible words:", len(possible_words), "list:", possible_words)
    for item1 in lines:
        if database.count(item1) > 0:
            continue
        elif len(item1) == 0:
            # print ("null string:", item1)
            continue
        else:
            sys.stdout.write("\r[--%d%%--]" % (((index + 1) / len(lines)) * 100))  # Progress Bar
            sys.stdout.flush()
            # print("item1:", item1,"index:" ,index, "len_of_lines", len(lines))
            word_exists(lines, item1)
            matching = [items for items in lines if items.startswith(item1, 0, len(item1))]
            # print("matching:", matching)
            for item2 in matching:
                if database.count(item2) == 0:
                    if item1 == item2:
                        continue
                        # print("replica:", item2)
                    elif len(item2) == 0:
                        # print ("null string:", item2)
                        continue
                    else:
                        # print("item2(possible str):", item2)
                        for item3 in lines:
                            if item3.startswith(item2[len(item1)]):
                                # print("item3: ", item3, "compare_str:", item2[len(item1):len(item3) + len(item1)])
                                if len(item3) == 0:
                                    # print ("null string:", item3)
                                    continue
                                elif len(item3) <= len(item2[len(item1):len(item3) + len(item1)]):
                                    if item2[len(item1):len(item3) + len(
                                            item1)] == item3:  # check only for list items matching the starting letter of remaining string
                                        check = [items for items in database if items == item2]
                                        # print ("check:",check)
                                        if check == item2:
                                            continue
                                            # print ("item duplicate in database")
                                        else:
                                            # print("\nstring of words found: %s ", item2, "word exists in database:", database.count(item2))
                                            database.append(item2)
                                            outfile.write("\n" + item2)
                                            # database = list(set(database))
                                            break
                                    else:
                                        continue
                                        # print ("Mismatch: item3:",item3, "compare_str:", item2[len(item1):len(item3)+len(item1)])
                                else:
                                    continue
        index += 1
    database = list(set(database))
    outfile.close()
    # print("\n", database)
    return database


def find_cat_strings2(lines):
    outfile = open('outfile_find_cat_strings.txt', 'w')
    index = 0
    database = list()
    for item1 in [items for items in lines if database.count(items) == 0 and len(items) > 0]:
        sys.stdout.write("\r[--%d%%--]" % (((index + 1) / len(lines)) * 100))  # Progress Bar
        sys.stdout.flush()
        for item2 in [items for items in lines if items.startswith(item1, 0, len(item1)) and items is not item1 and len(items) !=0 and database.count(items) == 0]:
            if len([items for items in lines if item2.startswith(items, len(item1), len(items)+len(item1)) and len(items) !=0]) > 0:
                database.append(item2)
        index += 1
    #database = list(set(database))
    outfile.close()
    print("\n", database)
    return database


'''
start_time_bin = time.monotonic()
strings = find_cat_strings(lines)
exec_time_bin = timedelta(seconds=time.monotonic() - start_time_bin)
print("Total execution time for find_cat_strings: %s", exec_time_bin)
strings.sort(key=len, reverse=True)
print("Longest concatenated word:", strings[0])
print("2nd Longest concatenated word:", strings[1])
print("Total count of all concatenated words:", len(strings))

# outfile = open('outfile.txt', 'w')
# outfile.write("binary_search_implementation")
'''
start_time_non_bin = time.monotonic()
strings = find_cat_strings2(lines)
exec_time_non_bin = timedelta(seconds=time.monotonic() - start_time_non_bin)
print("Total execution time for find_cat_strings: %s", exec_time_non_bin)
strings.sort(key=len, reverse=True)
print("Longest concatenated word:", strings[0])
print("2nd Longest concatenated word:", strings[1])
print("Total count of all concatenated words:", len(strings))

'''
print("Performance benchmark: find_cat_str2 search is ", ((exec_time_non_bin - exec_time_bin) / exec_time_bin) * 100,
      "% faster than find_cat_str")

'''