# Parsing Errors
Some patterns have been identified as being too problematic for libpostal to parse. The purpose of this document is to explain what the error codes used in `odbiz_custom_parse.py` mean, what criteria was used to spot entries that were given the code, and what was attempted to solve the error. For all entries, if either `street_name` or a valid `street_no` was already provided (the addresses were already parsed by the source), then it was ignored by the error detection. The script also only applies error detection to entries where a `full_address` is provided. The entire dataset was run through libpostal once before any error detection was applied. `odbiz_custom_parse.py` prints out a frequency summary of all combinations of error codes for all entries at the end of it's execution. 

Note that I focused most of my time fixing the `dashes_with_spaces` error since that was the error that made up an *overwhelming majority* of all errors. Often times, the fix applied to `dashes_with_spaces` would also fix many of the problems in other catagories as well.

---

## street_no_blank

### *Summary*
Detects if absolutely no street_no info has been parsed.

### *Conditions*
Check if all of the following columns are blank:
- street_no
- LP_street_no
- LP2_street_no

### *Attempted Solution*
No solution was attempted for this problem

---

## usa_postcode_err

### *Summary*
Detect values incorrectly parsed as USA postal codes

### *Conditions*
For an entry, if every character in `LP_PostCode` is a digit (0-9), then it is classified as a USA postal code

### *Attempted Solution*
Turns out that libpostal just maps these values to the wrong locations. The solution is to re-map columns as follows:
- Map (`LP2_unit` + `LP2_street_no`) to `LP2_unit`
- Map `LP_PostCode` to `LP2_street_no`
- Set `LP_PostCode` to empty string

The function `fix_postcode_errs`() executes this solution.

---

## dashes_with_spaces

### *Summary*
Every time there is a whitespace character adjacent to a dash (-) character, there's a chance that libpostal doesn't parse it properly. But it does parse some of these properly which is annoying to deal with

### *Conditions*
Detects if all of the following are true:
- `full_address` contains whitespaces adjacent to either side of a dash
- All of the following condition are false:
  - `LP_street_name` contains an ordinal number (1st, 2nd, 3rd, 4th...)
  - At least one of the following is true:
    - `LP2_unit` is not blank
    - `LP2_street_no` doesn't contain a whitespace
- `full_address` doesn't start with the `#` character. 

Note: There's a lot of negated conditionals here because it turns out that if the entry does have spaces adjacent to a whitespace AND one of the negated conditions, libpostal likely parses it properly the first time.

### *Attempted Solution*
First, remove any whitespaces that are adjacent to a dash, then feed the entries through libpostal again.

Then, detect any parsing anomolies in the set of re-parsed data using any of the conditions specified by the list `dws_parsing_errs`. If an entry doesn't have any detected anomolies, mark it as "parsed correctly". Note that this may not be true since this method is not 100% thorough. 

If a parsing anomoly was detected after running an entry through libpostal a second time, then keep the values that libpostal assigned to it the first time. These values appear to be better for the ones that weren't improved by passing them through libpostal twice. 

If LP_street_name contains two numerical values seperated by a space, then a re-mapping is necessary:
- Map (`LP2_unit` + `LP2_street_no`) to `LP2_unit`
- Map the leftmost number in `LP_street_name` to `LP2_street_no`
- Set `LP_street_name` to be everything to the right of the leftmost number. 

The function `fix_dashes_with_spaces`() executes this solution.

---

## has_dash_and_1st_col_max

### *Summary*
If `LP_street_no` happens to be a sequence of numbers seperated by dashes, then this detects whether the first number in the sequence is the street number.

### *Conditions*
If the first number is the max of the sequence, then it is considered to be the `street_no`

### *Attempted Solution*
Beyond detecting the street_no, no attempt has been made at solving the error as I couldn't figure out what to do with the rest of the sequence. 

---

## unit_starts_non_digit

### *Summary*
Detects if the unit (the first few characters of `full_address`) starts with a non-digit character

### *Conditions*
Detects if all of the following are true:
- `full_address` contains a dash
- `full_address` starts with a non-digit character

### *Attempted Solution*
No solution was attempted for this problem

---

## blank_street_names

### *Summary*
Detects if libpostal was able to parse a street_name from non-blank full addresses. This is because, in theory, the street_name should be the easiest thing for libpostal to parse, so if it didn't find it, then something went really wrong. Ignores addresses that are "out of town". 

### *Conditions*
All of the following conditions are true:
- `full_address` is not blank
- `LP_street_name` is blank
- `LP_street_name` is not one of the values specified in `OUT_OF_TOWN_VARS_LIST`

### *Attempted Solution*
No solution was attempted for this problem

---

## invalid_street_no

### *Summary*
Detects if the `street_no` contains any non-digit characters

### *Conditions*
See summary

### *Attempted Solution*
No solution was attempted for this problem
