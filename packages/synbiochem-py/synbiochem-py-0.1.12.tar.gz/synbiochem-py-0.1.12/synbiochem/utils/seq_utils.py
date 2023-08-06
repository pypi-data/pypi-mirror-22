'''
synbiochem (c) University of Manchester 2015

synbiochem is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=no-member
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
from subprocess import call, Popen
import collections
import itertools
import operator
import os
import random
import tempfile
import urllib
import urllib2

from Bio.Blast import NCBIXML
from Bio.Data import CodonTable, IUPACData
from Bio.Seq import Seq
from Bio.SeqUtils.MeltingTemp import Tm_NN
from requests.exceptions import ConnectionError
from synbiochem.biochem4j import taxonomy
import numpy

import regex as re


NUCLEOTIDES = ['A', 'C', 'G', 'T']

AA_CODES = {'Ala': 'A',
            'Cys': 'C',
            'Asp': 'D',
            'Glu': 'E',
            'Phe': 'F',
            'Gly': 'G',
            'His': 'H',
            'Ile': 'I',
            'Lys': 'K',
            'Leu': 'L',
            'Met': 'M',
            'Asn': 'N',
            'Pro': 'P',
            'Gln': 'Q',
            'Arg': 'R',
            'Ser': 'S',
            'Thr': 'T',
            'Val': 'V',
            'Trp': 'W',
            'Tyr': 'Y',
            'End': '*'}

CODONS = {'A': [['G', 'C', 'ACGT']],
          'C': [['T', 'G', 'CT']],
          'D': [['G', 'A', 'CT']],
          'E': [['G', 'A', 'AG']],
          'F': [['T', 'T', 'CT']],
          'G': [['G', 'G', 'ACGT']],
          'H': [['C', 'A', 'CT']],
          'I': [['A', 'T', 'ACT']],
          'K': [['A', 'A', 'AG']],
          'L': [['C', 'T', 'ACGT'], ['T', 'T', 'AG']],
          'M': [['A', 'T', 'G']],
          'N': [['A', 'A', 'CT']],
          'P': [['C', 'C', 'ACGT']],
          'Q': [['C', 'A', 'AG']],
          'R': [['C', 'G', 'ACGT'], ['A', 'G', 'AG']],
          'S': [['T', 'C', 'ACGT'], ['A', 'G', 'CT']],
          'T': [['A', 'C', 'ACGT']],
          'V': [['G', 'T', 'ACGT']],
          'W': [['T', 'G', 'G']],
          'Y': [['T', 'A', 'CT']],
          'Stop': [['T', 'A', 'AG'], ['T', 'G', 'A']]}

NUCL_CODES = {
    'A': 'A',
    'C': 'C',
    'G': 'G',
    'T': 'T',
    'AG': 'R',
    'CT': 'Y',
    'CG': 'S',
    'AT': 'W',
    'GT': 'K',
    'AC': 'M',
    'CGT': 'B',
    'AGT': 'D',
    'ACT': 'H',
    'ACG': 'V',
    'ACGT': 'N',
}

INV_NUCL_CODES = {val: key for key, val in NUCL_CODES.items()}

# KD Hydrophobicity, EIIP, Helix, Sheet, Turn
AA_PROPS = {
    'A': [1.8, -0.0667, 32.9, -23.6, -41.6],
    'R': [-4.5, 0.2674, 0, -6.2, -5.1],
    'N': [-3.5, -0.2589, -24.8, -41.6, 44.5],
    'D': [-3.5, 0.4408, 5.8, -41.6, 37.8],
    'C': [2.5, 0.1933, -5.1, 6.8, 17.4],
    'Q': [-3.5, 0.1545, 11.3, 0, -2],
    'E': [-3.5, -0.2463, 36.5, -67.3, -30.1],
    'G': [-0.4, -0.2509, -46.2, -13.9, 44.5],
    'H': [-3.2, -0.1414, 11.3, -18.6, -5.1],
    'I': [4.5, -0.2794, -1, 45.1, -75.5],
    'L': [3.8, -0.2794, 26.2, 15.7, -52.8],
    'K': [-3.9, -0.0679, 19.1, -31.5, 1],
    'M': [1.9, 0.1899, 27.8, 1, -51.1],
    'F': [2.8, 0.26, 10.4, 20.7, -51.1],
    'P': [-1.6, -0.1665, -59.8, -47.8, 41.9],
    'S': [-0.8, 0.1933, -32.9, -6.2, 35.8],
    'T': [-0.7, 0.2572, -24.8, 28.5, -4.1],
    'W': [-0.9, 0.0331, 3, 21.5, -4.1],
    'Y': [-1.3, 0.0148, -31.5, 27, 13.1],
    'V': [4.2, -0.2469, -3, 49.5, -69.3]
}

NUM_AA_PROPS = len(AA_PROPS['A'])

NA = 'NA'
K = 'K'
TRIS = 'TRIS'
MG = 'MG'
DNTP = 'DNTP'

START_CODON_PATT = '[ACGT]TG'


def get_aa_props(all_sequences, scale=(0.1, 0.9)):
    '''Returns input data for machine-learning problems.'''
    scaled = __scale(scale)
    mean_value = numpy.mean([x for sublist in scaled.values()
                             for x in sublist])
    return [list(itertools.chain.from_iterable([scaled[am_acid]
                                                if am_acid in scaled
                                                else [mean_value] *
                                                len(scaled['A'])
                                                for am_acid in sequences]))
            for sequences in all_sequences]


def __scale(scale):
    '''Scale amino acid properties.'''
    scaled = collections.defaultdict(list)

    for i in range(NUM_AA_PROPS):
        props = {key: value[i] for key, value in AA_PROPS.iteritems()}
        min_val, max_val = min(props.values()), max(props.values())

        for key, value in props.iteritems():
            scaled[key].append(scale[0] + (scale[1] - scale[0]) *
                               (value - min_val) / (max_val - min_val))

    return scaled

__DEFAULT_REAG_CONC = {NA: 0.05, K: 0, TRIS: 0, MG: 0.01, DNTP: 0}


def get_codon_usage_organisms(expand=False, verbose=False):
    '''Gets name to taxonomy id dictionary of available codon usage tables.'''
    destination = os.path.join(os.path.expanduser('~'), 'codon')
    filename = 'expand.txt' if expand else 'normal.txt'
    filepath = os.path.join(destination, filename)

    if not os.path.exists(filepath):
        # Download:
        if not os.path.exists(destination):
            os.makedirs(destination)

        url = 'ftp://ftp.kazusa.or.jp/pub/codon/current/species.table'
        tmp = tempfile.NamedTemporaryFile(delete=False)
        urllib.urlretrieve(url, tmp.name)

        # Read:
        codon_orgs = _read_codon_usage_orgs_file(tmp.name)

        # Expand:
        if expand:
            _expand_codon_usage_orgs(codon_orgs, verbose)

        # Save:
        _write_codon_usage_orgs_file(codon_orgs, filepath)

        return codon_orgs
    else:
        return _read_codon_usage_orgs_file(filepath)


class CodonOptimiser(object):
    '''Class to support codon optimisation.'''

    def __init__(self, taxonomy_id):
        self.__taxonomy_id = taxonomy_id
        self.__aa_to_codon_prob = self.__get_codon_usage()
        self.__codon_prob = {item[0]: item[1]
                             for lst in self.__aa_to_codon_prob.values()
                             for item in lst}

        self.__codon_to_w = {}

        for key in self.__aa_to_codon_prob:
            aa_dict = dict([(a, b / self.__aa_to_codon_prob[key][0][1])
                            for a, b in self.__aa_to_codon_prob[key]])
            self.__codon_to_w.update(aa_dict)

    def get_codon_prob(self, codon):
        '''Gets the codon probability.'''
        return self.__codon_prob[codon]

    def optimise(self, protein_seqs, max_repeat_nuc=float('inf')):
        '''Codon optimises the supplied protein sequences.'''
        optimised_seqs = []
        max_attempts = 1000
        attempts = 0

        for protein_seq in protein_seqs:
            while True:
                attempts += 1

                if attempts > max_attempts:
                    raise ValueError('Unable to optimise sequence. ' +
                                     'Greater than ' + str(max_repeat_nuc) +
                                     ' repeating nucleotides.')

                optimised_seq = self.get_codon_optim_seq(protein_seq)

                if is_valid(optimised_seq, max_repeat_nuc):
                    optimised_seqs.append(optimised_seq)
                    break

        return optimised_seqs

    def get_codon_optim_seq(self, protein_seq, excl_codons=None,
                            max_repeat_nuc=float('inf'), invalid_seqs=None,
                            max_attempts=100, tolerant=False):
        '''Returns a codon optimised DNA sequence.'''
        inv_patt = _get_inv_patt(max_repeat_nuc, invalid_seqs)

        if not len(inv_patt):
            return ''.join([self.get_random_codon(aa)
                            for aa in protein_seq])
        else:
            attempts = 0
            seq = ''
            i = 0
            blockage_i = -1
            inv_patterns = 0

            while attempts < max_attempts:
                amino_acid = protein_seq[i]
                new_seq = seq + self.get_random_codon(amino_acid, excl_codons)

                invalids = [invalid.start()
                            for invalid in re.finditer(inv_patt,
                                                       new_seq,
                                                       overlapped=True)]
                if len(invalids) == inv_patterns or \
                        (attempts == max_attempts - 1 and tolerant):

                    if i == blockage_i:
                        if attempts == max_attempts - 1:
                            inv_patterns = inv_patterns + 1

                        attempts = 0

                    seq = new_seq

                    if i == len(protein_seq) - 1:
                        return seq

                    i += 1
                else:
                    blockage_i = max(i, blockage_i)
                    i = max(0, (invalids[-1] / 3) - 1)
                    seq = seq[:i * 3]
                    attempts += 1

            raise ValueError('Unable to generate codon-optimised sequence.')

    def get_cai(self, dna_seq):
        '''Gets the CAI for a given DNA sequence.'''
        cai = 0

        for i in range(0, len(dna_seq), 3):
            cai += self.__codon_to_w[dna_seq[i:i + 3]]

        return cai / (len(dna_seq) / 3)

    def mutate(self, protein_seq, dna_seq, mutation_rate):
        '''Mutate a protein-encoding DNA sequence according to a
        supplied mutation rate.'''
        return ''.join([self.get_random_codon(amino_acid)
                        if random.random() < mutation_rate
                        else dna_seq[3 * i:3 * (i + 1)]
                        for i, amino_acid in enumerate(protein_seq)])

    def get_all_rev_trans(self, aa_seq):
        '''Returns all reverse translations of amino acid sequence.'''
        codons = [self.get_all_codons(aa) for aa in aa_seq]
        return [''.join(t) for t in list(itertools.product(*codons))]

    def get_all_codons(self, amino_acid):
        '''Returns all codons for a given amino acid.'''
        return [t[0] for t in self.__aa_to_codon_prob[amino_acid]]

    def get_random_codon(self, amino_acid, excl_codons=None):
        '''Returns a random codon for a given amino acid,
        based on codon probability from the codon usage table.'''
        if excl_codons is None:
            excl_codons = []

        codon_usage = [codon_usage
                       for codon_usage in self.__aa_to_codon_prob[amino_acid]
                       if codon_usage[0] not in excl_codons]

        if len(codon_usage) == 0:
            raise ValueError('No codons available for ' + amino_acid +
                             ' after excluding ' + str(excl_codons))

        while True:
            rand = random.random()
            cumulative_prob = 0

            for codon, prob in iter(reversed(codon_usage)):
                cumulative_prob += prob

                if cumulative_prob > rand:
                    return codon

    def __get_codon_usage(self):
        '''Gets the codon usage table for a given taxonomy id.'''
        aa_to_codon_prob = {aa_code: {} for aa_code in AA_CODES.values()}

        url = 'http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=' \
            + self.__taxonomy_id + '&aa=1&style=GCG'

        in_codons = False

        for line in urllib2.urlopen(url):
            if line == '<PRE>\n':
                in_codons = True
            elif line == '</PRE>\n':
                break
            elif in_codons:
                values = re.split('\\s+', line)

                if values[0] in AA_CODES:
                    codon_prob = aa_to_codon_prob[AA_CODES[values[0]]]
                    codon_prob[values[1]] = float(values[3])

        aa_to_codon_prob.update((x, _scale(y))
                                for x, y in aa_to_codon_prob.items())

        return aa_to_codon_prob


def get_minimum_free_energy(sequences):
    '''Returns minimum free energy of supplied DNA / RNA sequences.'''
    with open(tempfile.NamedTemporaryFile(), 'w') as input_file, \
            open(tempfile.NamedTemporaryFile(), 'w') as output_file:

        for i, sequence in enumerate(sequences):
            input_file.write('>Seq' + str(i) + '\n' + sequence + '\n')
            input_file.flush()

        input_file.close()

        proc = Popen('RNAfold',
                     stdin=open(input_file.name),
                     stdout=output_file)

        proc.wait()

        _cleanup(os.getcwd(), 'Seq\\d+_ss.ps')

        mfes = []
        pattern = re.compile(r'[+-]?\d+\.\d+')

        with open(output_file.name) as out_file:
            for line in out_file.readlines():
                src = pattern.search(line)

                if src:
                    mfes.append(float(src.group()))

        return mfes


def get_random_dna(length, max_repeat_nuc=float('inf'), invalid_seqs=None):
    '''Returns a random sequence of DNA of the supplied length,
    while adhering to a maximum number of repeating nucleotides.'''
    max_attempts = 1000
    attempts = 0

    inv_patt = _get_inv_patt(max_repeat_nuc, invalid_seqs)

    while True:
        attempts += 1

        if attempts > max_attempts:
            raise ValueError('Unable to optimise sequence.')

        random_dna = _get_random_dna(length)

        valid = True

        if len(inv_patt) and \
                len(re.findall(inv_patt, random_dna,  overlapped=True)) > 0:
            valid = False

        if valid:
            return random_dna

    return None


def _get_inv_patt(max_repeat_nuc=float('inf'), invalid_seqs=None):
    '''Gets invalid patterns.'''
    if invalid_seqs is None:
        invalid_seqs = []

    if max_repeat_nuc != float('inf'):
        invalid_repeat_nuc = [x * (max_repeat_nuc + 1) for x in NUCLEOTIDES]
    else:
        invalid_repeat_nuc = []

    return '|'.join(invalid_seqs + invalid_repeat_nuc)


def get_random_aa(length, insertions=False):
    '''Returns a random amino acid sequence of the supplied length.'''
    dictionary = list(AA_PROPS.keys()) + (['.'] if insertions else [])
    return ''.join(random.choice(dictionary) for _ in range(length))


def mutate_seq(seq, mutations=1, alphabet=None):
    '''Mutates sequence.'''
    if alphabet is None:
        alphabet = NUCLEOTIDES

    seq_new = seq

    for _ in range(mutations):
        move = random.random()
        pos = int(random.random() * len(seq))
        base = random.choice(alphabet)

        # Insert:
        if move < 0.1:
            seq_new = seq_new[1:pos + 1] + base + seq_new[pos + 1:]

        # Delete:
        elif move < 0.2:
            seq_new = base + seq_new[:pos] + seq_new[pos + 1:]

        # Replace:
        else:
            seq_new = seq_new[:pos] + base + seq_new[pos + 1:]

    return seq_new


def get_melting_temp(dna1, dna2=None, reag_concs=None, strict=True):
    '''Calculates melting temperarure of DNA sequence against its
    complement, or against second DNA sequence using Nearest-Neighbour
    method.'''
    assert len(dna1) > 1

    reagent_concs = __DEFAULT_REAG_CONC

    if reag_concs is not None:
        reagent_concs.update(reag_concs)

    reagent_conc = {k: v * 1000 for k, v in reagent_concs.iteritems()}
    dnac1 = 30

    return Tm_NN(dna1, check=True, strict=strict, c_seq=dna2, shift=0,
                 Na=reagent_conc[NA], K=reagent_conc[K],
                 Tris=reagent_conc[TRIS], Mg=reagent_conc[MG],
                 dNTPs=reagent_conc[DNTP],
                 dnac1=dnac1, dnac2=dnac1, selfcomp=dna2 is None,
                 saltcorr=7)


def get_seq_by_melt_temp(seq, target_melt_temp, forward=True,
                         terminii=None,
                         reagent_concs=None,
                         tol=0.025):
    '''Returns a subsequence close to desired melting temperature.'''
    if terminii is None:
        terminii = ['A', 'C', 'G', 'T']
    else:
        terminii = [term.upper() for term in terminii]

    best_delta_tm = float('inf')
    best_subseq = ''
    best_melt_temp = float('NaN')
    in_tol = False

    for i in range(1, len(seq)):
        subseq = seq[:(i + 1)] if forward else seq[-(i + 1):]
        melt_temp = get_melting_temp(subseq, None, reagent_concs)

        if subseq[-1 if forward else 0].upper() in terminii:
            delta_tm = abs(melt_temp - target_melt_temp)

            if delta_tm / target_melt_temp < tol:
                in_tol = True

                if delta_tm < best_delta_tm:
                    best_delta_tm = delta_tm
                    best_subseq = subseq
                    best_melt_temp = melt_temp
            elif in_tol:
                return best_subseq, best_melt_temp

    raise ValueError('Unable to get sequence of required melting temperature')


def get_rand_seq_by_melt_temp(target_melt_temp,
                              max_repeat_nuc=float('inf'),
                              invalid_seqs=None,
                              reagent_concs=None,
                              tol=0.025):
    '''Returns a random close to desired melting temperature.'''
    inv_patt = _get_inv_patt(max_repeat_nuc, invalid_seqs)
    seq = random.choice(NUCLEOTIDES)

    while True:
        seq += random.choice(NUCLEOTIDES)

        if len(re.findall(inv_patt, seq, overlapped=True)) > 0:
            seq = seq[:-random.choice(range(len(seq)))]
            continue

        melt_temp = get_melting_temp(seq, None, reagent_concs)

        delta_tm = abs(melt_temp - target_melt_temp)

        if delta_tm / target_melt_temp < tol:
            return seq, melt_temp

    raise ValueError('Unable to get sequence of required melting temperature')


def is_valid(dna_seq, max_repeat_nuc):
    '''Checks whether a DNA sequence is valid, in terms of a supplied maximum
    number of repeating nucleotides.'''
    nuc_count = 0
    prev_nuc = ''

    for nuc in dna_seq:
        if prev_nuc == nuc:
            nuc_count += 1
        else:
            prev_nuc = nuc
            nuc_count = 1

        if nuc_count > max_repeat_nuc:
            return False

    return True


def get_uniprot_values(uniprot_ids, fields, batch_size=64, verbose=False):
    '''Gets dictionary of ids to values from Uniprot.'''
    values = {}

    for i in xrange(0, len(uniprot_ids), batch_size):

        if verbose:
            print 'seq_utils: getting Uniprot values ' + str(i) + ' - ' + \
                str(min(i + batch_size, len(uniprot_ids))) + ' / ' + \
                str(len(uniprot_ids))

        batch = uniprot_ids[i:min(i + batch_size, len(uniprot_ids))]
        query = '+or+'.join(['id:' + uniprot_id for uniprot_id in batch])
        url = 'http://www.uniprot.org/uniprot/?query=' + query + \
            '&format=tab&columns=id,' + ','.join([urllib.quote(field)
                                                  for field in fields])

        _parse_uniprot_data(url, values)

    return values


def search_uniprot(name, fields, limit=128):
    '''Gets dictionary of ids to values from Uniprot.'''
    values = {}

    url = 'http://www.uniprot.org/uniprot/?query=name:' + name + \
        '&limit=' + str(limit) + \
        '&format=tab&columns=id,' + ','.join([urllib.quote(field)
                                              for field in fields])

    _parse_uniprot_data(url, values)

    return values


def count_pattern(seq, max_repeat_nuc=float('inf'), pattern_strs=None,
                  both_strands=True):
    '''Counts pattern in seq.'''
    pattern = _get_inv_patt(max_repeat_nuc, pattern_strs)

    forward = _count_pattern(seq, pattern)

    if both_strands:
        return forward + _count_pattern(get_rev_comp(seq), pattern)
    else:
        return forward


def get_hamming(str1, str2):
    '''Returns Hamming distance for two sequences, which are assumed to be of
    the same length.'''
    return sum(itertools.imap(operator.ne, str1, str2))


def get_rev_comp(seq):
    '''Returns reverse complement of sequence.'''
    seq = Seq(seq)
    return str(seq.reverse_complement())


def get_comp(seq):
    '''Returns complement of sequence.'''
    seq = Seq(seq)
    return str(seq.complement())


def do_blast(id_seqs_subjects, id_seqs_queries, program='blastn',
             dbtype='nucl', evalue=1.0, word_size=28):
    '''Performs BLAST of query sequences against subject sequences.'''

    db_filename = write_fasta(id_seqs_subjects)
    query_filename = write_fasta(id_seqs_queries)
    result_file = tempfile.NamedTemporaryFile(prefix='blast_result_',
                                              suffix='.xml',
                                              delete=False)
    call(['makeblastdb',
          '-in', db_filename,
          '-out', db_filename,
          '-dbtype', dbtype])

    call([program,
          '-query', query_filename,
          '-db', db_filename,
          '-out', result_file.name,
          '-evalue', str(evalue),
          '-word_size', str(word_size),
          '-outfmt', '5'])

    return NCBIXML.parse(open(result_file.name))


def write_fasta(id_seqs, filename=None):
    '''Writes a fasta file.'''
    if filename is None:
        temp_file = tempfile.NamedTemporaryFile(prefix='fasta_', suffix='.txt',
                                                delete=False)
        filename = temp_file.name

    with open(filename, 'w') as fle:
        for seq_id, seq in id_seqs.iteritems():
            fle.write('>' + str(seq_id) + '\n')
            fle.write(seq + '\n')

    return filename


def translate(seq, trans_table=CodonTable.unambiguous_dna_by_name["Standard"],
              min_prot_len=128):
    '''Translates supplied nucleotide sequence in all 6 reading frames.'''
    result = []

    seq = Seq(seq)

    for strand, nuc in [('+', seq), ('-', seq.reverse_complement())]:
        for frame in range(3):
            trans = \
                str(nuc[frame:-(len(nuc[frame:]) % 3)].translate(trans_table))
            trans_len = len(trans)
            aa_start = 0
            aa_end = 0

            while aa_start < trans_len:
                aa_end = trans.find("*", aa_start)
                if aa_end == -1:
                    aa_end = trans_len
                if aa_end - aa_start >= min_prot_len:
                    start = frame + aa_start * 3
                    end = frame + aa_end * 3

                    result.append((start, end, strand, frame,
                                   len(trans[aa_start:aa_end]),
                                   trans[aa_start:aa_end]))
                aa_start = aa_end + 1
    return result


def ambiguous_to_regex(seq):
    '''Converts sequence with ambiguous nucleotides to regex,
    e.g. ANT to A[ACGT]T.'''
    return ''.join([val
                    if val not in IUPACData.ambiguous_dna_values or
                    len(IUPACData.ambiguous_dna_values[val]) == 1
                    else '[' + IUPACData.ambiguous_dna_values[val] + ']'
                    for val in seq])


def apply_restriction(seq, restrict):
    '''Applies restriction site cleavage to forward and reverse strands.'''
    seq = _apply_restriction(seq, restrict)
    seq = _apply_restriction(get_rev_comp(seq), restrict)
    return get_rev_comp(seq)


def apply_mutations(seq, mutations):
    '''Applies mutations to sequence.'''
    seq = list(seq)

    for mutation in mutations:
        if mutation[0] != seq[mutation[1] - 1]:
            raise ValueError('Invalid mutation at position %d.' +
                             'Amino acid is %s but mutation is of %s.') \
                % mutation[1], seq[mutation[1] - 1], mutation[0]

        seq[mutation[1] - 1] = mutation[2]

    return ''.join(seq)


def _apply_restriction(seq, restrict):
    '''Applies restriction site cleavage to sequence.'''
    match = re.search(restrict, seq)

    if match:
        seq = match.group(0)

    return seq


def _count_pattern(strings, pattern):
    '''Counts pattern in string of list of strings.'''
    if isinstance(strings, str) or isinstance(strings, unicode):
        return len(re.findall(pattern, strings))
    elif strings is None:
        return 0
    else:
        return [count_pattern(s, pattern) for s in strings]


def _scale(codon_usage):
    '''Scale codon usage values to add to 1.'''
    codon_usage = dict([(key, value / sum(codon_usage.values()))
                        for key, value in codon_usage.items()])

    return sorted(codon_usage.items(), key=operator.itemgetter(1),
                  reverse=True)


def _get_random_dna(length):
    '''Returns a random sequence of DNA of the supplied length.'''
    return ''.join(random.choice(['A', 'C', 'G', 'T']) for _ in range(length))


def _cleanup(drctry, pattern):
    '''Deletes files in directory matching pattern.'''
    for filename in os.listdir(drctry):
        if re.search(pattern, filename):
            os.remove(os.path.join(drctry, filename))


def _parse_uniprot_data(url, values):
    '''Parses Uniprot data.'''
    headers = None

    try:
        for line in urllib2.urlopen(url):
            tokens = line.strip().split('\t')

            if headers is None:
                headers = tokens
            else:
                resp = dict(zip(headers, tokens))
                entry = resp.pop('Entry')

                if 'Protein names' in resp:
                    regexp = re.compile(r'(?<=\()[^)]*(?=\))|^[^(][^()]*')
                    names = regexp.findall(resp.pop('Protein names'))
                    resp['Protein names'] = [nme.strip() for nme in names]

                values.update({entry: resp})
    except urllib2.HTTPError, err:
        print err


def _read_codon_usage_orgs_file(filename):
    '''Reads Codon Usage Database table of species file.'''
    codon_orgs = {}

    with open(filename, 'r') as textfile:
        next(textfile)

        for line in textfile:
            tokens = line.strip().split('\t')
            codon_orgs[tokens[0]] = tokens[1]

    return codon_orgs


def _expand_codon_usage_orgs(codon_orgs, verbose, max_errors=16):
    '''Expand Codon Usage Db table of species with children and synonyms.'''
    for tax_id in codon_orgs.values():

        if verbose:
            print 'Expanding codon usage for NCBI Taxonomy id: ' + tax_id

        errors = 0
        success = False

        while not success:
            try:
                for name in taxonomy.get_synonyms_by_id(tax_id):
                    _add_codon_usage_org(codon_orgs, name, tax_id)

                for child in taxonomy.get_children_by_id(tax_id):
                    _add_codon_usage_org(codon_orgs, child['name'], tax_id)

                    for name in child['names']:
                        _add_codon_usage_org(codon_orgs, name, tax_id)

                success = True

            except ConnectionError, err:
                errors += 1

                if errors == max_errors:
                    raise err


def _add_codon_usage_org(codon_orgs, name, tax_id):
    '''Adds name to codon_orgs.'''
    if name not in codon_orgs:
        codon_orgs[name] = tax_id


def _write_codon_usage_orgs_file(codon_orgs, filepath):
    '''Writes Codon Usage Database table of species file.'''
    with open(filepath, 'w+') as fle:
        fle.write('Name\tId\n')

        for name, tax_id in codon_orgs.iteritems():
            fle.write(name + '\t' + tax_id + '\n')


def main():
    '''main method.'''
    get_codon_usage_organisms(expand=True)

if __name__ == '__main__':
    main()
