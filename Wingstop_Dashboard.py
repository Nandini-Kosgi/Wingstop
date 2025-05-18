#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


st.set_page_config(page_title="Wingstop Dashboard", layout="wide")
st.title("🍗 Wingstop Orders Dashboard")


# In[3]:


# Load data
df = pd.read_csv("wingstop_cleaned_data.csv")


# In[7]:


# Filters
st.sidebar.header("Filter")
locations = [col for col in df.columns if col.startswith("location_")]
order_types = df['order_type'].unique() if 'order_type' in df.columns else []

selected_locations = st.sidebar.multiselect("Select Locations", locations, default=locations)
if 'order_type' in df.columns:
    selected_order_types = st.sidebar.multiselect("Select Order Types", order_types, default=order_types)
else:
    selected_order_types = None

# Filter logic
filtered_df = df.copy()
if selected_locations:
    mask = df[selected_locations].any(axis=1)
    filtered_df = filtered_df[mask]

if selected_order_types:
    filtered_df = filtered_df[filtered_df['order_type'].isin(selected_order_types)]



# In[10]:


# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Order Value", f"${filtered_df['order_value_usd'].mean():.2f}")
col3.metric("Peak Hour", filtered_df['order_hour'].mode()[0])


# In[12]:


# Plots
st.subheader("📈 Orders by Hour")
fig, ax = plt.subplots()
sns.countplot(x='order_hour', data=filtered_df, ax=ax)
st.pyplot(fig)


# In[14]:


# Step 1: Reconstruct 'weekday' column from one-hot encoded columns
weekday_cols = [col for col in df.columns if col.startswith('weekday_')]
df['weekday'] = df[weekday_cols].idxmax(axis=1).str.replace('weekday_', '')

# Step 2: Plot - Orders by Weekday
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

fig, ax = plt.subplots()
sns.countplot(x='weekday', data=df, order=[
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday'  # Include only your present one-hot columns
], ax=ax)
plt.xticks(rotation=45)
plt.title("Orders by Weekday")
plt.xlabel("Weekday")
plt.ylabel("Order Count")
plt.tight_layout()
st.pyplot(fig)


# In[15]:


st.subheader("💵 Order Value Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(filtered_df['order_value_usd'], bins=30, kde=True, ax=ax3)
st.pyplot(fig3)


# In[ ]:




