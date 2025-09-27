# import os
# from supabase import create_client

# supabase_url = os.getenv("SUPABASE_URL")
# supabase_key = os.getenv("SUPABASE_KEY")

# supabase = create_client(supabase_url, supabase_key)


# Fix for streamlit not finding creds

import os

try:
    import streamlit as st
    supabase_url = st.secrets.get("SUPABASE_URL")  # Streamlit secrets
    supabase_key = st.secrets.get("SUPABASE_KEY")
except ModuleNotFoundError:
    supabase_url = None
    supabase_key = None

# fallback to environment variables if not running in Streamlit
if not supabase_url:
    supabase_url = os.getenv("SUPABASE_URL")
if not supabase_key:
    supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY.")

from supabase import create_client

supabase = create_client(supabase_url, supabase_key)

