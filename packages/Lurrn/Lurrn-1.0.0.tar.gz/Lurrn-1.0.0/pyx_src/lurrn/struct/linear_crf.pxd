# Bigram CRF with tag unigram potentials

cdef class LinearCRF:
    def __init__(self, feats, tag_feats):
        self.nTags = len(tag_feats)
        self.tag_feats = feats
        self.feats = feats
    cpdef double[:,::1] forward_max_scores(
        self, double[::1] w_init, double[::1] w_end, double[:,::1] w_trans,
        double[:,::1] scores):
        '''
        returns forward (Viterbi) scores that reflect
        the score before a given token.
        '''
        double[:,::1] fwd_scores
        #TODO actual computation
    cpdef double[:,::1] backward_max_scores(self, double[:,::1] scores):
        double[:,::1] bwd_scores
        #TODO actual computation
    cpdef int[::1] best_solution(
        self, double[::1] w_init, double[::1] w_end, double[:,::1] w_trans,
        double[:,::1] scores):
        '''
        returns the 1-best solution
        '''
        int[::1] result
    cpdef VecD2 pruned_unigrams(self):
        '''
        returns a list of (position, tag, goodness)
        scores for tag unigrams
        '''

