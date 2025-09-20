import streamlit as st
from omr_core import evaluate_omr
import pandas as pd
import style

# Apply custom style
style.set_page_style()
style.app_header("📝 OMR Evaluation System")

# Tabs for better layout
tabs = st.tabs(["Evaluate Sheet", "Batch Results", "Calibration/Preview"])

# Sidebar configuration
st.sidebar.header("Configuration")
sheet_versions = st.sidebar.selectbox("Sheet versions used in exam", options=[1,2,3,4], index=0)

# Upload Answer Key as Image
uploaded_key_img = st.sidebar.file_uploader("Upload Answer Key Sheet (Image)", type=["jpg","png","jpeg"])
key_answers = {}
if uploaded_key_img:
    key_answers = evaluate_omr(uploaded_key_img)
    st.sidebar.success("Answer key detected from image ✅")

version_selected = f"version_{sheet_versions}"

# ===========================
# Tab 1: Evaluate Sheet
# ===========================
with tabs[0]:
    st.subheader("Upload Student OMR Sheets")
    uploaded_files = st.file_uploader("Upload one or more OMR sheets (JPG/PNG)", accept_multiple_files=True)
    
    if st.button("Evaluate Sheets"):
        if not uploaded_files:
            st.warning("Please upload at least one student sheet.")
        elif not key_answers:
            st.warning("Please upload the answer key sheet image first.")
        else:
            results_list = []
            for f in uploaded_files:
                detected_answers = evaluate_omr(f)
                
                # Scoring
                total_score = 0
                per_subject = {}
                subjects = ["Math","Physics","Chemistry","English","CS"]  # Adjust per your syllabus
                questions_per_subject = 20
                qbase = 1
                for subj in subjects:
                    correct = 0
                    for q in range(qbase, qbase+questions_per_subject):
                        ans = detected_answers.get(str(q), "")
                        key_ans = key_answers.get(str(q), "")
                        if ans == key_ans:
                            correct += 1
                    score = round((correct/questions_per_subject)*20,2)
                    per_subject[subj] = {"correct": correct, "score": score}
                    total_score += score
                    qbase += questions_per_subject
                total_score = round(total_score,2)
                per_subject['TOTAL'] = {"score": total_score}
                results_list.append({"file": f.name, "version": version_selected, "per_subject": per_subject})
            
            # Display results with style
            for res in results_list:
                st.markdown(f"### Results for {res['file']}")
                for subj, data in res['per_subject'].items():
                    style.score_card(subj, data['score'])
                    if subj != "TOTAL":
                        style.progress_bar(data['score'])
            
            # Download CSV
            df_rows = []
            for res in results_list:
                row = {"file": res['file'], "version": res['version'], "total_score": res['per_subject']['TOTAL']['score']}
                for subj, data in res['per_subject'].items():
                    if subj == "TOTAL": continue
                    row[f"{subj}_score"] = data['score']
                    row[f"{subj}_correct"] = data['correct']
                df_rows.append(row)
            df = pd.DataFrame(df_rows)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CSV", csv, "results.csv", "text/csv")

# ===========================
# Tab 2: Batch Results (Optional)
# ===========================
with tabs[1]:
    st.info("Batch Results will appear here after evaluation.")

# ===========================
# Tab 3: Calibration/Preview
# ===========================
with tabs[2]:
    st.info("You can preview detected bubbles here (future enhancement).")
