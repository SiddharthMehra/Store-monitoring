from datetime import timedelta
from pytz import timezone
import numpy as np

def compute_uptime_and_downtime(store_id, start_time, end_time):
    # Get timezone for store
    tz = timezone(Timezone.query.filter_by(store_id=store_id).first().timezone_str)
    
    # Get business hours for store
    business_hours = BusinessHours.query.filter_by(store_id=store_id).all()
    if len(business_hours) == 0:
        # Store is open 24*7
        uptime = (end_time - start_time).total_seconds() / 60
        downtime = 0
        return uptime, downtime
    
    # Compute uptime and downtime for each day of week
    uptime = 0
    downtime = 0
    for day in range(7):
        business_hours_for_day = [bh for bh in business_hours if bh.day_of_week == day]
        if len(business_hours_for_day) == 0:
            # Store is closed on this day
            continue
        start_time_local = business_hours_for_day[0].start_time_local
        end_time_local = business_hours_for_day[0].end_time_local
        for bh in business_hours_for_day[1:]:
            if bh.start_time_local < start_time_local:
                start_time_local
