import streamlit as st
import re

# --- Session State Reset ---
if "reset" not in st.session_state:
    st.session_state.reset = False

def reset_inputs():
    st.session_state.inst = ""
    st.session_state.tissue = ""
    st.session_state.sample_id = ""
    st.session_state.subclone = ""
    st.session_state.ext_type = "None"
    st.session_state.ext_value = ""
    st.session_state.reset = True

# --- Helper Functions ---
def is_valid_name(name):
    issues = []
    if len(name) < 6:
        issues.append("Name should be at least 6 characters long.")
    if re.search(r"[^\w\-\(\)]", name):
        issues.append("Only use letters, numbers, dashes (-), and parentheses. Avoid punctuation and special characters.")
    if re.search(r"\b(glioma|melanoma|cancer|tumor)\b", name.lower()):
        issues.append("Name should not be a recognizable word.")
    if re.search(r"\d{2}/\d{2}/\d{4}", name) or re.search(r"[A-Z]{2,}", name):
        issues.append("Avoid using dates or personal initials.")
    if "_" in name:
        issues.append("Underscores are not allowed. Use dashes (-) instead.")
    if re.search(r"[.,;!?]", name):
        issues.append("Avoid punctuation marks.")
    return issues

def format_standard_name(inst, tissue, sample_id, subclone=None):
    base = f"{inst}-{tissue}-{sample_id}"
    if subclone:
        base += f"-{subclone}"
    return base

def append_extension(base_name, ext_type, ext_value):
    if ext_type == "None":
        return base_name
    return f"{base_name} {ext_type}:{ext_value}"

# --- UI ---
st.title("🧬 Cell Line Nomenclature Helper")
st.markdown("Generate and validate standardized cell line names based on Cellosaurus guidelines.")

# Reset button
if st.button("🔄 Reset All Fields"):
    reset_inputs()

# Step 1 Inputs
st.header("Step 1: Define Base Name")
inst = st.text_input("Institution Code (e.g., MOG)", key="inst")
tissue = st.text_input("Tissue/Disease Code (e.g., Lu)", key="tissue")
sample_id = st.text_input("Sample Number (e.g., 113)", key="sample_id")
subclone = st.text_input("Subclone or Clone ID (optional)", key="subclone")

base_name = format_standard_name(inst.strip(), tissue.strip(), sample_id.strip(), subclone.strip() or None)
st.markdown(f"**Generated Base Name**: `{base_name}`")

# Step 2 Extension
st.header("Step 2: Add Extension (Optional)")
ext_type = st.selectbox("Extension Type", ["None", "KO", "KD", "Res", "Added"], key="ext_type")
ext_value = st.text_input(f"{ext_type} target or compound/construct", key="ext_value") if ext_type != "None" else ""

# Final Name
final_name = append_extension(base_name, ext_type, ext_value.strip())
st.markdown("---")
st.subheader("✅ Final Suggested Name")
st.code(final_name)

# Validation
st.markdown("### 🔎 Validation Results")
validation_issues = is_valid_name(final_name)
if validation_issues:
    for issue in validation_issues:
        st.error(issue)
else:
    st.success("Name follows the basic Cellosaurus rules!")
