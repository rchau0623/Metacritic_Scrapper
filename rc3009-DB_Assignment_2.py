# -*- coding: utf-8 -*-
# Ryan Chau - rc3009

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
    
def getData():
    
    # Here I set up the initial url for the first page to be scraped.
    url = 'http://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&sort=desc&page='
    rank = 0 # Here is the 'ranking,' that is the order the games show up in the listing.
    output = 'output.csv' # This is the name of my output file.
    output_file = open(output, 'w')
    # This is my header, I decided the order of the columsn here, to be in order of relevance to a user
    output_file.write('Rank,Title,Metascore,Average User Score,Release Date,Publisher,Genre,Maturity Rating,Platform List\n')
    
    # I decided to scrap 50 pages so that I would get 5000 rows
    for i in range(50):
        try:
            # This line I found on the internet. I was required to set my header in order to scrape metacritic.
            hdr = {'User-Agent': 'Mozilla/5.0'}
            # Here I increment the page number in the url by i.
            request = Request(url+str(i),headers=hdr)
            page = urlopen(request)
        except Exception as e:
            print("URL is not responding.")
            print(e)
        else: 
            # Using BeautifulSoup to scrape each page of a 100 listings each.
            soup = BeautifulSoup(page, 'html.parser')
            games = soup.find_all('div', class_='wrap product_wrap')
            
            for j in range(100):
                rank += 1 # incrementing the rank so that I start at 1
                title = games[j].h3.a.contents[0] # finding the title
                metascore = games[j].find('span', class_='metascore_w').contents[0] # getting the title
                more_stats = games[j].find('ul', class_='more_stats') # all the other information is stored under a ul tag labeled more stats
                release_date = more_stats.find('li', class_='stat release_date').find('span', class_='data').contents[0] # release date
                # I initialize the maturity rating to be an empty string, so that if no maturity rating is found, the column for that listing will be empty.
                # I do this for most of the other columns as well, so that the code will not break. I decided not to replace the data, as that would require
                # manual entry.
                maturity_rating = ''
                if (more_stats.find('li', class_='stat maturity_rating') is not None):
                    maturity_rating = more_stats.find('li', class_='stat maturity_rating').find('span', class_='data').contents[0] # maturity rating
                publisher = ''
                if (more_stats.find('li', class_='stat publisher') is not None):
                    publisher = more_stats.find('li', class_='stat publisher').find('span', class_='data').contents[0] # publisher
                genre = ''
                if(more_stats.find('li', class_='stat genre') is not None):
                    # the formating for the genres were weird, with a lot of empty space in the html, so i replaced all the spaces with nothing,
                    # all the escape characters with nothing, and then proceeded to add spaces after the commas.
                    genre = more_stats.find('li', class_='stat genre').find('span', class_='data').contents[0].replace(' ', '').replace('\n', '').replace(',', ', ') # genres
                avguserscore = ''
                if (more_stats.find('li', class_='stat product_avguserscore') is not None):
                    # As all average user scores were computed out of 10, as opposed to the critic system of out of a 100, I removed the decimal
                    # so average user scores would match critic scores. I could not simply multiply by 10 because I could not find a way to compare
                    # navigable strings to 'tbh' which was there in the case that there were no user scores. Thus I couldn't filter and multiply.
                    avguserscore = more_stats.find('li', class_='stat product_avguserscore').find('span', class_='data').contents[0].replace('.', '')
                # Each platform in the platform list had an associated link. I do this to remove the a tags.
                platform_list = more_stats.find('li', class_='stat platform_list').find('span', class_='data').find_all('a')
                platforms = ''
                for platform in platform_list:
                    # Here I am removing all the a tags and separating platforms by commas. 
                    platforms += platform.contents[0] +  ','
                # Here I compile all my information separated by commas, to be written into the output file in csv format. For any information that has a comma in it,
                # I surrounded that chunk of information with double quotes, as this is the escape character for csv files.
                row = str(rank) + ',\"' + title + '\",' + str(metascore) + ',' + str(avguserscore) + ',\"' + release_date + '\",\"' + publisher + '\",\"' + genre + '\",' + maturity_rating + ',\"' + platforms[:len(platforms)-1] + '\",\n'
                output_file.write(row)
        # Here I print the page number of the page that just completed scraping.
        print(i)
        
    output_file.close()
    
    
# Function call to run it.
getData()

