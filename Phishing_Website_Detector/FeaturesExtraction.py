import csv                                #To Open Csv Output File
import tldextract                         #To Extract Top level Domain of our URL
import requests                           #To Provide our script with Internet Connectivity 
from bs4 import BeautifulSoup             #To Extract our DOM(Document Object Model)-Tree of our URL
from urlextract import URLExtract         #Extract All URL's  from our given URL

class Extract_Features:
    
    def __init__(self, url):
        self.extracted_features = []
        self.count = 0
        self.url = url
        
        #Feature 1
    def __url_features(self):
        flag = 0
        
        if self.url.count('.') >= 4:
            flag = 1
            
        self.extracted_features.append(flag)
        self.count += 1
        
        #Feature 2
    def __special_char(self):
        flag = 0
        
        if self.url.find('@') >= 0 or self.url.find('-'):
            flag = 1
            
        self.extracted_features.append(flag)
        self.count += 1
        
        #Feature 3
    def __url_len(self):
        flag = 0
        
        if len(self.url) >= 74:
            flag = 1
            
        self.extracted_features.append(flag)
        self.count += 1 
        
        #Feature 4
    def __susp_word(self):
        susp_wrds = ["security","signin","login","bank","account","update","include","webs","online","Secur","Verif","Com-","Support","Service","Auth","Confirm","Account"]
        flag = 0
        
        for word in susp_wrds:
            if word in self.url:
                flag = 1
                break
                
        self.extracted_features.append(flag)
        self.count += 1
        
        #Feature 5
    def __tld_count(self):
        susp_wrds = ['.com','.org','.edu','.biz','.gov','.net']
        flag = 0
        
        for word in susp_wrds:
            if self.url.count(word) > 1:
                flag = 1
                break
                
        self.extracted_features.append(flag)
        self.count += 1
    
        #Feature 6
    def __http_count(self):
        flag = 0
        
        if self.url.count('http') > 1:
            flag = 1
            
        self.extracted_features.append(flag)
        self.count += 1
        
        #Feature 7
    def __brand_name(self):
        flag = 0
        susp_wrds = ["Facebook","Chevrolet","Apple","Google","Microsoft","Amazon","PayPal","Whatsapp","Dropbox","Paytm","americanexpress","Yahoo","AOL","USAA"]
        
        for word in susp_wrds:
            if self.url.find('word') > 25:
                flag = 1
                break
                
        self.extracted_features.append(flag)
        self.count += 1
            
        #Feature 8
    def __data_uri(self):
        flag = 0
        
        if self.url.find("data:"):
            flag = 1
            
        self.extracted_features.append(flag)
        self.count += 1
        
        #Feature 9
    def __netfeature(self):
        try:
            result = requests.get(self.url)
            src = result.content
            soup = BeautifulSoup(src,'lxml')
            form = soup.find_all('form')
            
            flag = 0
            
            for a in form:
                
                php = a.attrs['action']
                
                if php.find('.php') > -1 or php.find('#') > -1 or php.find('void(0)') > -1:
                    flag = 1
                    break
                    
            self.extracted_features.append(flag)
            self.count += 1
            
        #Feature 10
            flag = 0
            html = soup.prettify()
            extractor = URLExtract()
            
            links = extractor.find_urls(html)
            no = len(links)
            
            if no == 0:
                flag = 1
                
            self.extracted_features.append(flag)
            self.count += 1
            
        #Feature 11
            flag, fcount , empty_url_count, err_count, redirect_count = 0, 0, 0, 0, 0
            
            mdomain = tldextract.extract(self.url).domain
            
            for link in links:
                
                if link == '#' or link == '#content' or link == 'JavaScript::void(0)' or link == '#skip':
                    empty_url_count += 1
                    
                domain = tldextract.extract(link).domain
                if domain != mdomain:
                    fcount += 1
                
                try:
                    link = link.lower()
                    if 'http' not in link:
                        link = 'http://' + link
                        
                    r = requests.get(link).status_code
                    
                    if r == 404 or r == 403:
                        err_count += 1
                        
                    elif r == 301 or r == 302:
                        redirect_count += 1
                    
                except:
                    continue
                    
            if no > 0 and (fcount/no) > 0.5:
                flag = 1
                
            self.extracted_features.append(flag)
            self.count += 1
            
        #Feature 12
            flag = 0
            
            if no > 0 and (empty_url_count/no) > 0.34:
                flag = 1
                
            self.extracted_features.append(flag)
            self.count += 1
            
        #Feature 13
            flag = 0
            tag = soup.find_all('link')
            
            if len(tag) == 1:
                flag = 1
                
            self.extracted_features.append(flag)
            self.count += 1
            
        #Feature 14
            flag = 0
            
            if no > 0 and (err_count/no) > 0.3:
                flag = 1
                
            self.extracted_features.append(flag)
            self.count += 1
            
        #Feature 15
            flag = 0
            
            if no > 0 and (redirect_count/no) > 0.3:
                flag = 1
                
            self.extracted_features.append(flag)
            
        except:
            
            for i in range(15 - self.count):
                self.extracted_features.append(-1)
                
    def Extract(self):
        self.__url_features()
        self.__special_char()
        self.__url_len()
        self.__susp_word()
        self.__tld_count()
        self.__http_count()
        self.__brand_name()
        self.__data_uri()
        self.__netfeature()

        print(self.extracted_features)
        
        return self.extracted_features
        
            