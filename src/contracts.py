from blockchain import Ledger

class LendingPool:
    def __init__(self, ledger, token_name="USDC", collateral_token="ETH"):
        self.ledger = ledger
        self.token_name = token_name
        self.collateral_token = collateral_token
        
                    
        self.total_liquidity = 0.0
        self.total_borrowed = 0.0
        self.base_rate = 0.05               
        
                                                                                             
        self.user_positions = {}
        
                                                
        self.pool_address = "LENDING_POOL_ADDRESS"

    def get_utilization_rate(self):
        if self.total_liquidity == 0:
            return 0
        return self.total_borrowed / self.total_liquidity

    def get_borrow_rate(self):
                                                                       
        utilization = self.get_utilization_rate()
        return self.base_rate + (utilization * 0.1)

    def deposit(self, user_address, amount):
                                       
                                                          
                                                              
        
        user_bal = self.ledger.get_balance(user_address, self.token_name)
        if user_bal < amount:
            raise ValueError("Insufficient funds to deposit")
            
                                      
        self.ledger.update_balance(user_address, -amount, self.token_name)
        self.ledger.update_balance(self.pool_address, amount, self.token_name)
        
        self.total_liquidity += amount
        print(f"User {user_address[:8]} deposited {amount} {self.token_name}")

    def add_collateral(self, user_address, amount):
        user_bal = self.ledger.get_balance(user_address, self.collateral_token)
        if user_bal < amount:
            raise ValueError("Insufficient collateral funds")
            
        self.ledger.update_balance(user_address, -amount, self.collateral_token)
        self.ledger.update_balance(self.pool_address, amount, self.collateral_token)
        
        if user_address not in self.user_positions:
            self.user_positions[user_address] = {"collateral": 0.0, "borrowed": 0.0, "interest_index": 1.0}
            
        self.user_positions[user_address]["collateral"] += amount
        print(f"User {user_address[:8]} added {amount} {self.collateral_token} collateral")

    def borrow(self, user_address, amount):
                                                
                                                 
        ETH_PRICE = 2000.0 
        
        if user_address not in self.user_positions:
             raise ValueError("No collateral deposited")
             
        position = self.user_positions[user_address]
        collateral_value = position["collateral"] * ETH_PRICE
        max_borrow = collateral_value * 0.75
        
        if position["borrowed"] + amount > max_borrow:
            raise ValueError("Insufficient collateral for this borrow amount")
            
        if amount > (self.total_liquidity - self.total_borrowed):
            raise ValueError("Not enough liquidity in pool")
            
                                         
        self.ledger.update_balance(self.pool_address, -amount, self.token_name)
        self.ledger.update_balance(user_address, amount, self.token_name)
        
        position["borrowed"] += amount
        self.total_borrowed += amount
        print(f"User {user_address[:8]} borrowed {amount} {self.token_name}")

    def repay(self, user_address, amount):
        if user_address not in self.user_positions:
            raise ValueError("No loan found")
            
        position = self.user_positions[user_address]
        
        if amount > position["borrowed"]:
            amount = position["borrowed"]                    
            
        user_bal = self.ledger.get_balance(user_address, self.token_name)
        if user_bal < amount:
            raise ValueError("Insufficient funds to repay")
            
                                    
        self.ledger.update_balance(user_address, -amount, self.token_name)
        self.ledger.update_balance(self.pool_address, amount, self.token_name)
        
        position["borrowed"] -= amount
        self.total_borrowed -= amount
        print(f"User {user_address[:8]} repaid {amount} {self.token_name}")

    def accrue_interest(self):
                                     
        rate = self.get_borrow_rate()
                                                       
                                                             
        for user, pos in self.user_positions.items():
            if pos["borrowed"] > 0:
                interest = pos["borrowed"] * 0.01 
                pos["borrowed"] += interest
                                                                                                 
                                                                   
                print(f"Interest accrued for {user[:8]}: {interest}")
