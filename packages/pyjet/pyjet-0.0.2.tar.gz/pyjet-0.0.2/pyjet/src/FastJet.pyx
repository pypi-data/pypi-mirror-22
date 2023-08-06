include "FastJet.pxi"


cdef class PyPseudoJet:
    """ Python wrapper class for fastjet::PseudoJet
    """
    cdef PseudoJet jet
    cdef vector[PseudoJet] constits

    @staticmethod
    cdef wrap(PseudoJet& jet):
        wrapped_jet = PyPseudoJet()
        wrapped_jet.jet = jet
        if jet.has_valid_cluster_sequence() and jet.has_constituents():
            wrapped_jet.constits = jet.constituents()
        return wrapped_jet

    def __contains__(self, other):
        cdef PseudoJet* jet = <PseudoJet*> PyCObject_AsVoidPtr(other.jet)
        if jet == NULL:
            raise TypeError("object must be of type PyPseudoJet")
        return self.jet.contains(deref(jet))

    def __len__(self):
        return self.constits.size()

    def __iter__(self):
        cdef PseudoJet jet
        for jet in self.constits:
            yield PyPseudoJet.wrap(jet)

    def constituents(self):
        return list(self)

    def constituents_array(self, bool ep=False):
        # convert pseudojets into numpy array
        cdef np.ndarray jets
        if ep:
            jets = np.empty(self.constits.size(), dtype=dtype_fourvect)
        else:
            jets = np.empty(self.constits.size(), dtype=dtype_jet)
        cdef DTYPE_t* data = <DTYPE_t *> jets.data
        cdef PseudoJet jet
        cdef unsigned int ijet
        if ep:
            for ijet in range(self.constits.size()):
                jet = self.constits[ijet]
                data[ijet * 4 + 0] = jet.e()
                data[ijet * 4 + 1] = jet.px()
                data[ijet * 4 + 2] = jet.py()
                data[ijet * 4 + 3] = jet.pz()
        else:
            for ijet in range(self.constits.size()):
                jet = self.constits[ijet]
                data[ijet * 4 + 0] = jet.perp()
                data[ijet * 4 + 1] = jet.pseudorapidity()
                data[ijet * 4 + 2] = jet.phi_std()
                data[ijet * 4 + 3] = jet.m()
        return jets

    @property
    def pt(self):
        return self.jet.perp()

    @property
    def eta(self):
        return self.jet.pseudorapidity()

    @property
    def phi(self):
        return self.jet.phi_std()

    @property
    def mass(self):
        return self.jet.m()

    @property
    def e(self):
        return self.jet.e()

    @property
    def et(self):
        return self.jet.Et()

    @property
    def px(self):
        return self.jet.px()

    @property
    def py(self):
        return self.jet.py()

    @property
    def pz(self):
        return self.jet.pz()

    def __repr__(self):
        return "PyPseudoJet(pt={0}, eta={1}, phi={2}, mass={3})".format(
            self.pt, self.eta, self.phi, self.mass)


@cython.boundscheck(False)
@cython.wraparound(False)
def cluster(np.ndarray vectors, float R, int p, bool ep=False, bool return_array=False):
    """
    Perform jet clustering on a numpy array of 4-vectors in (pT, eta, phi, mass) representation, otherwise (E, px, py, pz) representation if ep=True

    Parameters
    ----------

    vectors: np.ndarray
        Array of 4-vectors as (pT, eta, phi, mass) or (E, px, py, pz) if ep=True
    R : float
        Clustering size parameter
    p : int
        Generalized kT clustering parameter (p=1 for kT, p=-1 for anti-kT, p=0 for C/A)

    Returns
    -------

    jets : list or np.ndarray
        If return_array=False then return list of PyPseudoJets.
        Otherwise return array of (pT, eta, phi, mass) or (E, px, py, pz) if ep=True.

    """
    cdef vector[PseudoJet] pseudojets
    cdef PseudoJet jet
    cdef ClusterSequence* sequence
    # convert numpy array into vector of pseudojets
    array_to_pseudojets(
        vectors.shape[0], len(vectors.dtype.names),
        <DTYPE_t*> vectors.data,
        pseudojets, -1, ep)

    # cluster and sort by decreasing pt
    sequence = cluster_genkt(pseudojets, R, p)
    pseudojets = sorted_by_pt(sequence.inclusive_jets())

    if not return_array:
        # return pseudojets
        py_jets = []
        for jet in pseudojets:
            py_jets.append(PyPseudoJet.wrap(jet))
        # the jets own the ClusterSequence through a shared_ptr
        sequence.delete_self_when_unused()
        return py_jets

    # no need to keep sequence when returning array
    del sequence

    # convert pseudojets into numpy array
    cdef np.ndarray jets
    if ep:
        jets = np.empty(pseudojets.size(), dtype=dtype_fourvect)
    else:
        jets = np.empty(pseudojets.size(), dtype=dtype_jet)
    cdef DTYPE_t* data = <DTYPE_t *> jets.data
    cdef unsigned int ijet;
    cdef PseudoJet pseudojet
    if ep:
        for ijet in range(pseudojets.size()):
            pseudojet = pseudojets[ijet]
            data[ijet * 4 + 0] = pseudojet.e()
            data[ijet * 4 + 1] = pseudojet.px()
            data[ijet * 4 + 2] = pseudojet.py()
            data[ijet * 4 + 3] = pseudojet.pz()
    else:
        for ijet in range(pseudojets.size()):
            pseudojet = pseudojets[ijet]
            data[ijet * 4 + 0] = pseudojet.perp()
            data[ijet * 4 + 1] = pseudojet.pseudorapidity()
            data[ijet * 4 + 2] = pseudojet.phi_std()
            data[ijet * 4 + 3] = pseudojet.m()
    return jets
