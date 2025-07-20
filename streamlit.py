import streamlit as st
from rag_engine import rag_call  # Import the function from ollama.py

# Title of the App
st.title("AI Cost Optimization Advisor")

# Step 1: Company Overview
st.header("1. Company Overview")
company_name = st.text_input("Company Name (Optional)")
industry = st.selectbox("Industry/Vertical", ["Manufacturing", "Retail", "Healthcare", "Finance", "Other"])
company_size_employees = st.number_input("Number of Employees", min_value=1, step=1)
annual_revenue_range = st.selectbox("Annual Revenue Range", ["<$1M", "$1M-$10M", "$10M-$50M", "$50M-$100M", ">$100M"])
geographical_presence = st.selectbox("Geographical Presence", ["Local", "Regional", "Global"])
primary_products_services = st.text_area("Primary Products/Services", help="Brief description of what the company does.")

# Step 2: Current Processes
st.header("2. Current Processes")
key_processes = st.text_area("List of Key Business Processes", help="e.g., Customer Support, Inventory Management, Sales, Marketing, HR, Accounting, etc.")
process_descriptions = st.text_area("Process Descriptions", help="For each process, briefly describe how it works today. Is it manual, semi-automated, or fully automated?")
process_pain_points = st.text_area("Process Pain Points", help="What challenges do you face in these processes? e.g., Slow turnaround times, High error rates, High labor costs, Lack of scalability, etc.")
task_frequency = st.selectbox("Frequency of Tasks", ["Daily", "Weekly", "Monthly"])

# Step 3: Financial Information
st.header("3. Financial Information")
operational_costs = st.text_area("Annual Operational Costs", help="Breakdown of operational costs by department or process (e.g., Labor, Software, Equipment, etc.).")
automation_spending = st.number_input("Current Automation Spending ($)", min_value=0, step=1)
costliest_processes = st.text_area("Costliest Processes", help="Which processes consume the most resources (time, money, labor)?")
profit_margins = st.text_area("Profit Margins", help="Are there any processes that are particularly low-margin or loss-making?")

# Step 4: Technology Stack
st.header("4. Technology Stack")
current_tools_software = st.text_area("Current Tools and Software", help="What tools/software are you using for key processes? e.g., CRM, ERP, Accounting Software, etc.")
data_availability = st.radio("Data Availability", ["Yes", "No"], help="Do you have access to data related to your processes?")
cloud_vs_onpremise = st.selectbox("Cloud vs On-Premise", ["Cloud-Based", "On-Premise"])
ai_experience = st.radio("AI Experience", ["Yes", "No"], help="Have you implemented AI solutions before? If yes, what were the outcomes?")

# Step 5: Workforce Details
st.header("5. Workforce Details")
employee_roles = st.text_area("Employee Roles", help="What are the primary roles within your organization?")
manual_vs_automated_tasks = st.slider("Percentage of Manual vs Automated Tasks", 0, 100, 50, help="What percentage of tasks are manual vs automated?")
high_turnover_roles = st.text_area("High-Turnover Roles", help="Are there roles with high turnover or high recruitment costs?")
skill_gaps = st.text_area("Skill Gaps", help="Are there any skill gaps in your workforce that AI could address?")

# Step 6: Customer Interaction
st.header("6. Customer Interaction")
customer_support_channels = st.multiselect("Customer Support Channels", ["Phone", "Email", "Chat", "Social Media"])
response_times = st.number_input("Average Response Time (in hours)", min_value=0, step=1)
customer_satisfaction = st.text_area("Customer Satisfaction", help="Are there any recurring complaints or issues from customers?")
sales_funnel_efficiency = st.text_area("Sales Funnel Efficiency", help="How efficient is your sales funnel? e.g., Lead conversion rates, Time to close deals")

# Step 7: Goals and Priorities
st.header("7. Goals and Priorities")
primary_business_goals = st.multiselect("Primary Business Goals", ["Cost Reduction", "Revenue Growth", "Improved Customer Experience", "Scalability"])
automation_goals = st.text_area("Automation Goals", help="What do you hope to achieve with AI automation?")
timeline = st.selectbox("Timeline", ["<3 Months", "3-6 Months", "6-12 Months", ">12 Months"])
budget_constraints = st.number_input("Budget for AI Investments ($)", min_value=0, step=1)

