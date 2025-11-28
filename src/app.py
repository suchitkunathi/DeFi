import streamlit as st
from crypto import Wallet
from blockchain import Ledger
from contracts import LendingPool
import time

# Initialize session state
if 'ledger' not in st.session_state:
    st.session_state.ledger = Ledger()
    st.session_state.alice = Wallet()
    st.session_state.bob = Wallet()
    st.session_state.pool = LendingPool(st.session_state.ledger)
    
    # Initial funding
    st.session_state.ledger.update_balance(st.session_state.alice.address, 10000, "USDC")
    st.session_state.ledger.update_balance(st.session_state.bob.address, 10, "ETH")

st.set_page_config(page_title="DeFi Simulator", layout="wide")

st.title("DeFi Lending Protocol Simulator")

# Sidebar for Wallet Selection
st.sidebar.header("Wallet Selector")
user_option = st.sidebar.selectbox("Select User", ["Alice", "Bob"])

if user_option == "Alice":
    current_user = st.session_state.alice
    st.sidebar.success(f"Logged in as Alice")
else:
    current_user = st.session_state.bob
    st.sidebar.info(f"Logged in as Bob")

st.sidebar.code(f"Address: {current_user.address[:10]}...")

# Main Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pool Liquidity (USDC)", f"{st.session_state.pool.total_liquidity:.2f}")

with col2:
    st.metric("Total Borrowed (USDC)", f"{st.session_state.pool.total_borrowed:.2f}")

with col3:
    st.metric("Current Interest Rate", f"{st.session_state.pool.get_borrow_rate() * 100:.2f}%")

# User Balances
st.subheader(f"{user_option}'s Wallet")
usdc_bal = st.session_state.ledger.get_balance(current_user.address, "USDC")
eth_bal = st.session_state.ledger.get_balance(current_user.address, "ETH")

b_col1, b_col2 = st.columns(2)
b_col1.metric("USDC Balance", f"{usdc_bal:.2f}")
b_col2.metric("ETH Balance", f"{eth_bal:.2f}")

# User Position in Pool
st.subheader("Your Pool Position")
if current_user.address in st.session_state.pool.user_positions:
    pos = st.session_state.pool.user_positions[current_user.address]
    p_col1, p_col2 = st.columns(2)
    p_col1.metric("Collateral Locked (ETH)", f"{pos['collateral']:.2f}")
    p_col2.metric("Borrowed Amount (USDC)", f"{pos['borrowed']:.2f}")
else:
    st.info("No active position in pool.")

st.markdown("---")

# Actions
tab1, tab2, tab3, tab4 = st.tabs(["Deposit", "Add Collateral", "Borrow", "Repay"])

with tab1:
    st.write("### Deposit USDC to earn interest")
    deposit_amount = st.number_input("Amount to Deposit (USDC)", min_value=0.0, step=100.0, key="dep")
    if st.button("Deposit"):
        try:
            st.session_state.pool.deposit(current_user.address, deposit_amount)
            st.success(f"Deposited {deposit_amount} USDC")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.write("### Add ETH Collateral")
    collat_amount = st.number_input("Amount to Add (ETH)", min_value=0.0, step=0.1, key="col")
    if st.button("Add Collateral"):
        try:
            st.session_state.pool.add_collateral(current_user.address, collat_amount)
            st.success(f"Added {collat_amount} ETH Collateral")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

with tab3:
    st.write("### Borrow USDC against Collateral")
    borrow_amount = st.number_input("Amount to Borrow (USDC)", min_value=0.0, step=100.0, key="bor")
    if st.button("Borrow"):
        try:
            st.session_state.pool.borrow(current_user.address, borrow_amount)
            st.success(f"Borrowed {borrow_amount} USDC")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

with tab4:
    st.write("### Repay Loan")
    repay_amount = st.number_input("Amount to Repay (USDC)", min_value=0.0, step=100.0, key="rep")
    if st.button("Repay"):
        try:
            st.session_state.pool.repay(current_user.address, repay_amount)
            st.success(f"Repaid {repay_amount} USDC")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
if st.button("Simulate Time (Accrue Interest)"):
    st.session_state.pool.accrue_interest()
    st.success("Interest accrued!")
    st.rerun()
