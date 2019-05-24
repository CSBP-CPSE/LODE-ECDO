# Address Matching
The scripts in this directory use fuzzy string matching (via the [fuzzy wuzzy](https://github.com/seatgeek/fuzzywuzzy) library) to match addresses across databases. The primary purpose in this instance is to perform a limited sort of geocoding, where addresses in an open database of addresses that are not geocoded can be matched up against addresses in an OpenAddress (or other) list of geocoded addresses.

The general approach is to read in two csv files to be matched against each other (in this case, the first is a list of addresses to be geocoded, and the second is a list of addresses with geocoordinates). 
The general approach is, for every address in the first database, to look for matches by first restricting the other database to only matching street numbers, and then performing fuzzy string matching on the street names.

Fuzzy string matching is in some ways a dangerous way to perform address matching. This is because, for example, '98 st e' and '99 st e' are only one character apart and would therefore be considered a close match, as would 'main st e' and 'main st w'. There are therefore several rules applied to make this fuzzy matching slightly less naive:
* directions need to match exactly. if one string ends with a direction and the other ends in a different (or no) direction, then it is explicitly not a match.
* If a street name is itself a number (e.g., 98 street) then the match has to be a string that begins with the same number.
* the 'best' match has to be significantly better than the next best match. This way, if fuzziness means that two different strings are a good match for a given string, then neither are selected to avoid a bad match.

A small example of output from matching addresses of public libraries from the City of Ottawa's open data portal against the city's open address data is shown below:

| street_no | street_name  | match_name            | score | lon          | lat         | validity |
|-----------|--------------|-----------------------|-------|--------------|-------------|----------|
| 2782      | 8th line     | 8th line rd           | 84    | -75.4697823  | 45.2295893  | TP       |
| 7749      | bleeks       | bleeks rd             | 80    | -75.93912    | 45.1652793  | TP       |
| 101       | centrepointe | centrepointe dr       | 89    | -75.76128546 | 45.34449722 | TP       |
| 2036      | ogilvie      | ogilvie rd            | 82    | -75.6006177  | 45.4368362  | TP       |
| 6579      | fourth line  | fourth line rd        | 88    | -75.7174918  | 45.1329446  | TP       |
| 1705      | orléans      | orleans, boulevard d' | 52    |              |             | FN       |
| 5630      | osgoode main | osgoode main st       | 89    | -75.6030625  | 45.1473892  | TP       |

most of these matches are determined to be true positives - that is, real matches. One entry was determined not to be a match because the score is so low, but it is actually still the correct address.
In this example, most of the streets in the input database don't include a street type, which doesn't help the matching. A similar problem was encountered in Edmonton: nearly every street in Edmonton is northwest because [Edmonton lies nearly entirely within the northwest quadrant of Edmonton](https://www.vueweekly.com/nw-of-what-the-story-of-edmontons-offset-quadrant-system/). The result of this is that many addresses are written without 'nw' appended, and so they do not match against address lists when the directions are entered. This has so far been encountered in a database of educational facilities in Edmonton, where most addresses are written with the directions omitted.
