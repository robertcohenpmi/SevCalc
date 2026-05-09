import streamlit as st
from rules import CountryRules
from datetime import date

st.set_page_config(page_title="HR Severance & IC Calculator", layout="centered")

st.title("⚖️ Severance & Bonus Calculator")
st.caption("Stateless Tool: No data is stored or saved.")

# --- SECTION 1: INPUTS ---
with st.form("calc_form"):
    with st.container(border=True):
        st.subheader("👤 Employee Profile")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            name = st.text_input("Full Name", value="Jane Smith")
        with col2:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
        with col3:
            country = st.selectbox("Country", ["UK"])

    with st.container(border=True):
        st.subheader("📅 Employment Dates")
        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            start_date = st.date_input("Start Date", value=date(2020, 1, 1))
        with col_d2:
            end_date = st.date_input("End Date (Notice Date)")
        with col_d3:
            annual_salary = st.number_input("Annual Base Salary (£)", min_value=0.0, step=1000.0, format="%.2f")

    with st.container(border=True):
        st.subheader("💰 Incentive Compensation (IC)")
        st.info("Bonus Cycle: February 1st to January 31st")
        col_ic1, col_ic2 = st.columns(2)
        with col_ic1:
            ic_percent = st.number_input("IC Target Percentage (%)", min_value=0.0, value=10.0)
        with col_ic2:
            multiplier_percent = st.number_input("Performance Multiplier (%)", min_value=0.0, value=100.0)

    # ADDED CALCULATION BUTTON
    submit = st.form_submit_button("Run Full Calculation")

# --- SECTION 2: RESULTS (Only shows after clicking button) ---
if submit:
    data = {
        'country': country, 'employee_name': name, 'age': age,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'annual_salary': annual_salary,
        'ic_percent': ic_percent, 'multiplier_percent': multiplier_percent
    }

    result = CountryRules.calculate_uk(data)

    st.divider()
    st.subheader(f"📊 Results for {name}")

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.markdown("### **Statutory Redundancy**")
        st.metric("Service Years", f"{result.get('years_of_service', 0)}")
        # Use .get() to prevent KeyError if the variable is missing
        st.write(f"**Weekly Cap Applied:** £{result.get('capped_pay', 0):,.2f}")
        st.write(f"**Multiplier Used:** {result.get('multiplier', 0)} weeks")
        st.write(f"**Subtotal:** £{result.get('statutory_pay', 0):,.2f}")

    with res_col2:
        st.markdown("### **Incentive Comp (IC)**")
        st.metric("Proration Days", f"{result.get('bonus_days', 0)}")
        
        full_target = annual_salary * (ic_percent / 100)
        st.write(f"**Full Year Target:** £{full_target:,.2f}")
        st.write(f"**Prorated Subtotal:** £{result.get('bonus_pay', 0):,.2f}")

    st.success(f"### **Total Package: £{result.get('total_package', 0):,.2f}**")

    # Exports
    audit_data = f"Name,End Date,Base,Statutory,Bonus,Total\n{name},{end_date},{annual_salary},{result['statutory_pay']},{result['bonus_pay']},{result['total_package']}"
    st.download_button("📋 Download Audit CSV", data=audit_data, file_name=f"audit_{name}.csv", mime="text/csv")