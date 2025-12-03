from crypto import Wallet
from blockchain import Ledger, Transaction
from contracts import LendingPool
import time

def main():
    print("=== DeFi Application Simulation ===")
    
              
    print("\n[1] Setting up Wallets and Ledger...")
    ledger = Ledger()
    alice = Wallet()
    bob = Wallet()
    
    print(f"Alice Address: {alice.address}")
    print(f"Bob Address: {bob.address}")
    
                                                    
    print("\n[2] Funding Wallets (Faucet)...")
    ledger.update_balance(alice.address, 10000, "USDC")                        
    ledger.update_balance(bob.address, 10, "ETH")                       
    
    print(f"Alice Balance: {ledger.get_balance(alice.address, 'USDC')} USDC")
    print(f"Bob Balance: {ledger.get_balance(bob.address, 'ETH')} ETH")
    
                                
    print("\n[3] Initializing Lending Pool...")
    pool = LendingPool(ledger, token_name="USDC", collateral_token="ETH")
    
                            
    print("\n[4] Alice Deposits 5000 USDC to Pool...")
                                                                        
                                                               
    pool.deposit(alice.address, 5000)
    
    print(f"Pool Liquidity: {pool.total_liquidity} USDC")
    print(f"Alice Balance: {ledger.get_balance(alice.address, 'USDC')} USDC")
    
                            
    print("\n[5] Bob Adds 5 ETH Collateral...")
    pool.add_collateral(bob.address, 5)
    
                         
    print("\n[6] Bob Borrows 2000 USDC...")
                                                                
    pool.borrow(bob.address, 2000)
    
    print(f"Bob USDC Balance: {ledger.get_balance(bob.address, 'USDC')} USDC")
    print(f"Pool Total Borrowed: {pool.total_borrowed} USDC")
    
                                         
    print("\n[7] Simulating Interest Accrual...")
    pool.accrue_interest()
    
    bob_pos = pool.user_positions[bob.address]
    print(f"Bob's Debt after interest: {bob_pos['borrowed']} USDC")
    
                   
    print("\n[8] Bob Repays Loan...")
                                          
                                                                                
                                                                            
    
                                                                   
    ledger.update_balance(bob.address, 100, "USDC") 
    
    repay_amount = bob_pos['borrowed']
    pool.repay(bob.address, repay_amount)
    
    print(f"Bob's Remaining Debt: {pool.user_positions[bob.address]['borrowed']} USDC")
    print(f"Pool Liquidity: {pool.total_liquidity} USDC")
    
    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    main()
