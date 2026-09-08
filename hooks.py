# In hooks.py
import datetime

if "date" in meta:
    date_str = str(meta["date"]) # e.g. "2024-05-15"
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        # Outputs: "2024-05 (May)"
        formatted_month = dt.strftime("%Y-%m (%B)")
        filters.append(f'<span data-pagefind-filter="Date" style="display:none;">{formatted_month}</span>')
    except ValueError:
        pass