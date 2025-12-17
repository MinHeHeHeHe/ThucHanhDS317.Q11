import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def load_users(path: str = "test_P5.csv") -> pd.DataFrame:
    """Load user activity data from CSV."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file '{path}'.")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_courses(path: str = 'course_info_final_P5.csv') -> pd.DataFrame:
    """Load course metadata from CSV."""
    try:
        df_local = pd.read_csv(path)
        # Sort by user_count descending
        if 'user_count' in df_local.columns:
            df_local = df_local.sort_values(by='user_count', ascending=False).reset_index(drop=True)
        
        # Standardize date format
        if 'class_start' in df_local.columns:
            df_local['class_start'] = pd.to_datetime(df_local['class_start']).dt.strftime('%m/%d/%Y')
        if 'class_end' in df_local.columns:
            df_local['class_end'] = pd.to_datetime(df_local['class_end']).dt.strftime('%m/%d/%Y')
            
        return df_local
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file '{path}'.")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_train_data(path: str = 'train_validate.csv') -> pd.DataFrame:
    """Load training/validation data."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file '{path}'.")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_clean_data(path: str = 'df_clean.csv') -> pd.DataFrame:
    """Load cleaned data for quality analysis."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file '{path}'.")
        return pd.DataFrame()
