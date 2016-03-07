import bisect
from bisect import bisect_left
from itertools import islice
import sys
import time
from datetime import timedelta

start_time = time.monotonic()
#input_file = "words for problem.txt"
input_file = "words_test.txt"

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

def is_concat_str(item2,start_length):

    #print ("\nitem2:",item2,"start_len",start_length)
    for item3 in lines:
        #print ("item3:",item3, "compare_str:",item2[start_length:], "start_length",start_length)
        if item2.startswith(item3,start_length):#todo compare_length to be factored in
            #print("item3: ", item3, "compare_str:", item2[start_length:len(item3) + start_length])
            #if len(item3) <=                                                                           KUNAL KHANNA
            #print ("item3:",item3)
            if len(item3) == 0:
                #print ("null string:", item3)
                continue
            elif len(item3) + start_length == len(item2):
                #print ("matched:",item2[:start_length],"item3:",item3, "compare_str:",item2[start_length:], "start_length",start_length)
                #print("Concat_str:",item2)
                return 1
            else:
                #print ("matched:",item2[:start_length],"item3:",item3, "compare_str:",item2[start_length:], "start_length",start_length)
                #start_length += len(item3)
                #print("potential string of words found:", item2,"start_length:",start_length)
                if is_concat_str(item2,start_length+len(item3)):#if concat_str identified, return 1
                    #print("Concat_str:",item2)
                    return 1
                else:# if concat_str not identified, move on to next comparison
                    continue
    return 0

def find_cat_strings(lines):
    outfile = open('outfile_find_cat_strings.txt', 'w')
    index = 0
    database = list()
    #possible_words = list(items for items in lines if lines.count(items) > 1)
    #print("possible words:", len(possible_words), "list:", possible_words)
    for item1 in lines:
        if database.count(item1) > 0:
            continue
        elif len(item1) == 0:
            # print ("null string:", item1)
            continue
        else:
            sys.stdout.write("\r[--%d%%--]" % (((index + 1) / len(lines)) * 100))  # Progress Bar
            sys.stdout.flush()
            #print("item1:", item1,"index:" ,index, "len_of_lines", len(lines))
            #word_exists(lines, item1)
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
                        #print("item2(possible str):", item2)
                        start_length = len(item1)
                        if is_concat_str(item2,start_length): #start_length is fixed here. change to chack for all starting string matches.
                            database.append(item2)

        index += 1
    database = list(set(database))
    outfile.close()
    #print("\n", database)
    return database

def find_cat_strings3(lines):
    outfile = open('outfile_find_cat_strings.txt', 'w')
    index = 0
    database = list()
    words = list()
    floating_word = lines[0]
    for item1 in lines:
        sys.stdout.write("\r[--%d%%--]" % (((index + 1) / len(lines)) * 100))  # Progress Bar
        sys.stdout.flush()
        print ("item1", item1)
        if database.count(item1) > 0:
            continue
        elif len(item1) == 0:
            # print ("null string:", item1)
            continue
        elif item1 == floating_word: # first item of same floating word list
            print ("item1:",item1,"= floating word:", floating_word)
            continue
        else:
            print ("floating_word:", floating_word, "compare string", item1)
            if item1.startswith(floating_word):
                print("item1(possible str):", item1)
                is_string=0
                #for item3 in islice(lines, bisect.bisect_left(lines, item1[len(floating_word)]), None):#todo: modify logic to search only in words database.
                for item3 in lines:
                    if item3.startswith(item1[len(floating_word)]):#todo check logic
                        print("item3:", item3, "compare_str:", item1[len(floating_word):len(item3) + len(floating_word)])
                        if len(item3) == 0: #NULL string
                            # print ("null string:", item3)
                            continue
                        if item1[len(floating_word):len(item3) + len(
                                floating_word)] == item3:  # check only for list items matching the starting letter of remaining string
                            print("\nstring of words found:", item1, "word exists in database:", database.count(item1))
                            database.append(item1)
                            outfile.write("\n" + item1)
                            is_string=1
                            break
                        else:
                            print ("Mismatch: item3:",item3, "compare_str:", item1[len(floating_word):len(item3)+len(floating_word)])
                            continue
                if is_string == 0:
                    print ("word_check2:",item1)
                    if floating_word in item1:
                        floating_word.append(item1)
                    else:
                        floating_word=item1
                    continue
            else:
                if floating_word in item1:
                    floating_word.append(item1)
                else:
                    floating_word=item1
                print ("word_check3:",item1)
                continue
        index += 1
    database = list(set(database))
    outfile.close()
    print("\n", database)
    return database




