inp=open('mtLBS_protein_stability_after_mt.txt','r')
inpr=inp.readlines()

uniprot=[]
LBS=[] #ligand binding site
mutation=[] #residue mutation
score=[]

for i in range(len(inpr)):
	if int(i)>0:
		line=str(inpr[i]).strip()
		uniprot.append(line.split('_')[0])
		LBS.append(line.split('_')[1])
		temp=line.split('_')[2]
		mutation=temp.split(' ')[0]
		score.append(temp.split('\t')[1])


import os, sys
#import wget
#import urllib2
import requests
import re

out=open('Uniprot_PDB_resolution.dat','w')

for i in uniprot:
	i=i.strip()
	flag=0
	url = "https://www.uniprot.org/uniprot/"+str(i)+"#structure"
	page_=requests.get(url)
	response=page_.text
	pdb=re.findall(r'class="pdb">\w\w\w\w+</a></td><td>X-ray</td><td>\d+\.\d+',response)
	
	for j in pdb:
		j=str(j)
		j=j.strip()
		temp1=j.split('class="pdb">')[1]
		id=temp1[:4]
		resolution=temp1[-4:]
		print(i, id, resolution)
		out.write(str(i)+' '+str(id)+' '+str(resolution)+'\n')
