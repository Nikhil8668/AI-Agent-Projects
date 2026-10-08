import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import log_intake , get_intake_history

@st.cache_resource
def get_agent():
    return WaterIntakeAgent()


if "tracker_started" not in st.session_state :
    st.session_state.tracker_started = False


#Welcome section

if not st.session_state.tracker_started:
    st.title("Welcome to Water Intake Tracker")
    st.markdown("""
    This application helps you track your daily water intake and provides feedback on your hydration status.
    """)

    if st.button("Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()

else:
    st.title("AI Powered Water Intake Tracker")

    #Sidebar Intake Input
    st.sidebar.header("Log your water intake")
    user_id = st.sidebar.text_input("User ID" , value="user_03")
    intake_ml = st.sidebar.number_input("Water Intake (ml)", min_value=0 , step = 100)
    goal_ml = st.sidebar.number_input("Daily Goal (ml)" , min_value=500 , value=2000 , step=250)

    submitted = st.sidebar.button("Submit")

    if submitted and user_id and intake_ml :
            log_intake(user_id , intake_ml)
            st.success(f"Logged {intake_ml}ml for {user_id}")

    #Calculate today's total from the database
    history = get_intake_history(user_id) if user_id else []
    today = datetime.today().strftime("%Y-%m-%d")
    #each row is (id, user_id, intake_ml, date)
    today_total = sum(row[2] for row in history if row[3] == today)

    # Show progress towards the goal
    st.metric("Today's Intake" , f"{today_total} ml" , f"{today_total}/{goal_ml} ml vs goal")
    st.progress(min(today_total / goal_ml , 1.0))

    #Ask the AI about the Total , not just this one entry
    if submitted and user_id and intake_ml :
            try:
                with st.spinner("Getting AI feedback..."):
                      feedback = get_agent().analyze_intake(today_total , goal_ml)
                st.info(f"AI Feedback : {feedback}")
            except Exception as e:
                 st.warning(f"Intake saves , but AI feedback is unvailable right now : {e}")
            

            # agent = WaterIntakeAgent()
            # with st.spinner("Getting AI feedback..."):
            #     feedback = agent.analyze_intake(intake_ml)
            # st.info(f" AI Feedback : {feedback}")

    #Divider
    st.markdown("---")

    # History Section
    st.header("Water Intake History")

    if history:
          dates = [datetime.strptime(row[3], "%Y-%m-%d") for row in history]
          values = [row[2] for row in history]

    # if user_id:

    #     history = get_intake_history(user_id)
    #     if history:
    #         # each row is (id, user_id, intake_ml, date)
    #         dates = [datetime.strptime(row[3], "%Y-%m-%d").date() for row in history]
    #         values = [row[2] for row in history]

          df = pd.DataFrame({"Date": dates, "Intake (ml)": values})
          #Combine multiple entries on the same day into one total
          df = df.groupby("Date" , as_index=False)["Intake (ml)"].sum()

          st.dataframe(df)
          st.line_chart(df , x = "Date" , y = "Intake (ml)")
    else:

        st.warning("No water intake data found . Pls log your intake first.")
