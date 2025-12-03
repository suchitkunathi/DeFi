import streamlit as st
from crypto import Wallet
from blockchain import Ledger
from contracts import LendingPool
import time
import pandas as pd

                          
if 'ledger' not in st.session_state:
    st.session_state.ledger = Ledger()
    st.session_state.alice = Wallet()
    st.session_state.bob = Wallet()
    st.session_state.pool = LendingPool(st.session_state.ledger)
    
                     
    st.session_state.ledger.update_balance(st.session_state.alice.address, 10000, "USDC")
    st.session_state.ledger.update_balance(st.session_state.bob.address, 10, "ETH")

st.set_page_config(page_title="DeFi Simulator", layout="wide", page_icon="🏦")

            
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #000000;
    }
    .stMetric label {
        color: #333333 !important;
    }
    .stMetric div[data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    .stMetric div[data-testid="stMetricDelta"] {
        color: #666666 !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
        border-color: #45a049;
        color: white;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 DeFi Lending Protocol Simulator")
st.markdown("Simulate lending, borrowing, and earning interest on a decentralized protocol.")

                              
with st.sidebar:
    st.header("🔐 Wallet Selector")
    user_option = st.selectbox("Select User", ["Alice", "Bob"])
    
    if user_option == "Alice":
        current_user = st.session_state.alice
        st.success(f"Logged in as **Alice**")
    else:
        current_user = st.session_state.bob
        st.info(f"Logged in as **Bob**")

    st.code(f"{current_user.address}", language="text")
    st.caption("Wallet Address")
    
    st.markdown("---")
    st.subheader("💰 Current Balance")
    usdc_bal = st.session_state.ledger.get_balance(current_user.address, "USDC")
    eth_bal = st.session_state.ledger.get_balance(current_user.address, "ETH")
    
    st.metric("USDC", f"{usdc_bal:,.2f}")
    st.metric("ETH", f"{eth_bal:,.4f}")

                
st.subheader("📊 Protocol Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pool Liquidity", f"{st.session_state.pool.total_liquidity:,.2f} USDC", delta="Available to Borrow")

with col2:
    st.metric("Total Borrowed", f"{st.session_state.pool.total_borrowed:,.2f} USDC", delta_color="inverse")

with col3:
    st.metric("APY (Borrow Rate)", f"{st.session_state.pool.get_borrow_rate() * 100:.2f}%", delta="Variable Rate")

st.markdown("---")

                       
st.subheader("👤 Your Position")
if current_user.address in st.session_state.pool.user_positions:
    pos = st.session_state.pool.user_positions[current_user.address]
    p_col1, p_col2, p_col3 = st.columns(3)
    p_col1.metric("Collateral Locked", f"{pos['collateral']:.4f} ETH")
    p_col2.metric("Borrowed Amount", f"{pos['borrowed']:.2f} USDC")
    
                                                
    collateral_value_usdc = pos['collateral'] * 2000                                                       
    health_factor = collateral_value_usdc / pos['borrowed'] if pos['borrowed'] > 0 else float('inf')
    
    p_col3.metric("Health Factor", f"{health_factor:.2f}", delta="> 1.5 Safe" if health_factor > 1.5 else "Risk", delta_color="normal" if health_factor > 1.5 else "inverse")
else:
    st.info("You have no active position in the lending pool.")

st.markdown("---")

         
st.subheader("⚡ Actions")
tab1, tab2, tab3, tab4 = st.tabs(["📥 Deposit", "🔒 Add Collateral", "💸 Borrow", "💳 Repay"])

with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("### Deposit USDC")
        st.write("Deposit your USDC into the lending pool to provide liquidity.")
        deposit_amount = st.number_input("Amount to Deposit (USDC)", min_value=0.0, step=100.0, key="dep")
    with c2:
        st.write("")         
        st.write("")
        if st.button("Confirm Deposit", key="btn_dep"):
            try:
                st.session_state.pool.deposit(current_user.address, deposit_amount)
                st.toast(f"✅ Successfully deposited {deposit_amount} USDC")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("### Add ETH Collateral")
        st.write("Lock ETH as collateral to borrow USDC.")
        collat_amount = st.number_input("Amount to Add (ETH)", min_value=0.0, step=0.1, key="col")
    with c2:
        st.write("")
        st.write("")
        if st.button("Confirm Collateral", key="btn_col"):
            try:
                st.session_state.pool.add_collateral(current_user.address, collat_amount)
                st.toast(f"✅ Added {collat_amount} ETH Collateral")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

with tab3:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("### Borrow USDC")
        st.write("Borrow USDC against your ETH collateral.")
        borrow_amount = st.number_input("Amount to Borrow (USDC)", min_value=0.0, step=100.0, key="bor")
    with c2:
        st.write("")
        st.write("")
        if st.button("Confirm Borrow", key="btn_bor"):
            try:
                st.session_state.pool.borrow(current_user.address, borrow_amount)
                st.toast(f"✅ Borrowed {borrow_amount} USDC")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

with tab4:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("### Repay Loan")
        st.write("Repay your borrowed USDC to unlock your collateral.")
        repay_amount = st.number_input("Amount to Repay (USDC)", min_value=0.0, step=100.0, key="rep")
    with c2:
        st.write("")
        st.write("")
        if st.button("Confirm Repayment", key="btn_rep"):
            try:
                st.session_state.pool.repay(current_user.address, repay_amount)
                st.toast(f"✅ Repaid {repay_amount} USDC")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")

                     
with st.expander("⚙️ Simulation Controls", expanded=True):
    if st.button("⏳ Simulate Time Passage (Accrue Interest)"):
        st.session_state.pool.accrue_interest()
        st.toast("✅ Time passed, interest accrued!")
        time.sleep(1)
        st.rerun()

                     
st.markdown("---")
st.subheader("📜 Transaction History")

if st.session_state.ledger.chain:
                                                            
    tx_data = []
    for tx in reversed(st.session_state.ledger.chain):                    
        tx_data.append({
            "Time": time.strftime('%H:%M:%S', time.localtime(tx.timestamp)),
            "Action": tx.action.upper(),
            "Amount": tx.amount,
            "Sender": f"{tx.sender[:6]}...",
            "Receiver": f"{tx.receiver[:6]}..."
        })
    
    df = pd.DataFrame(tx_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No transactions yet.")
