'''A program that reads data about the 2016 Primary election from a CSV file, and then creates a choropelth map
that displays each voting district colored based on the candidate who received the highest percentage of votes in
that district (for that party)'''

import csv
from bs4 import BeautifulSoup

def read_for_democrat_svg(democrat_dictionary):
    '''Colorize the svg map based on the data from the democrat dictionary that has the winning candidate name in each county'''

    fill_color = ''   # default value for fill color

    style_description = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

    with open('counties.svg', 'r') as fin:     # open the file and read in all the data
        svg_data = fin.read()

        soup = BeautifulSoup(svg_data, "html.parser")  # give the data to BeautifulSoup to parse the XML

        paths = soup.findAll('path')     # soup is the XML data, findAll extracts the "path" items

        for p in paths:
            # we want to handle all the id's in the .svg file, but leave the
            # "State_Lines" and "separator" paths alone.
            if p['id'] not in ["State_Lines", "separator"]:  # add code for 1st, 2nd 3rd below

                # First, look for this id in the .csv data dictionary.
                for fips_key in democrat_dictionary:

                    if p['id'] == fips_key:

                        # Second, choose a HEX color code, based on the data.



                        if democrat_dictionary[fips_key] == 'Hillary Clinton':
                            fill_color = '#de2d26'   #red

                        elif democrat_dictionary[fips_key] == 'Bernie Sanders':
                            fill_color = '#bdbdbd'   #tan/ light gray

                        else:
                            fill_color = '#000000'  # black

                        # Third, modify the style, so that the "fill:" entry is this color.
                        # Fourth, change the entry within the BeautifulSoup data structure by:
                        p['style'] = style_description + fill_color

                    else:
                        continue

        with open('democrat_map.svg', mode='w') as out_svg:
             print(soup.prettify(), file=out_svg)  # "prettify" the XML, then write it out '''


def read_for_republican_svg(republican_dictionary):
    '''Colorize the svg map based on the data from the republican dictionary that has the winning candidate name in each county'''

    fill_color = ''      # default value for fill color
    style_description = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

    with open('counties.svg', 'r') as fin:  # open the file and read in all the data
        svg_data = fin.read()

        soup = BeautifulSoup(svg_data, "html.parser")  # give the data to BeautifulSoup to parse the XML

        paths = soup.findAll('path')  # soup is the XML data, findAll extracts the "path" items

        for p in paths:
            # we want to handle all the id's in the .svg file, but leave the
            # "State_Lines" and "separator" paths alone.
            if p['id'] not in ["State_Lines", "separator"]:  # add code for 1st, 2nd 3rd below

                # First, look for this id in the .csv data dictionary.
                for fips_key in republican_dictionary:

                    if p['id'] == fips_key:

                        # Second, choose a HEX color code, based on the data.

                        #fill_color = '#000000'  # black

                        if republican_dictionary[fips_key] == 'Donald Trump':
                            fill_color = '#3182bd'  # blue

                        elif republican_dictionary[fips_key] == 'Ted Cruz':
                            fill_color = '#31a354'  # green

                        elif republican_dictionary[fips_key] == 'Marco Rubio':
                            fill_color = '#f1ca4f'  # yellow

                        elif republican_dictionary[fips_key] == 'John Kasich':
                            fill_color = '#a1d99b'  # mint

                        elif republican_dictionary[fips_key] == 'Ben Carson':
                            fill_color = '#BF5FFF'  # purple

                        else:
                            fill_color = '#000000'   #black


                        # Third, modify the style, so that the "fill:" entry is this color.
                        # Fourth, change the entry within the BeautifulSoup data structure by:
                        p['style'] = style_description + fill_color

                    else:
                        continue

        with open('republican_map.svg', mode='w') as out_svg:
            print(soup.prettify(), file=out_svg)  # "prettify" the XML, then write it out '''


def read_from_csv_file():
    '''A function that reads from the given csv file, creates dictionaries for both republican and democratic party with
    fips as the key and winning candidate name as the value. The function then calls two functions sending corresponding
    dictionaries as arguments'''

    fips = ''                     # default value of fips
    party_name = ''               # default value of party name
    candidate_name = ''           # default value of name of the candidate
    num_votes = ''                # default value for number of votes
    dict_democrat = {}            # dictionary for winners (candidate) from democratic party in each county
    dict_republican = {}          # dictionary for winners (candidate) from republican party in each county

    with open('primary_results.csv', newline='') as csvfile:  # open the file
        reader = csv.reader(csvfile, delimiter=",")  # create the reader object

        for row in reader:  # loop through each row

            # discard the value if fips is greater than 5 digits (here, with decimal points)
            if len(row[3]) > 7:
                continue

            # skip the first row with heading, else update all the variables with current data
            if (fips == ''):
                if row[3] == 'fips':
                    continue
                else:
                    fips = row[3]
                    num_votes = row[6]
                    candidate_name = row[5]
                    party_name = row[4]

            # check to see if we are looking at the votes for the same county and same party
            elif fips == row[3] and party_name == row[4]:
                # check to see if the votes is higher for the the candidate in this row (as compared to the other)
                # update the variables with new data if the votes is higher
                if int(num_votes) < int(row[6]):
                    num_votes = row[6]
                    candidate_name = row[5]

            # if the row gives data for a new county, populate the dictionaries with old data, and then repopulate the variables with new data
            elif fips != row[3] and fips != '':
                fips = fips.strip('.0')     # strip decimal points

                if len(fips) < 5:
                    fips = '0'*(5 - len(fips)) + fips     # add leading zeros to make fips a 5-digit

                if party_name == 'Republican':            # check to see if the previous party was Republican
                   dict_republican[fips] = candidate_name   # populate the republican dictionary with fips as key, winning candidate as value

                elif party_name == 'Democrat':    # check to see if the previous party was Democratic
                    dict_democrat[fips] = candidate_name # populate the democratic dictionary with fips as key, winning candidate as value

                # repopulate variables with data from current row
                fips = row[3]
                num_votes = row[6]
                candidate_name = row[5]
                party_name = row[4]

    read_for_democrat_svg(dict_democrat)   # call the function sending democratic dictionary as the argument
    read_for_republican_svg(dict_republican)  # call the function sending republican dictionary as the argument


def main():
    '''The main() function'''
    read_from_csv_file()    # call the function that reads from csv file and creates dictionaries for winning candidates for each party

# Standard boilerplate to call the main function, if executed.
if __name__ == '__main__':
    main()