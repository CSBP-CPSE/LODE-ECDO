# Address Formatting

The scripts in this directory are used to standardise street names to make street name matching easier. The functions that format addresses are "AddressClean_en" and "AddressClean_fr". They are both functions that read in a pandas dataframe where one column constains street names, the name of the column to change, and the name of a column for the modified street names.

The formatting functions apply three main processes to the input addresses. These are
* removing punctuation
* standardising directions (e.g., north &rarr; n)
* standardising street types (e.g., street &rarr; st)

While removing punctuation is done universally (i.e., all punctuation is removed), there are additional rules that determine how street directions and names are processed.
* in english, directions are shortened only if they are the first or last words of a string, while in french only if they are the last word (this may change)
* in english, street types are shortened only if they are the last word of the string, or, the 2nd last word if the last word is a direction. In french, street types are shortened only if they are the first word of the string. This is because in French the street type is typically before the street name, though this is not true for numbered streets (e.g., 4e av), and so an additional rule will be implemented for those cases in the future.

An example of how english and french rules are applied to some street names (in 'example.csv' and 'example_formatted.csv') is shown below:

| street_name             | formatted_en            | formatted_fr            |
|-------------------------|-------------------------|-------------------------|
| fourth avenue           | fourth av               | fourth avenue           | 
| 4th avenue              | 4th av                  | 4th avenue              | 
| park square             | park sq                 | park square             | 
| island park             | island pk               | island park             | 
| second street east      | second st e             | second street east      | 
| west 100 street north   | w 100 st n              | west 100 street north   | 
| confederation boulevard | confederation blvd      | confederation boulevard | 
| boulevard confederation | boulevard confederation | boul confederation      | 
| chemin albert           | chemin albert           | ch albert               | 
| albert chemin           | albert chemin           | albert chemin           | 
| chemin albert nord      | chemin albert nord      | ch albert n             | 
| ouest rue 100 nord      | ouest rue 100 nord      | ouest rue 100 n         | 
