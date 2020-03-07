from random import randint
from concurrent.futures import ThreadPoolExecutor as pool

import random
import os
import subprocess
import re
import requests
import json
import time




class Prox:
    
    def __init__(self):  	
    
        self.alive=[]
        self.unfiltered=[]
        self.get_proxy('https://free-proxy-list.net')
        self.get_proxy('https://www.us-proxy.org/')
        self.get_proxy('https://www.sslproxies.org/')
        self.get_proxy('http://spys.me/proxy.txt')
       
 
        self.unfiltered=list(set(self.unfiltered))
        print('Total valid proxies>>>')
        print(len(self.unfiltered))
        time.sleep(3)
        


    def get_proxy(self,url):
        pl=[]
        try:  
            res=requests.get(url) 
            html=res.content.decode()
            try:
            	pl=re.findall(r'<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>',html)
            	if not len(pl):
            		print('now collecting>>>')
            		time.sleep(1)
            		pl=re.findall(r'(\d+\.\d+\.\d+\.\d+):(\d+)',html)
            	try:
            		pl=[x[0]+':'+x[1] for x in pl]
            	except:
            		print('no proxy found')
            		
            	self.unfiltered += pl
            	print(pl)
            except:
            	print('line 40')
            
            
            print(len(self.unfiltered))
            	
            
        except Exception as e:
            print('ERROR AT GET PROXY')
            print(str(e))
    
    def collect(self):
        with pool(max_workers=1000) as exc:
            exc.map(self.check_proxy,self.unfiltered)
        print(len(set(self.alive)))
    	
    def check_proxy(self,x):
        
        for _ in range(3):
            try:
                
                #print('TRYING PROXY: '+x)
                
                proxies= {
                        'http':'http://'+ x,
                        'https':'https://'+ x,
                        }
                r = requests.get('https://www.google.com/humans.txt',
                                 timeout=3,
                                 proxies = proxies
                                 )
                
                if r.status_code == 200:
                    print(x)
                    self.alive.append(x)
                    return 
            
            except:
                pass
        print('dropping '+x)          
                
                #print(f'TRYING ANOTHER PROXY....PROXY NO.{i+1}')
        
    
if __name__=='__main__':
    r=Prox()
    r.collect()
    with open('fresh_proxy.txt','a') as f:
    	for i in r.alive:
    		f.write(i+'\n')