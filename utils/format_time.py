from datetime import datetime, timedelta

def format_time(option):
    current_time = datetime.now()  # Thời gian hiện tại

    if option.endswith('s ago'):
            seconds = int(option[:-5]) if option[:-5].isdigit() else 0
            new_time = current_time - timedelta(seconds=seconds)
    if option.endswith('m ago'):
            minutes = int(option[:-5]) if option[:-5].isdigit() else 0
            new_time = current_time - timedelta(minutes=minutes)
            new_time = new_time.replace(second=0)
    elif option.endswith('h ago'):
            hours = int(option[:-5]) if option[:-5].isdigit() else 0
            new_time = current_time - timedelta(hours=hours)
            new_time = new_time.replace(minute=0, second=0)
    elif option.endswith('d ago'):
            days = int(option[:-5]) if option[:-5].isdigit() else 0
            new_time = current_time - timedelta(days=days)
            new_time = new_time.replace(hour=0, minute=0, second=0)
    elif option.endswith('w ago'):
            weeks = int(option[:-5]) if option[:-5].isdigit() else 0
            new_time = current_time - timedelta(weeks=weeks)
            new_time = new_time.replace(hour=0, minute=0, second=0)
    else:
            try:
                if '-' in option:
                    new_time = datetime.strptime(option, '%m-%d')
                    new_time = new_time.replace(year=current_time.year)
                else:
                    new_time = datetime.strptime(option, '%m-%d-%Y')
            except ValueError:
                pass
        
        # Định dạng thời gian mới
    return new_time

# Thử nghiệm hàm
time_option = '22s ago'
a = format_time(time_option)
print(a)