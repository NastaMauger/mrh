import unittest
import numpy as np
from pyscf import gto, scf
from mrh.my_pyscf.mcscf.soc_int import compute_hso
from mrh.my_pyscf.mcscf.lassi_op_o0 import si_soc

def setUpModule():
    global mol, mfh2o, h2o_dm
    mol = gto.M (atom="""
        O  0.000000  0.000000  0.000000
        H  0.758602  0.000000  0.504284
        H  0.758602  0.000000  -0.504284
    """, basis='631g')
    mfh2o = scf.RHF (mol).run ()
    
    # Pre-calculated atomic densities used in AMFI
    h2o_dm = np.zeros ((13,13))
    h2o_dm[0,0] = h2o_dm[1,1] = 2
    h2o_dm[3,3] = h2o_dm[4,4] = h2o_dm[5,5] = 4/3

    # Below obtained from OpenMolcas v22.02
    int_ref = np.array ([0.0000000185242348, 0.0000393310222742, 0.0000393310222742, 0.0005295974407740]) 

def tearDownModule():
    global mol, mfh2o, h2o_dm
    mol.stdout.close()
    del mol, mfh2o, h2o_dm, int_ref

class KnownValues (unittest.TestCase):

    def test_soc_int (self):
        # Pre-calculated atomic densities used in the OpenMolcas version of AMFI
        h2o_dm = np.zeros ((13,13))
        h2o_dm[0,0] = h2o_dm[1,1] = 2
        h2o_dm[3,3] = h2o_dm[4,4] = h2o_dm[5,5] = 4/3

        # Obtained from OpenMolcas v22.02
        int_ref = np.array ([0.0000000185242348, 0.0000393310222742, 0.0000393310222742, 0.0005295974407740]) 
        
        amfi_int = compute_hso (mol, h2o_dm, amfi=True)
        amfi_int = amfi_int[2][amfi_int[2] > 0]
        self.assertAlmostEqual (np.sort (amfi_int), int_ref, 10)

    def test_soc_1frag (self):
        ## compare excited state energies (incl. SOC) for 1 frag calculation

    def test_soc_2frag (self):
        ## stationary test for >1 frag calc

    def test_soc_stdm12s (self):
        ## stationary test for roots_make_stdm12s
  
  def test_soc_rdm12s (self):
        ## stationary test for roots_make_rdm12s

if __name__ == "__main__":
    print("Full Tests for SOC")
    unittest.main()
