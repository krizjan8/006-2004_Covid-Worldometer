# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:52:22 2020

@author: krizh
"""

from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import codecs
import timeit


def get_page_raw(url, code):
    """Returns raw html page in text version"""

    htmt_file = code +".html"
    try:
        return requests.get(url).content # do error handling
    
    except:
        try:
            file = codecs.open(htmt_file, 'r')
            print("Web page cannot be reached. Data loaded from file!")
            return file.read()
        
        except FileNotFoundError:
            print("Neither Web Page nor Data file can be reached!")
            return ''

class Country():
       
   def __init__(self, name, data, base_url, phrase):
       self.name = name
       self.pop = data["Pop"] * 1000000 #input is in milions
       self.code = data["Code"]
       self.url = "{}{}/".format(base_url,self.code)
       self.deaths = [i for i in self.fetch_data(phrase) if i > 100]
       
   def get_death_promile(self):
       """Returns daily covid19 death people per 1000"""
       foo = [i/self.pop*1000 for i in self.deaths] #divides
       a = []
       avg_bins = 7
       for i,x in enumerate(foo):
           buf = 0
           if i < avg_bins:
                continue
           for y in range(avg_bins):
               buf = foo[i-y] + buf
               
           a.append(buf/avg_bins) 
       return a    
       #return [i/self.pop*1000 for i in self.deaths] #divides
      

   def fetch_data(self,phrase):
       
       
       page_data = get_page_raw(self.url, self.code)
       if page_data != '':
        
           soup = BeautifulSoup(page_data, 'html.parser') #page_data.content
           data = soup.find_all('script')
           text = ''    
           results = []
           for x in data:
               results.extend(x)
           
           for x in results:
               if phrase in x: #matches = re.finditer(regex, results[9], re.MULTILINE)
                     text = x
                   
           regex = r"data: \[(.*?)\]"
           result = re.findall(regex, text)
           return [float(i) for i in result[0].split(",") if i != 'null'] # divide text to array of numbers (string) and type cast them to float
       else:
          raise NoData('No data')
                
               

class NoData(Exception):
    pass

def plotgraph(countries, title):
    try:
        print("Yesterday:")
        for y in countries:
           data = y.deaths
           plt.plot(y.get_death_promile(),label=y.name) 
           print(y.name + ' {:.2f}'.format(data[len(data)-1]-data[len(data)-2]))
           
        plt.legend()
        plt.xlabel("Day of pandemy")
        plt.ylabel("Death people per 1000")
        plt.title("Covid - "+ title)
        plt.grid(True)
        
        plt.show()
        
        
        
    except NoData:
        print("Graph not plotted: No Data !")


# inputs
url = "https://www.worldometers.info/coronavirus/country/" #https://www.worldometers.info/coronavirus/country/sweden/
#countries_in = {"France": 66.99, "Italy": 60.36, "Spain": 46.94, "United States": 327.2, "Germany": 83.02}

#main
countries_in = {"France": {"Pop": 66.99, "Code": "france"},
                "Sweden": {"Pop": 10.23, "Code": "sweden"},
                "Cz": {"Pop": 10.65, "Code": "czech-republic"},
                "Germany": {"Pop": 83.02, "Code": "germany"},
                "USA": {"Pop": 327.2, "Code": "us"},
                "Spain": {"Pop": 46.94, "Code": "spain"},
                "Brazil": {"Pop": 209.5, "Code": "brazil"},
                "UK": {"Pop": 66.65, "Code": "uk"},
                "Italy": {"Pop": 60.369, "Code": "italy"},
                "Russia": {"Pop": 144.5, "Code": "russia"},
                "Belgium": {"Pop": 11.58, "Code": "belgium"},
                }

countries = []

#phrase = "Total Coronavirus Cases"
#phrase = "Total Coronavirus Deaths" 
phrase = "Novel Coronavirus Daily Cases"
program = """
for name, data in countries_in.items():
    countries.append(Country(name, data, url, phrase))

plotgraph(countries, phrase)"""


#time = timeit.timeit('plotgraph(countries_in, url)', globals=globals(), number=1)
time = timeit.timeit(program, globals=globals(), number=1)
print("Script last: ", '{:.3}'.format(time) ,"s")



