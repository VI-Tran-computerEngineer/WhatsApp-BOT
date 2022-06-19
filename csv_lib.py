import csv
from datetime import datetime


def check_available_timestamp(send_timestamp):
    current_timestamp = round(datetime.now().timestamp())
    if send_timestamp < current_timestamp - 600:
        return "overtime"
    elif current_timestamp + 60 >= send_timestamp >= current_timestamp - 660:
        return "ontime"

    return None


def get_data_from_csv(csv_file_name):
    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        send_msgs_info = {}
        phone_numbers = []
        first_row = True
        datetime_format = "%d/%m/%Y %H:%M:%S"
        for row in csv_reader:
            if first_row:
                row_processed = [cell for cell in row[3:] if cell != '']
                phone_numbers.extend(row_processed)
                for phone_number in phone_numbers:
                    send_msgs_info[phone_number] = []
                first_row = False
            else:
                cell_idx = 0
                for cell in row[3:]:
                    send_time = datetime.strptime(
                        row[0]+' '+row[1], datetime_format)
                    send_timestamp = round(datetime.timestamp(send_time))
                    if (row[cell_idx+3] != ""):
                        check_available_timestamp(send_timestamp) == "overtime"
                        continue
                    sent_or_not = False
                    if check_available_timestamp(send_timestamp) == "overtime":
                        sent_or_not = True
                    send_msgs_info[phone_numbers[cell_idx]].append({
                        "time": send_timestamp,
                        "body": row[2],
                        "sent": sent_or_not,
                    })
                    cell_idx += 1
    dict_keys = [list(send_msgs_info)[0]]
    for key in dict_keys:
        if len(send_msgs_info[key]) == 0:
            del send_msgs_info[key]
    return send_msgs_info


def save_msg_to_csv(csv_file_name, phone_number, sent_msg, recved_msg):
    with open(csv_file_name) as csv_file:
        reader = csv.reader(csv_file)
        readerlist = []
        for row in reader:
            if row[0] == '':
                continue
            readerlist.append(row)
    with open(csv_file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        first_row = True
        column_idx = None
        for row in readerlist:
            if first_row:
                column_idx = row.index(phone_number)
                first_row = False
            elif row[2] == sent_msg:
                row[column_idx] = recved_msg
            writer.writerow(row)
        csv_file.close()
