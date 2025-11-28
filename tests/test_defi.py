import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from crypto import Wallet
from blockchain import Ledger, Transaction
from contracts import LendingPool

class TestDeFi(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()
        self.alice = Wallet()
        self.bob = Wallet()
        self.pool = LendingPool(self.ledger)
        
        # Fund accounts
        self.ledger.update_balance(self.alice.address, 10000, "USDC")
        self.ledger.update_balance(self.bob.address, 10, "ETH")

    def test_wallet_signing(self):
        msg = "hello"
        sig = self.alice.sign(msg)
        self.assertTrue(Wallet.verify(msg, sig, self.alice.get_public_key_hex()))
        self.assertFalse(Wallet.verify("wrong", sig, self.alice.get_public_key_hex()))

    def test_deposit(self):
        self.pool.deposit(self.alice.address, 1000)
        self.assertEqual(self.pool.total_liquidity, 1000)
        self.assertEqual(self.ledger.get_balance(self.alice.address, "USDC"), 9000)

    def test_borrow_repay(self):
        # Deposit liquidity
        self.pool.deposit(self.alice.address, 5000)
        
        # Add collateral
        self.pool.add_collateral(self.bob.address, 2) # 4000 USD value
        
        # Borrow
        self.pool.borrow(self.bob.address, 1000)
        self.assertEqual(self.ledger.get_balance(self.bob.address, "USDC"), 1000)
        self.assertEqual(self.pool.total_borrowed, 1000)
        
        # Repay
        self.pool.repay(self.bob.address, 1000)
        self.assertEqual(self.pool.user_positions[self.bob.address]["borrowed"], 0)

    def test_insufficient_collateral(self):
        self.pool.deposit(self.alice.address, 5000)
        self.pool.add_collateral(self.bob.address, 0.1) # 200 USD value
        
        with self.assertRaises(ValueError):
            self.pool.borrow(self.bob.address, 1000) # Max borrow is 150

if __name__ == '__main__':
    unittest.main()
