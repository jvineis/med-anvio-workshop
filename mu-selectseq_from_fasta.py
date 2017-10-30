from Bio import SeqIO
from Bio.Seq import Seq
import sys
import argparse

parser = argparse.ArgumentParser(description='''Read in a pair of fastq files and pull out sequence\
 pairs if they contain defline ids provided in a given file''')
parser.add_argument('--x', help = 'reads in fasta format')
parser.add_argument('--outfile', help = 'Your name for the output file containing your target seqs')
parser.add_argument('--infile', help = 'A txt file with a single column of defline ids')
args = parser.parse_args()

headers = []
infile = open(args.infile, 'rU')
for line in infile:
    x =line.strip()
    headers.append(x)

reads = open(args.x, 'rU')
print("Hi awesome microbial scientist, Im searching for your %d sequecnces and writing them to a fasta file [ %s]. Its gonna be awesome :)" %(len(headers), str(args.outfile)))


def select_fastq(fastafile, output):
    outfile = open(output, 'w')
    for seq_record in SeqIO.parse(fastafile, "fasta"):
        if seq_record.id in headers:
            outfile.write(seq_record.format("fasta"))
            #outfile.write("@"+str(seq_record.id) +'\n'+str(seq_record.seq)+'\n'+"+"+'\n'+str(seq_record.qual)+'\n')
    return outfile

select_fastq(reads,args.outfile)
