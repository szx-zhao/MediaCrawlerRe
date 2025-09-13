import datetime

timestamp = 1750990811

now_utc = datetime.datetime.now(datetime.timezone.utc)
comment_time_utc = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

delta = now_utc - comment_time_utc
total_days = delta.days + delta.seconds / 86400


print(f"抓取时间: {comment_time_utc}")
print(f"时间差: {total_days}")
