import streamlit as st
from datetime import datetime, date

# Page config - makes it look like a real app
st.set_page_config(
    page_title="Fertilizer Order Kenya",
    page_icon="🌱",
    layout="centered"
)

# Custom CSS to make it look exactly like your beautiful design
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #0ea5e9, #22d3ee);}
    .stApp {background: transparent;}
    h1 {color: white; text-align: center; text-shadow: 0 2px 10px rgba(0,0,0,0.3);}
    .css-1d391kg {padding-top: 2rem;}
    .success-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌱 Fertilizer Order Kenya")

st.markdown("### Place an Order")
st.info("Enter your company access code to proceed.")

# Access code (you can change this or connect to database later)
ACCESS_CODE = "FARM2025"

code = st.text_input("Company access code", type="password")

if code == ACCESS_CODE:
    st.success("✅ Access granted! Please fill the order below.")

    with st.form("fertilizer_form"):
        st.subheader("Farmer & Order Details")

        col1, col2 = st.columns(2)
        with col1:
            farmer_name = st.text_input("Farmer name *", placeholder="e.g. John Kamau")
            farmer_id = st.text_input("Farmer ID (optional)", placeholder="e.g. 123456")
        with col2:
            phone = st.text_input("Phone number *", placeholder="e.g. 0712345678")

        col3, col4 = st.columns(2)
        with col3:
            fertilizer = st.selectbox("Fertilizer *", [
                "", "DAP (Diammonium Phosphate)", "UREA", "NPK 17-17-17", "CAN", "MOP"
            ])
            bags = st.selectbox("Bag size", ["25 kg", "50 kg"])
        with col4:
            quantity = st.number_input("Number of bags *", min_value=1, value=1)
            delivery_date = st.date_input("Preferred delivery date *", min_value=date.today())

        address = st.text_area("Delivery address *", placeholder="e.g. Kitale, Trans-Nzoia County")
        
        col5, col6 = st.columns(2)
        with col5:
            payment = st.selectbox("Payment method *", ["", "M-Pesa", "Cash on delivery", "Bank transfer"])
        with col6:
            notes = st.text_area("Notes (optional)", placeholder="Any special instructions...")

        submitted = st.form_submit_button("🚀 Submit Order", use_container_width=True)

        if submitted:
            if not all([farmer_name, phone, fertilizer, address, payment]):
                st.error("Please fill all required fields (*)")
            else:
                st.success(f"""
                **Order Submitted Successfully!** 🌾
                
                Farmer: **{farmer_name}** ({farmer_id or 'No ID'})
                Order: **{quantity} bags** of {fertilizer} ({bags})
                Delivery: {delivery_date} to {address}
                Payment: {payment}
                """)
                # Here you can later send to WhatsApp, email, Google Sheets, etc.

elif code and code != ACCESS_CODE:
    st.error("❌ Wrong access code. Try again or contact admin.")

else:
    st.markdown("<br><br>", unsafe_allow_html=True)