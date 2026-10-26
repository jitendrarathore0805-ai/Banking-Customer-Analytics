# streamlit_app.pyimport
import streamlit as st
import requests
import json
API_BASE = "http://127.0.0.1:8000"  # change if your FastAPI runs elsewhere
st.set_page_config(page_title="Bank Models UI", layout="centered")
st.title("Bank Models — Streamlit UI")
st.markdown("Use this UI to call the Segmentation and Personal Loan prediction endpoints.")
tab1, tab2 = st.tabs(["Customer Segmentation", "Personal Loan Prediction"])
# ---------- Helper functions ----------
def post_json(endpoint: str, payload: dict):
    url = f"{API_BASE}{endpoint}"
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return {"ok": True, "data": resp.json()}
    except requests.exceptions.HTTPError as e:
        return {"ok": False, "error": f"HTTP {resp.status_code}: {resp.text}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
def format_payload(payload: dict):
    return json.dumps(payload, indent=2)
# ---------- Tab 1: Customer Segmentation ----------
with tab1:
    st.header("Customer Segmentation")
    st.write("Predict cluster for a single customer. Endpoint: `POST /get_customer_segmentation`")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("age", min_value=0, max_value=120, value=35)
        experience = st.number_input("experience", min_value=0, max_value=80, value=10)
    with col2:
        income = st.number_input("income", min_value=0.0, value=80.0, step=1.0)
        family = st.selectbox("family", options=[1,2,3,4], index=1)
    with col3:
        ccavg = st.number_input("ccavg", min_value=0.0, value=2.5, step=0.1)
        mortgage = st.number_input("mortgage", min_value=0.0, value=2.5, step=0.1)
    seg_sample_btn = st.button("Use sample payload for segmentation")
    if seg_sample_btn:
        # different sample values
        age = 42
        experience = 18
        income = 125.0
        family = 3
        ccavg = 3.2
        mortgage=2
        st.experimental_rerun()
    seg_payload = {
        "age": int(age),
        "experience": int(experience),
        "income": int(income),
        "family": int(family),
        "ccavg": float(ccavg),
        "mortgage":int(mortgage)
    }
    st.subheader("Payload (sent)")
    st.code(format_payload(seg_payload), language="json")
    if st.button("Get Segmentation"):
        with st.spinner("Calling segmentation endpoint..."):
            result = post_json("/get_customer_segmentation", seg_payload)
        if result["ok"]:
            st.success("Response received")
            st.json(result["data"])
        else:
            st.error("Error calling endpoint")
            st.write(result["error"])
# ---------- Tab 2: Personal Loan Prediction ----------
with tab2:
    st.header("Personal Loan Prediction")
    st.write("Predict if a customer will take a personal loan. Endpoint: `POST /predict_loan/` (lowercase keys)")
    # Layout inputs in two columns
    left, right = st.columns(2)
    with left:
        age = st.number_input("age", min_value=18, max_value=120, value=35, key="loan_age")
        experience = st.number_input("experience", min_value=0, max_value=80, value=10, key="loan_exp")
        income = st.number_input("income", min_value=0.0, value=80.0, step=1.0, key="loan_income")
        zip_code = st.number_input("zip_code", min_value=0, value=94112, step=1, key="loan_zip")
        family = st.selectbox("family", options=[1,2,3,4], index=1, key="loan_family")
        ccavg = st.number_input("ccavg", min_value=0.0, value=2.5, step=0.1, key="loan_ccavg")
    with right:
        education = st.selectbox("education (1/2/3)", options=[1,2,3], index=1, key="loan_edu")
        mortgage = st.number_input("mortgage", min_value=0.0, value=0.0, step=1.0, key="loan_mortgage")
        securities_account = st.selectbox("securities_account", options=[0,1], index=0, key="loan_securities")
        cd_account = st.selectbox("cd_account", options=[0,1], index=0, key="loan_cd")
        online = st.selectbox("online", options=[0,1], index=1, key="loan_online")
        creditcard = st.selectbox("creditcard", options=[0,1], index=1, key="loan_credit")
    loan_sample = st.button("Use sample payload for loan prediction")
    if loan_sample:
        # sample values (different from earlier)
        st.session_state.loan_age = 42
        st.session_state.loan_exp = 18
        st.session_state.loan_income = 125.0
        st.session_state.loan_zip = 90089
        st.session_state.loan_family = 3
        st.session_state.loan_ccavg = 3.2
        st.session_state.loan_edu = 3
        st.session_state.loan_mortgage = 120.0
        st.session_state.loan_securities = 1
        st.session_state.loan_cd = 1
        st.session_state.loan_online = 0
        st.session_state.loan_credit = 1
        st.experimental_rerun()
    loan_payload = {
        "age": float(st.session_state.get("loan_age", age)),
        "experience": float(st.session_state.get("loan_exp", experience)),
        "income": float(st.session_state.get("loan_income", income)),
        "zip_code": int(st.session_state.get("loan_zip", zip_code)),
        "family": int(st.session_state.get("loan_family", family)),
        "ccavg": float(st.session_state.get("loan_ccavg", ccavg)),
        "education": int(st.session_state.get("loan_edu", education)),
        "mortgage": float(st.session_state.get("loan_mortgage", mortgage)),
        "securities_account": int(st.session_state.get("loan_securities", securities_account)),
        "cd_account": int(st.session_state.get("loan_cd", cd_account)),
        "online": int(st.session_state.get("loan_online", online)),
        "creditcard": int(st.session_state.get("loan_credit", creditcard)),
    }
    st.subheader("Payload (sent)")
    st.code(format_payload(loan_payload), language="json")
    if st.button("Predict Personal Loan"):
        with st.spinner("Calling loan prediction endpoint..."):
            result = post_json("/predict_personal_loan/", loan_payload)
        if result["ok"]:
            st.success("Response received")
            # show prettified response if it's simple
            try:
                st.json(result["data"])
            except Exception:
                st.write(result["data"])
        else:
            st.error("Error calling endpoint")
            st.write(result["error"])
# ---------- Footer ----------
st.markdown("---")
st.caption("Make sure your FastAPI server is running and API_BASE is set correctly.")