# Step 8: Risk Tolerance
st.header("8. Risk Tolerance")
risk_appetite = st.selectbox("Risk Appetite", ["Open to Experimentation", "Prefer Proven Solutions"])
change_management = st.radio("Change Management", ["Easy", "Difficult"], help="How easy is it to implement changes across your organization?")
regulatory_concerns = st.radio("Regulatory Concerns", ["Yes", "No"], help="Are there any regulatory or compliance requirements that might impact AI adoption?")

# Step 9: Additional Context
st.header("9. Additional Context")
biggest_bottlenecks = st.text_area("Biggest Bottlenecks", help="What are the biggest bottlenecks in your business today?")
success_metrics = st.text_area("Success Metrics", help="How do you measure success for your processes? e.g., Cost per transaction, Error rate, Customer satisfaction score")
competitor_insights = st.text_area("Competitor Insights", help="Are your competitors using AI in ways that give them an edge?")

# Submit Button
if st.button("Submit"):
    # Combine all inputs into a single prompt
    prompt = f"""
    Company Overview:
    - Name: {company_name}
    - Industry: {industry}
    - Size: {company_size_employees} employees, {annual_revenue_range} revenue
    - Geographical Presence: {geographical_presence}
    - Primary Products/Services: {primary_products_services}

    Current Processes:
    - Key Processes: {key_processes}
    - Process Descriptions: {process_descriptions}
    - Pain Points: {process_pain_points}
    - Task Frequency: {task_frequency}

    Financial Information:
    - Operational Costs: {operational_costs}
    - Automation Spending: ${automation_spending}
    - Costliest Processes: {costliest_processes}
    - Profit Margins: {profit_margins}

    Technology Stack:
    - Tools/Software: {current_tools_software}
    - Data Availability: {data_availability}
    - Cloud vs On-Premise: {cloud_vs_onpremise}
    - AI Experience: {ai_experience}

    Workforce Details:
    - Employee Roles: {employee_roles}
    - Manual vs Automated Tasks: {manual_vs_automated_tasks}% manual
    - High-Turnover Roles: {high_turnover_roles}
    - Skill Gaps: {skill_gaps}

    Customer Interaction:
    - Support Channels: {', '.join(customer_support_channels)}
    - Response Times: {response_times} hours
    - Customer Satisfaction: {customer_satisfaction}
    - Sales Funnel Efficiency: {sales_funnel_efficiency}

    Goals and Priorities:
    - Business Goals: {', '.join(primary_business_goals)}
    - Automation Goals: {automation_goals}
    - Timeline: {timeline}
    - Budget: ${budget_constraints}

    Risk Tolerance:
    - Risk Appetite: {risk_appetite}
    - Change Management: {change_management}
    - Regulatory Concerns: {regulatory_concerns}

    Additional Context:
    - Biggest Bottlenecks: {biggest_bottlenecks}
    - Success Metrics: {success_metrics}
    - Competitor Insights: {competitor_insights}

You are a AI cost optimisation agent based on the information collected above suggest an AI strategy to move ahead reducing overall
cost for the company. Also only suggest Lyzr agentic tools and no other tool

    """

    # Call the RAG function from ollama.py
    with st.status("Processing your request...", expanded=True) as status:
        answer = rag_call(prompt)
        status.update(label="✅ Response generated!", state="complete")


    # Display the AI-generated response
    # st.subheader("AI Recommendations:")
    # st.write(answer)

    st.markdown(
        f"""
    <div style="background-color: #008080; padding: 15px; border-radius: 10px; border: 1px solid #d3e3fd;">
        <strong>AI Recommendations:</strong><br><br>{answer}
    </div>
    """,
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div style="background-color: #e02424; padding: 15px; border-radius: 10px; border: 2px solid #a71d2a; text-align: center; margin-top: 25px;">
        <a href="https://www.lyzr.ai/" target="_blank" style="color: white; text-decoration: none; font-weight: bold; font-size: 20px;">
            Visit Lyzr.ai Website
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
