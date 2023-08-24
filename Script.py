from bs4 import BeautifulSoup
import pprint
import requests
import os

data = []
year_list = []
result = {
            "form_number": '',
            "form_title": '',
            "min_year": '',
            "max_year": ''
                }

def pdf_download(pdf_url, form_number, year):
    '''download pdfs from IRS website and save in its own folder '''
    print(pdf_url)
    r = requests.get(pdf_url, stream = True)
    
    try:
        os.mkdir(form_number)
    except Exception as e:
        print(e) 
        

    with open(f'{form_number}/{form_number} - {year}.pdf',"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            # writing one chunk at a time to pdf file
            if chunk:
                pdf.write(chunk)
iii = 0

def find(search_url):
    global iii
    '''Search the search_url for specific elements in all pages.
    The result is part of the final json output. '''

    req = requests.get(search_url)
    if req.status_code == 200:
        # print(f'*****Weblink is working properly!*****')
        soup = BeautifulSoup(req.content, 'html.parser')

        all_rows = soup.findAll("tr")

        for row in all_rows[5:]:
            # xpath //*[@id="tablesaw-2900"]/tbody/tr[1]/td[1]/span/a
            form_number = row.find_all('td')[0].text
            form_title = row.find_all('td')[1].text
            year = row.find_all('td')[2].text
            pdf_url = row.find_all('td')[0].find('a')['href']
            result["form_number"] = form_number
            result["form_title"] = form_title
            year_list.append(year)
        
            for print_year in print_years:
                print(f'downloading.. {print_year}')
                pdf_download("https://www.irs.gov" + '/' + pdf_url, form_number, year)

        if soup.find(class_='errorBlock'):
            print('No Results were found, check inputs')
            return
        

        iii+=1
        next_page_partial = "?page="+str(iii)
        print(next_page_partial)
        find( f'https://www.irs.gov/prior-year-forms-and-instructions?find=%20&page=' + str(iii))
        return

    result["min_year"] = year_list[-1]
    result["max_year"] = year_list[0]
    data.append(result.copy())
    return data

####################################################

searches = input('Please enter the complete tax form number seperate by a comma follow by a space (not case sensitive): \n(ie. Form W-2, Form 1095-C, Form W-3, etc)\n>>').split(', ')

# testing:
# searches = ['forc', "Form W-2", "Form 1095-C"]
# searches = ['form 1095-c']
# download = 'y'

download = input('Would you like to download all related pdfs? (Y/N)\n>>')

'''If download is yes, this will generate a list of year based on input'''
if download =='y':
    print_range = input('Please provide the year range by using a dash in between the years (starting year must be smaller than ending year): (ie. 2018-2020)\n').split('-')
    # print_range = '2018-2021'.split('-')
    if int(print_range[0])> int(print_range[1]):
        print('Date range error. Unable to download files. Please rerun the program.\n')
        print_years = []

    else:
        print_years = [year for year in range(int(print_range[0]), int(print_range[1])+1)]
else:
    print_years = []



#Set initial URLs
base_url = 'https://apps.irs.gov/'

# Starts here
for search_item in searches:
    format_search = search_item.replace(' ', '+')

    # Generate a search url based on inputs.
    search_url = f'https://www.irs.gov/prior-year-forms-and-instructions?find=%20&page=' + str(iii)

    print(f'Currently searching {search_item} at this link: \n{search_url}\n')
    find(search_url)

print('***Task completed***')

if print =='y':
    print('All pdf files have been downloaded')

print('Final output is --> \n')
print(f'{pprint.pprint(data)}')
