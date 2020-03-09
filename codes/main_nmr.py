##P32780_Q17_R16C -0.78186216

inp=open('failed_cases.dat','r')
inpr=inp.readlines()
import os,sys
#import wget
#import urllib2
import requests
import re
out=open('nmr_uniprot_pdb_resolution.dat','w')

for i in inpr:
	i=i.strip()
	unip=i.split('_')[0]
	url = "https://www.uniprot.org/uniprot/"+str(unip)+"#structure"
	page_=requests.get(url)
	response=page_.text
	pdb=re.findall(r'class="pdb">\w\w\w\w+</a></td><td>NMR',response)
	
	for j in pdb:
		j=str(j)
		j=j.strip()
		temp1=j.split('class="pdb">')[1]
		id=temp1[:4]
		print(unip, id)
		out.write(str(unip)+' '+str(id)+'\n')
