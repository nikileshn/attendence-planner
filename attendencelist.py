import streamlit as st
import math

st.set_page_config(page_title="CVV Attendance", page_icon="🎓")

st.title("🎓 CVV Attendance Planner")
st.write("Calculate exactly how many classes you can skip or need to attend to maintain your target attendance.")

goal = st.slider("🎯 Set Your Attendance Goal (%)", min_value=65, max_value=100, value=65, step=1)
goal_fraction = goal / 100

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    total_classes = st.number_input("Total Classes", min_value=1, value=40, step=1)
with col2:
    attended_classes = st.number_input("Classes Attended", min_value=0, value=30, step=1)

if attended_classes > total_classes:
    st.error("⚠️ Error: You cannot attend more classes than the total!")

else:
    current_percentage = (attended_classes / total_classes) * 100
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Current Attendance", value=f"{current_percentage:.2f}%")
    with col_b:
        st.metric(label="Your Goal", value=f"{goal}%")

    st.progress(min(current_percentage / 100, 1.0))

    if current_percentage >= goal:
        skippable_classes = math.floor((attended_classes - goal_fraction * total_classes) / goal_fraction)
        
        gap = current_percentage - goal
        if gap <= 3:
            st.warning(f"⚠️ YOU ARE SAFE — but barely! Only {skippable_classes} class(es) left before dropping below {goal}%.")
        else:
            st.success(f"✅ YOU ARE SAFE!")
        
        st.write(f"You can skip the next **{skippable_classes} class(es)** and still stay at or above **{goal}%**.")

    else:
        needed_classes = math.ceil(
            (goal_fraction * total_classes - attended_classes) / (1 - goal_fraction)
        )
        
        st.error(f"🚨 ATTENDANCE LOW!")
        st.write(f"You need to attend the next **{needed_classes} class(es)** straight to hit **{goal}%**.")

    st.markdown("---")
    st.subheader("📅 What-If Simulator")
    st.write("See how future classes affect your attendance.")

    future_total = st.number_input("Upcoming Classes", min_value=0, value=10, step=1)
    future_attend = st.number_input("How Many Will You Attend?", min_value=0, max_value=int(future_total) if future_total > 0 else 0, value=int(future_total), step=1)

    if future_total > 0:
        new_total = total_classes + future_total
        new_attended = attended_classes + future_attend
        new_pct = (new_attended / new_total) * 100

        st.metric(
            label="Projected Attendance",
            value=f"{new_pct:.2f}%",
            delta=f"{new_pct - current_percentage:+.2f}% vs now"
        )

        if new_pct >= goal:
            st.success(f"✅ You'll meet your {goal}% goal!")
        else:
            still_needed = math.ceil(
                (goal_fraction * new_total - new_attended) / (1 - goal_fraction)
            )
            st.error(f"🚨 Still short! Attend {still_needed} more class(es) on top of this to reach {goal}%.")

st.markdown("---")
st.markdown("Built with pure Python by [Nikilesh N](www.linkedin.com/in/nikilesh-n/) 🎓")
