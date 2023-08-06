#!/usr/bin/env python
"""Record file for immunoglobulin data type.

This file is adapted from Change-O modules.
See changeo.DbCore for the original version.
Reference: http://changeo.readthedocs.io/en/latest/

Author: Federico Tomasi
Copyright (c) 2016, Federico Tomasi.
Licensed under the FreeBSD license (see LICENSE.txt).
"""
import re
import sys

from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from sklearn.base import BaseEstimator

from icing.utils.extra import junction_re

# Regular expression globals
allele_regex = re.compile(r'((IG[HLK]|TR[ABGD])([VDJ][A-Z0-9]+[-/\w]*[-\*][\.\w]+))')
gene_regex = re.compile(r'((IG[HLK]|TR[ABGD])([VDJ][A-Z0-9]+[-/\w]*))')
family_regex = re.compile(r'((IG[HLK]|TR[ABGD])([VDJ][A-Z0-9]+))')

v_allele_regex = re.compile(r'((IG[HLK]|TR[ABGD])V[A-Z0-9]+[-/\w]*[-\*][\.\w]+)')
d_allele_regex = re.compile(r'((IG[HLK]|TR[ABGD])D[A-Z0-9]+[-/\w]*[-\*][\.\w]+)')
j_allele_regex = re.compile(r'((IG[HLK]|TR[ABGD])J[A-Z0-9]+[-/\w]*[-\*][\.\w]+)')


