# make sure you can pyrosetta and then run this

convertAA = {

"ALA":"A", "A":"ALA", "CYS":"C", "C":"CYS", "ASP":"D", "D":"ASP", \
       "GLU":"E", "E":"GLU", "PHE":"F", "F":"PHE", "GLY":"G", "G":"GLY", \
"HIS":"H", "HSD":"H", "H":"HIS", "ILE":"I", "I":"ILE", "LYS":"K", "K":"LYS", \
       "LEU":"L", "L":"LEU", "MET":"M", "M":"MET", "ASN":"N", "N":"ASN", \
       "PRO":"P", "P":"PRO", "GLN":"Q", "Q":"GLN", "ARG":"R", "R":"ARG", \
       "SER":"S", "S":"SER", "THR":"T", "T":"THR", "VAL":"V", "V":"VAL", \
       "TRP":"W", "W":"TRP", "TYR":"Y", "Y":"TYR"
}

from pyrosetta import *

XRAY_FILE = '../data/specsheet_xray.dat'

DATA_DIR = '../data/pdbs'
NEWDATA_DIR = '../data/mutpdbs/xray_all'

init(extra_options = "-mute all -ignore_zero_occupancy false")

flog = open('xray_mutate.log','w')
success = 0
fail = 0

xf = open(XRAY_FILE)
for line in xf:
    head, score, pdbid, resolution = line.split()
    uid, lbs, mut = head.split('_')
    try:
        pose = pose_from_pdb('../data/pdbs/{}.pdb'.format(pdbid))
    except RuntimeError:
        flog.write('{}\tFAILED\tPDB_not_found\n'.format(head))
        fail+=1
        continue

    #check if mutation exists in chain A

    native = mut[0]
    resn = int(mut[1:-1])
    target = mut[-1]
    info = pose.pdb_info()
    resn_pose = info.pdb2pose('A',resn)
    if resn_pose==0:
        flog.write('{}\tFAILED\tResnum_not_found\n'.format(head))
        fail+=1
    else:
        try:
            aa_pose = convertAA[str(pose.aa(resn_pose)).split('_')[-1].upper()]
            if native!=aa_pose:
                flog.write('{}\tFAILED\tRes_not_native\n'.format(head))
                fail+=1
            else:
                toolbox.mutate_residue(pose,resn_pose,target)
                newpdb = '{}_{}.pdb'.format(pdbid,mut)
                flog.write('{}\tSUCCESS\t{}\n'.format(head,mut))
                pose.dump_pdb('{}/{}'.format(NEWDATA_DIR,newpdb))
                success+=1
        except:
            flog.write('{}\tFAILED\tSomething_wrong\n'.format(head))
print('No. of success = {}'.format(success))
print('No. of failures = {}'.format(fail))

flog.close()
xf.close()
