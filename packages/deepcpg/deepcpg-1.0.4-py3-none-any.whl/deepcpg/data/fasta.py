import os
from glob import glob
import gzip as gz

from ..utils import to_list


class FastaSeq(object):

    def __init__(self, head, seq):
        self.head = head
        self.seq = seq


def parse_lines(lines):
    seqs = []
    seq = None
    start = None
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0]
    for i in range(len(lines)):
        if lines[i][0] == '>':
            if start is not None:
                head = lines[start]
                seq = ''.join(lines[start + 1: i])
                seqs.append(FastaSeq(head, seq))
            start = i
    if start is not None:
        head = lines[start]
        seq = ''.join(lines[start + 1:])
        seqs.append(FastaSeq(head, seq))
    return seqs


def read_file(filename, gzip=None):
    if gzip is None:
        gzip = filename.endswith('.gz')
    if gzip:
        lines = gz.open(filename, 'r').read().decode()
    else:
        lines = open(filename, 'r').read()
    lines = lines.splitlines()
    return parse_lines(lines)


def select_file_by_chromo(filenames, chromo):
    filenames = to_list(filenames)
    if len(filenames) == 1 and os.path.isdir(filenames[0]):
        filenames = glob(os.path.join(filenames[0],
                                      '*.dna.chromosome.%s.fa*' % chromo))

    for filename in filenames:
        if filename.find('chromosome.%s.fa' % chromo) >= 0:
            return filename


def read_chromo(filenames, chromo):
    filename = select_file_by_chromo(filenames, chromo)
    if not filename:
        raise ValueError('DNA file for chromosome "%s" not found!' % chromo)

    fasta_seqs = read_file(filename)
    if len(fasta_seqs) != 1:
        raise ValueError('Single sequence expected in file "%s"!' % filename)
    return fasta_seqs[0].seq
