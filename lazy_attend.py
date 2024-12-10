#!/usr/bin/env python3
import json
import requests
from time import sleep
from dotenv import load_dotenv
from datetime import datetime
from logwriter import write_some_log
import pickle
import time
import os

# run this file with cron with interval of 5 minutes
# atau windows task scheduler

# lazy upload periodic json file
now = datetime.now()
formatted_time = now.strftime("%d-%m-%Y")
logger = write_some_log(f'./logs/{formatted_time}.log','lazy_attend.py')
logger.Log_write('Starting')
periodic_post = f'./db/post_periodic/post_periodic{formatted_time}.json'
posted_ids = f'./db/post_periodic/posted{formatted_time}.checkpoint'
# Umur maksimal file post_periodic dan posted adalah 30 hari
max_age_seconds = 30 * 24 * 60 * 60
check_this_week_seconds = 7 * 24 * 60 * 60

load_dotenv()
find_this = os.environ
# JAM_TERAKHIR_MASUK = find_this['JAM_TERAKHIR_MASUK']
# API anshar
API_URL = find_this['API_URL']
API_URL_BACKEND_WA = find_this['API_URL_BACKEND_WA']
EMAIL_ADMIN = find_this['EMAIL_ADMIN']
PASSWORD_ADMIN = find_this['PASSWORD_ADMIN']
# time1 = datetime.strptime(JAM_TERAKHIR_MASUK, "%H:%M:%S")

if not os.path.exists("./db/post_periodic"):
    os.mkdir("./db/post_periodic")

post_periodic_this_week = {}
for file_name in os.listdir('./db/post_periodic'):
    file_path = os.path.join('./db/post_periodic',file_name)
    file_stat = os.stat(file_path)
    current_time = time.time()
    # Calculate the age of the file in seconds
    file_age_seconds = current_time - file_stat.st_mtime
    # Compare the age with the maximum allowed age
    if file_age_seconds > max_age_seconds:
        # File is older than 30 days, so delete it
        os.remove(file_path)
        print(f"{file_path} has been deleted as it's more than 30 days old.")
        logger.Log_write(f'deleted {file_path} - old post_periodic','warning')
        continue
    if file_age_seconds <= check_this_week_seconds:
        # File is generated this week
        extension = file_path.rsplit('.', 1)[1].lower()
        if extension == "json":
            key = file_name.replace("post_periodic","").replace(".json","")
            if post_periodic_this_week.get(key,False):
                post_periodic_this_week[key]["post_periodic"] = file_path
            else:
                post_periodic_this_week[key] = {"post_periodic":file_path}
        if extension == "checkpoint":
            key = file_name.replace("posted","").replace(".checkpoint","")
            if post_periodic_this_week.get(key,False):
                post_periodic_this_week[key]["posted"] = file_path
            else:
                post_periodic_this_week[key] =  {"posted":file_path}
        logger.Log_write(f"{file_name} is generated this week, adding to check for incomplete uploads ...")
# Simulate already posted today, uncomment this
# with open(posted_ids,'wb') as f:
#     pickle.dump([
#         "stu-id-2221",
#         "stu-id-2220",
#         "stu-id-2219",
#         "stu-id-2218"],f)
logger.Log_write(f"{post_periodic_this_week.keys()}")
unique_nis_notif = []
for day_week,post_values in post_periodic_this_week.items():
    # print(f'Jam masuk : {JAM_TERAKHIR_MASUK}')
    post_periodic = post_values.get("post_periodic",False)
    posted = post_values.get("posted",False)
    if post_periodic:
        with open(post_periodic,'r') as json_file :
            payloads:dict = json.load(json_file)
    else:
        # Will happen if for example post_periodic file got deleted but not with posted.checkpoint
        print(f"Something went wrong in this day {day_week} [err post periodic not found]")
        logger.Log_write(f"Something went wrong in this day {day_week} [err post periodic not found] values : {post_values}","error")
        continue
    if posted:
        with open(posted,'rb') as f:
            marked_ids = pickle.load(f)
            logger.Log_write('Opening .checkpoint')
    else:
        marked_ids = []
        logger.Log_write('No checkpoint found')
    complete = False
    cur_marked_id = []
    while not complete:
        for key,value in payloads.items():
            if key in marked_ids:
                continue
            # id_stu = int(value.get("id"))
            id_stu = value.get("id")
            tipe = value.get("tipe")
            time_attend = value.get("time")
            
            # time_date_format = datetime.strptime(time_attend,'%H:%M:%S')
            # Jika waktu masuk siswa > waktu telat maka tipe = TELAT
            # if time_date_format > time1:
            #     print(f'id : {id_stu} tipe : TELAT time : {time_attend}')
            #     logger.Log_write(f'id : {id_stu} tipe : TELAT time : {time_attend}')
            #     tipe = 'TELAT'
            # else:
            print(f'id : {id_stu} tipe : HADIR time : {time_attend}')
            logger.Log_write(f'id : {id_stu} tipe : HADIR time : {time_attend} Key : {key}')
            # post the payload
            r = requests.post(API_URL,{'id':id_stu,'tipe':tipe,'time':time_attend})
            if r.status_code >= 200 and r.status_code <=299:
                marked_ids.append(key)
                cur_marked_id.append(key)
            else:
                print(r.text)
                logger.Log_write(f'Key : {key} got {r.text}','error')

            # Simulate success post, uncomment this
            # marked_ids.append(key)
            # cur_marked_id.append(key)
            if key not in unique_nis_notif:
                print("Sending notif ...")
                current_session = requests.Session()
                logger.Log_write(f"Sending notif once for nis : {key}")
                current_session.post(f"{API_URL_BACKEND_WA}/login",json={'email':EMAIL_ADMIN,'password':PASSWORD_ADMIN})
                r = current_session.post(f"{API_URL_BACKEND_WA}/absensi",json={'nis':id_stu})
                if r.status_code >= 200 and r.status_code <=299:
                    unique_nis_notif.append(key)
                elif r.status_code >= 400 and r.status_code <= 499:
                    print(r.text)
                    logger.Log_write(f'Key : {key} got {r.text} possibly ortu not found','error')
                    unique_nis_notif.append(key)
                else:
                    print(r.text)
                    logger.Log_write(f'Key : {key} got {r.text}','error')
        # Pop id yang telah terkirim
        for xid in marked_ids:
            payloads.pop(xid)

        # Jika selesai semua maka mark complete
        if len(payloads) <= 0:
            complete=True
    if len(cur_marked_id) == 0:
        logger.Log_write(f'Listening [0 marked id] [{post_periodic}]..')
        continue
    print('All posted .. ')
    logger.Log_write('All posted, storing to .checkpoint')
    if posted:
        with open(posted,'wb') as f:
            pickle.dump(marked_ids,f)
    else:
        with open(f"./db/post_periodic/posted{day_week}.checkpoint",'wb') as f:
            pickle.dump(marked_ids,f)
print('Menunggu absen baru .. [lazy_attend.py]')
logger.Log_write('Listening ..')