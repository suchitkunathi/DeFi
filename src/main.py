from crypto import Wallet
from blockchain import Ledger, Transaction
from contracts import LendingPool
import time

def main():
    print("=== DeFi Application Simulation ===")
    
    # 1. Setup
    print("\n[1] Setting up Wallets and Ledger...")
    ledger = Ledger()
    alice = Wallet()
    bob = Wallet()
    
    print(f"Alice Address: {alice.address}")
    print(f"Bob Address: {bob.address}")
    
    # 2. Initial Funding (Simulate mining or faucet)
    print("\n[2] Funding Wallets (Faucet)...")
    ledger.update_balance(alice.address, 10000, "USDC") # Alice has 10,000 USDC
    ledger.update_balance(bob.address, 10, "ETH")       # Bob has 10 ETH
    
    print(f"Alice Balance: {ledger.get_balance(alice.address, 'USDC')} USDC")
    print(f"Bob Balance: {ledger.get_balance(bob.address, 'ETH')} ETH")
    
    # 3. Initialize Lending Pool
    print("\n[3] Initializing Lending Pool...")
    pool = LendingPool(ledger, token_name="USDC", collateral_token="ETH")
    
    # 4. Alice Deposits USDC
    print("\n[4] Alice Deposits 5000 USDC to Pool...")
    # In a real app, Alice would sign a transaction to approve/transfer.
    # Here we simulate the contract call which checks balances.
    pool.deposit(alice.address, 5000)
    
    print(f"Pool Liquidity: {pool.total_liquidity} USDC")
    print(f"Alice Balance: {ledger.get_balance(alice.address, 'USDC')} USDC")
    
    # 5. Bob Adds Collateral
    print("\n[5] Bob Adds 5 ETH Collateral...")
    pool.add_collateral(bob.address, 5)
    
    # 6. Bob Borrows USDC
    print("\n[6] Bob Borrows 2000 USDC...")
    # Max borrow for 5 ETH * 2000 = 10000 USD * 0.75 = 7500 USDC
    pool.borrow(bob.address, 2000)
    
    print(f"Bob USDC Balance: {ledger.get_balance(bob.address, 'USDC')} USDC")
    print(f"Pool Total Borrowed: {pool.total_borrowed} USDC")
    
    # 7. Simulate Time Passing & Interest
    print("\n[7] Simulating Interest Accrual...")
    pool.accrue_interest()
    
    bob_pos = pool.user_positions[bob.address]
    print(f"Bob's Debt after interest: {bob_pos['borrowed']} USDC")
    
    # 8. Bob Repays
    print("\n[8] Bob Repays Loan...")
    # Bob needs to repay 2000 + interest. 
    # He has 2000 USDC borrowed. He might need to get more USDC if interest > 0.
    # For this sim, let's assume he has enough or we just repay what he has.
    
    # Let's give Bob a bit more USDC to cover interest for the demo
    ledger.update_balance(bob.address, 100, "USDC") 
    
    repay_amount = bob_pos['borrowed']
    pool.repay(bob.address, repay_amount)
    
    print(f"Bob's Remaining Debt: {pool.user_positions[bob.address]['borrowed']} USDC")
    print(f"Pool Liquidity: {pool.total_liquidity} USDC")
    
    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    main()