# TODO:  might be better to just use the lower case column name as the member
# variable name. can use getattr and setattr.
class IgRecord(BaseEstimator):
    """A class defining a V(D)J germline sequence alignment."""

    # Mapping of member variables to column names
    _key_map = {'id': 'SEQUENCE_ID',
                'v_call': 'V_CALL',
                'v_call_geno': 'V_CALL_GENOTYPED',
                'd_call': 'D_CALL',
                'j_call': 'J_CALL',
                'seq_input': 'SEQUENCE_INPUT',
                'seq_vdj': 'SEQUENCE_VDJ',
                'seq_imgt': 'SEQUENCE_IMGT',
                'junction': 'JUNCTION',
                'junctionaa': 'JUNCTIONAA',
                'functional': 'FUNCTIONAL',
                'in_frame': 'IN_FRAME',
                'stop': 'STOP',
                'mutated_invariant': 'MUTATED_INVARIANT',
                'indels': 'INDELS',
                'v_seq_start': 'V_SEQ_START',
                'v_seq_length': 'V_SEQ_LENGTH',
                'v_germ_start': 'V_GERM_START',
                'v_germ_length': 'V_GERM_LENGTH',
                'n1_length': 'N1_LENGTH',
                'd_seq_start': 'D_SEQ_START',
                'd_seq_length': 'D_SEQ_LENGTH',
                'd_germ_start': 'D_GERM_START',
                'd_germ_length': 'D_GERM_LENGTH',
                'n2_length': 'N2_LENGTH',
                'j_seq_start': 'J_SEQ_START',
                'j_seq_length': 'J_SEQ_LENGTH',
                'j_germ_start': 'J_GERM_START',
                'j_germ_length': 'J_GERM_LENGTH',
                'junction_length': 'JUNCTION_LENGTH',
                'v_score': 'V_SCORE',
                'v_identity': 'V_IDENTITY',
                'v_evalue': 'V_EVALUE',
                'j_score': 'J_SCORE',
                'j_identity': 'J_IDENTITY',
                'j_evalue': 'J_EVALUE',
                'mut': 'MUT',
                'subset': 'SUBSET'}

    # Mapping of column names to member variables
    _field_map = {v: k for k, v in _key_map.iteritems()}

    # Mapping of member variables to parsing functions
    _parse_map = {'id': '_identity',
                  'v_call': '_identity',
                  'v_call_geno': '_identity',
                  'd_call': '_identity',
                  'j_call': '_identity',
                  'seq_input': '_sequence',
                  'seq_vdj': '_sequence',
                  'seq_imgt': '_sequence',
                  'junction': '_sequence',
                  'junctionaa': '_sequence',
                  'functional': '_logical',
                  'in_frame': '_logical',
                  'stop': '_logical',
                  'mutated_invariant': '_logical',
                  'indels': '_logical',
                  'v_seq_start': '_integer',
                  'v_seq_length': '_integer',
                  'v_germ_start': '_integer',
                  'v_germ_length': '_integer',
                  'n1_length': '_integer',
                  'd_seq_start': '_integer',
                  'd_seq_length': '_integer',
                  'd_germ_start': '_integer',
                  'd_germ_length': '_integer',
                  'n2_length': '_integer',
                  'j_seq_start': '_integer',
                  'j_seq_length': '_integer',
                  'j_germ_start': '_integer',
                  'j_germ_length': '_integer',
                  'junction_length': '_integer',
                  'v_score': '_float',
                  'v_identity': '_float',
                  'v_evalue': '_float',
                  'j_score': '_float',
                  'j_identity': '_float',
                  'j_evalue': '_float',
                  'mut': '_float',
                  'subset': '_identity'}

    _logical_parse = {'F': False, 'T': True, 'TRUE': True, 'FALSE': False,
                      'NA': None, 'None': None}
    _logical_deparse = {False: 'F', True: 'T', None: 'None'}

    # Private methods
    @staticmethod
    def _identity(v, deparse=False):
        return v

    @staticmethod
    def _logical(v, deparse=False):
        if not deparse:
            try:
                return IgRecord._logical_parse[v]
            except:
                return None
        else:
            try:
                return IgRecord._logical_deparse[v]
            except:
                return ''

    @staticmethod
    def _integer(v, deparse=False):
        if not deparse:
            try:
                return int(v)
            except:
                return None
        else:
            try:
                return str(v)
            except:
                return ''

    @staticmethod
    def _float(v, deparse=False):
        if not deparse:
            try:
                return float(v)
            except:
                return None
        else:
            try:
                return str(v)
            except:
                return ''

    @staticmethod
    def _sequence(v, deparse=False):
        if not deparse:
            try:
                return Seq(v, IUPAC.ambiguous_dna)
            except:
                return None
        else:
            try:
                return str(v)
            except:
                return ''

    # Initializer
    #
    # Arguments:  row = dictionary of {field:value} data
    #             genotyped = if True assign v_call from genotyped field
    # Returns:    IgRecord
    def __init__(self, row, genotyped=True):
        required_keys = ('id',)
        optional_keys = (x for x in IgRecord._parse_map if x not in required_keys)

        # Not ideal. Will place V_CALL_GENOTYPED in annotations
        if not genotyped and 'v_call_geno' in optional_keys:
            del optional_keys['v_call_geno']

        try:
            for k in required_keys:
                f = getattr(IgRecord, IgRecord._parse_map[k])
                setattr(self, k, f(row.pop(IgRecord._key_map[k])))
        except:
            raise ValueError('row must contain valid %s values'
                     % ','.join([IgRecord._key_map[k] for k in required_keys]))

        # Defined optional logical values
        for k in optional_keys:
            f = getattr(IgRecord, IgRecord._parse_map[k])
            setattr(self, k, f(row.pop(IgRecord._key_map[k], None)))

        # Add remaining elements as annotations dictionary
        self.annotations = row
        self.setV = set(self.getVGene('set') or ())
        self.setJ = set(self.getJGene('set') or ())
        self.junc = junction_re(self.junction)

    # Get a field value by column name and return it as a string
    #
    # Arguments:  field = column name
    # Returns:    value in the field as a string
    def getField(self, field):
        if field in IgRecord._field_map:
            v = getattr(self, IgRecord._field_map[field])
        elif field in self.annotations:
            v = self.annotations[field]
        else:
            return None

        if isinstance(v, str):
            return v
        else:
            return str(v)

    def getVSeq(self):
        # _seq_vdj = self.getField('SEQUENCE_VDJ')
        _seq_vdj = self.getField('SEQUENCE_IMGT')
        # _idx_v = int(self.getField('V_SEQ_LENGTH'))
        return _seq_vdj[:312]  # 312: V length without cdr3

    # Get a field value converted to a Seq object by column name
    #
    # Arguments:  field = column name
    # Returns:    value in the field as a Seq object
    def getSeqField(self, field):
        if field in IgRecord._field_map:
            v = getattr(self, IgRecord._field_map[field])
        elif field in self.annotations:
            v = self.annotations[field]
        else:
            return None

        if isinstance(v, Seq):
            return v
        elif isinstance(v, str):
            return Seq(v, IUPAC.ambiguous_dna)
        else:
            return None

    # Returns: dictionary of the namespace
    def to_dict(self):
        d = {}
        n = self.__dict__
        for k, v in n.iteritems():
            if k == 'annotations':
                d.update({i.upper(): j for i, j in n['annotations'].iteritems()})
            else:
                f = getattr(IgRecord, IgRecord._parse_map[k])
                d[IgRecord._key_map[k]] = f(v, deparse=True)
        return d

    # Methods to get multiple allele, gene and family calls
    #
    # Arguments:  calls = iterable of calls to get; one or more of ('v','d','j')
    #             actions = one of ('first','set')
    # Returns:    list of requested calls in order
    def getAlleleCalls(self, calls, action='first'):
        vdj = {'v': self.getVAllele(action),
               'd': self.getDAllele(action),
               'j': self.getJAllele(action)}
        return [vdj[k] for k in calls]

    def getGeneCalls(self, calls, action='first'):
        vdj = {'v': self.getVGene(action),
               'd': self.getDGene(action),
               'j': self.getJGene(action)}
        return [vdj[k] for k in calls]

    def getFamilyCalls(self, calls, action='first'):
        vdj = {'v': self.getVFamily(action),
               'd': self.getDFamily(action),
               'j': self.getJFamily(action)}
        return [vdj[k] for k in calls]

    # Individual allele, gene and family getter methods
    #
    # Arguments:  actions = one of ('first','set')
    # Returns:    call as a string
    def getVAllele(self, action='first'):
        # TODO: this can't distinguish empty value ("") from missing field (no column)
        x = self.v_call_geno if self.v_call_geno is not None else self.v_call
        return parseAllele(x, allele_regex, action)

    def getDAllele(self, action='first'):
        return parseAllele(self.d_call, allele_regex, action)

    def getJAllele(self, action='first'):
        return parseAllele(self.j_call, allele_regex, action)

    def getVGene(self, action='first'):
        return parseAllele(self.v_call, gene_regex, action)

    def getDGene(self, action='first'):
        return parseAllele(self.d_call, gene_regex, action)

    def getJGene(self, action='first'):
        return parseAllele(self.j_call, gene_regex, action)

    def getVFamily(self, action='first'):
        return parseAllele(self.v_call, family_regex, action)

    def getDFamily(self, action='first'):
        return parseAllele(self.d_call, family_regex, action)

    def getJFamily(self, action='first'):
        return parseAllele(self.j_call, family_regex, action)

    @property
    def features(self):
        """Get features as list of strings.

        They are organised as:
        - Vgenes (separated by '|')
        - Jgenes (separated by '|')
        - Junction
        - Junction length
        - Mutation level
        """
        return ["|".join(list(self.setV)),
                "|".join(list(self.setJ)),
                self.junc,
                str(self.junction_length),
                str(self.mut)]


# TODO:  might be cleaner as getAllele(), getGene(), getFamily()
def parseAllele(alleles, regex, action='first'):
    """
    Extract alleles from strings

    Arguments:  alleles = string with allele calls
                regex = compiled regular expression for allele match
                action = action to perform for multiple alleles;
                         one of ('first', 'set', 'list').
    Returns:    string of the allele for action='first';
                tuple of allele calls for 'set' or 'list' actions.
    """
    try:
        match = [x.group(0) for x in regex.finditer(alleles)]
    except:
        match = None

    if action == 'first':
        return match[0] if match else None
    elif action == 'set':
        return tuple(sorted(set(match))) if match else None
    elif action == 'list':
        return tuple(sorted(match)) if match else None
    else:
        return None
