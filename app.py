app_code = '''
import streamlit as st
import pandas as pd
from datetime import date, datetime
import uuid
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURATION ---
SHEET_ID = "107185697411127795995"  # from your Google Sheet URL
SERVICE_ACCOUNT_FILE = "fertilizerordersapp-9b3706737334.json"  # e.g. fertilizerapp-123456.json
COMPANY_CODE = "GREENFLO"
ADMIN_CODE = "GF_ADMIN_2025"

FERTILIZER_TYPES = [
    {"id":"DAP", "name":"DAP (Diammonium Phosphate)", "bag_sizes":[25,50]},
    {"id":"Urea", "name":"Urea", "bag_sizes":[50]},
    {"id":"NPK_20_10_10", "name":"NPK 20-10-10", "bag_sizes":[25,50]},
    {"id":"CAN", "name":"CAN (Calcium Ammonium Nitrate)", "bag_sizes":[50]},
]

PAYMENT_METHODS = ["Cash on delivery", "Mobile money (M-Pesa)", "Bank Transfer", "Company credit"]

st.set_page_config(page_title="Fertilizer Order Portal", layout="centered")

# --- Connect to Google Sheet ---
creds_info = st.secrets["gcp_service_account"]
creds = Credentials.from_service_account_info(creds_info)
client = gspread.authorize(creds)
sheet = client.open("FertilizerOrders").sheet1

# --- Helper to add order to sheet ---
def append_order_to_sheet(order_dict):
    headers = list(order_dict.keys())
    existing_headers = sheet.row_values(1)
    if not existing_headers:
        sheet.append_row(headers)
    sheet.append_row(list(order_dict.values()))

def fertilizer_lookup(fid):
    for f in FERTILIZER_TYPES:
        if f["id"]==fid:
            return f
    return None

# --- UI ---
st.title("🌾 Fertilizer Order Portal")
st.caption("Place fertilizer orders for your farming cooperative or company.")

menu = st.sidebar.selectbox("Menu", ["Place Order", "My Orders", "Admin"])

if menu == "Place Order":
    st.header("Place an Order")
    with st.form("access_form"):
        company_code = st.text_input("Company access code", type="password")
        access = st.form_submit_button("Continue")
    if access:
        if company_code.strip().upper() != COMPANY_CODE:
            st.error("Invalid company access code.")
        else:
            st.success("Access granted. Fill in your order details below.")
            with st.form("order_form"):
                farmer_name = st.text_input("Farmer name")
                farmer_id = st.text_input("Farmer ID (optional)")
                phone = st.text_input("Phone number")
                fert_choice = st.selectbox("Fertilizer", [f"{item['id']} — {item['name']}" for item in FERTILIZER_TYPES])
                fert_id = fert_choice.split(" — ")[0]
                fert = fertilizer_lookup(fert_id)
                bag_size = st.selectbox("Bag size (kg)", fert["bag_sizes"])
                quantity = st.number_input("Quantity (bags)", min_value=1, value=1, step=1)
                delivery_address = st.text_area("Delivery address")
                delivery_date = st.date_input("Preferred delivery date", min_value=date.today())
                payment_method = st.selectbox("Payment method", PAYMENT_METHODS)
                notes = st.text_area("Notes (optional)")
                submit = st.form_submit_button("Submit Order")
            if submit:
                if not farmer_name or not phone or not delivery_address:
                    st.warning("Please fill in required fields.")
                else:
                    order = {
                        "order_id": str(uuid.uuid4())[:8],
                        "timestamp": datetime.utcnow().isoformat(),
                        "farmer_name": farmer_name,
                        "farmer_id": farmer_id,
                        "phone": phone,
                        "fertilizer_id": fert["id"],
                        "fertilizer_name": fert["name"],
                        "bag_size_kg": bag_size,
                        "quantity_bags": quantity,
                        "total_kg": bag_size * quantity,
                        "delivery_address": delivery_address,
                        "delivery_date": delivery_date.isoformat(),
                        "payment_method": payment_method,
                        "notes": notes,
                        "status": "Pending"
                    }
                    append_order_to_sheet(order)
                    st.success("✅ Order submitted successfully!")
                    st.write("Order Summary:")
                    st.dataframe(pd.DataFrame([order]).T.rename(columns={0:"value"}))

elif menu == "My Orders":
    st.header("Your Orders")
    st.info("To see your order history, open the shared Google Sheet (company staff view only).")

elif menu == "Admin":
    st.header("Admin View")
    code = st.text_input("Enter admin code", type="password")
    if code == ADMIN_CODE:
        st.success("Admin access granted")
        records = sheet.get_all_records()
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df)
        else:
            st.info("No orders yet.")
    else:
        st.warning("Enter admin code to continue.")
'''
with open("app.py", "w") as f:
    f.write(app_code)
print("✅ app.py created!")
