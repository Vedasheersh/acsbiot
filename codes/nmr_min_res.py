inp=open('mtLBS_protein_stability_after_mt.txt','r')
inpr=inp.readlines()
datafile=open('nmr_uniprot_pdb_resolution.dat','r')
dat=datafile.readlines()
mini=open('nmr_specsheet.dat','w')
err=open('xray_nmr_failed_cases.dat','w')

uniprot=[]
LBS=[] #ligand binding site
mutation=[] #residue mutation
score=[]

for i in range(len(inpr)):
	if int(i)>0:
		line=str(inpr[i]).strip()
		pdb=[]
		res=[]
		text=''
		for j in dat:
			j=j.strip()
			if j.startswith(line.split('_')[0]):
				pdb.append(str(j.split(' ')[1]))
				#res.append(float(j.split(' ')[2]))
		try:
			text=str(line)+' '+str(pdb[0])
			mini.write(str(text)+'\n')
		except ValueError:
			print (line)
			err.write(str(line)+'\n')
