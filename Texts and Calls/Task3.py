"""
Intro to Python Lab 1, Task 3

Complete each task in the file for that task. Submit the whole folder
as a zip file or GitHub repo. 
Full submission instructions are available on the Lab Preparation page.
"""

"""
Read file into texts and calls. 
It's ok if you don't understand how to read files
You will learn more about reading files in future lesson
"""
import csv

with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)

"""
TASK 3:
(080) is the area code for fixed line telephones in Bangalore. 
Fixed line numbers include parentheses, so Bangalore numbers 
have the form (080)xxxxxxx.)

Part A: Find all of the area codes and mobile prefixes called by people
in Bangalore. 
 - Fixed lines start with an area code enclosed in brackets. The area 
   codes vary in length but always begin with 0.
 - Mobile numbers have no parentheses, but have a space in the middle
   of the number to help readability. The prefix of a mobile number
   is its first four digits, and they always start with 7, 8 or 9.
 - Telemarketers' numbers have no parentheses or space, but they start
   with the area code 140.

Print the answer as part of a message:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
The list of codes should be print out one per line in lexicographic order with no duplicates.

Part B: What percentage of calls from fixed lines in Bangalore are made
to fixed lines also in Bangalore? In other words, of all the calls made
from a number starting with "(080)", what percentage of these calls
were made to a number also starting with "(080)"?

Print the answer as a part of a message::
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
The percentage should have 2 decimal digits
"""

def get_prefix(number):
    if number.startswith('('):
        prefix, _, _ = number[1:].partition(')')
        return prefix
    elif ' ' in  number and number[0] in '789':
        return number[:4]
    elif ' ' not in  number and number.startswith('140'):
        return '140'
    else:
        return ''

def is_bangalore(number):
    return number.startswith('(080)')

codes = {get_prefix(to_no)
         for from_no, to_no, _, _ in calls
         if is_bangalore(from_no)}
codes -= {'140', ''}

# Part A:
print('The numbers called by people in Bangalore have codes:')
print(*sorted(codes), sep='\n')

# Part B:

from_bangalore = [c for c in calls
                    if is_bangalore(c[0])]

both_bangalore = [c for c in from_bangalore
                    if is_bangalore(c[1])]

proportion = len(both_bangalore) / len(from_bangalore)

message = f'{proportion:.2%} percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.'
print(message)

