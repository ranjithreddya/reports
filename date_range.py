from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Max

try:
    res = []

    # Extract start and end time from the request data
    start_in_time = request.data['start_in_time']
    end_in_time = request.data['end_in_time']

    # Convert to datetime objects
    start = datetime.strptime(start_in_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_in_time, "%Y-%m-%d %H:%M:%S")

    # Calculate the total duration in hours
    total_duration = (end - start).total_seconds() / 3600

    # Calculate the number of 24-hour intervals
    interval_hours = 24
    num_intervals = int(total_duration // interval_hours)

    # Iterate over each 24-hour interval
    for i in range(num_intervals + 1):
        interval_start = start + timedelta(hours=i * interval_hours)
        interval_end = min(end, start + timedelta(hours=(i + 1) * interval_hours))

        # Fetch files created within the current interval
        files_within_interval = SFComparePath.objects.filter(created_date__gte=interval_start, created_date__lt=interval_end)
        
        # Sort files within the interval by creation date in descending order
        sorted_files = sorted(files_within_interval, key=lambda x: x.created_date, reverse=True)

        # Find the latest creation date for each JSON file within the current interval
        latest_dates = files_within_interval.values('JSON').annotate(latest_date=Max('created_date'))
        latest_date_dict = {item['JSON']: item['latest_date'] for item in latest_dates}

        # Categorize files within the current interval
        for file in sorted_files:
            latest_date = latest_date_dict.get(file.JSON)
            status = "latest" if latest_date and file.created_date == latest_date else "old"
            
            res.append({
                "req_id": file.req_id,
                "file": file.JSON,
                "created_date": file.created_date.strftime("%Y-%m-%d %H:%M:%S"),  # Include seconds in the format
                "status": status
            })

    print(res)
    return JsonResponse({"detail": res}, status=200)

except Exception as e:
    import traceback
    traceback.print_exc()
    return JsonResponse({"detail": str(e)}, status=500)