def find_cat_strings_5(lines):
    index = 0
    database = list()
    #items in list if database does not contain items already and items are not null.
    for item1 in [items for items in lines if database.count(items) == 0 and len(items) > 0]:
        sys.stdout.write("\r[--%d%%--]" % (((index + 1) / len(lines)) * 100))  # Progress Bar
        sys.stdout.flush()
        #items in list if item starts with item1 and item is not equal to item1 and item is not null and item is not in database.
        for item2 in [items for items in lines if items.startswith(item1, 0, len(item1)) and items is not item1 and len(items) !=0 and database.count(items) == 0]:
            #items in list that contain items in item2 object where item1 ends till length of item2 object and item is not null. TODO: could be improved to find first match only.
            if len([items for items in lines if item2.startswith(items, len(item1), len(items)+len(item1)) and len(items) !=0]) > 0:
                database.append(item2)
        index += 1
    #database = list(set(database))
    #outfile.close()
    print("\n", database)
    return database




def find_cat_strings4(lines):
    outfile = open('outfile_find_cat_strings.txt', 'w')
    index = 0
    database = list()
    possible_words = list(items for items in lines if lines.count(items) > 1)
    #print("possible words:", len(possible_words), "list:", possible_words)
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
                        count = len(item2) - len(item1)
                        while count !=0:
                            for item3 in lines:
                                if item3.startswith(item2[len(item1)]):#todo check logic
                                    # print("item3: ", item3, "compare_str:", item2[len(item1):len(item3) + len(item1)])
                                    if len(item3) == 0:
                                        # print ("null string:", item3)
                                        continue
                                    elif len(item3) <= len(item2[len(item1):len(item3) + len(item1)]):
                                        if item2[len(item1):len(item3) + len(
                                                item1)] == item3:  # check only for list items matching the starting letter of remaining string
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
    print("\n", database)
    return database

def find_cat_strings2(lines):
    outfile = open('outfile_find_cat_strings.txt', 'w')
    index = 0
    database = list()
    #items in list if database does not contain items already and items are not null.
    for item1 in [items for items in lines if database.count(items) == 0 and len(items) > 0]:
        sys.stdout.write("\r[--%d%%--]" % (((index + 1) / len(lines)) * 100))  # Progress Bar
        sys.stdout.flush()
        #items in list if item starts with item1 and item is not equal to item1 and item is not null and item is not in database.
        for item2 in [items for items in lines if items.startswith(item1, 0, len(item1)) and items is not item1 and len(items) !=0 and database.count(items) == 0]:
            #items in list that contain items in item2 object where item1 ends till length of item2 object and item is not null. TODO: could be improved to find first match only.
            if len([items for items in lines if item2.startswith(items, len(item1), len(items)+len(item1)) and len(items) !=0]) > 0:
                database.append(item2)
        index += 1
    database = list(set(database))
    outfile.close()
    print("\n", database)
    return database



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
strings = find_cat_strings3(lines)
exec_time_non_bin = timedelta(seconds=time.monotonic() - start_time_non_bin)
print("Total execution time for find_cat_strings: %s", exec_time_non_bin)
strings.sort(key=len, reverse=True)
print("Longest concatenated word:", strings[0])
print("2nd Longest concatenated word:", strings[1])
print("Total count of all concatenated words:", len(strings))


print("Performance benchmark: find_cat_str3 search is ", ((exec_time_non_bin - exec_time_bin) / exec_time_bin) * 100,
      "% faster than find_cat_str")
'''