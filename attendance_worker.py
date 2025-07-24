from lazy_attend_utils import MyUtils
from logwriter import write_some_log
from dotenv import load_dotenv
from datetime import datetime
import requests
import sqlite3
import time
import os

logger = write_some_log(f'./logs/{datetime.now().strftime("%d-%m-%Y")}.log','lazy_attend.py')
logger.Log_write('Starting')

class LazyAttend:
    def __init__(self):
        self.db_path = "attendance.db"
        load_dotenv()
        self.API_URL_ERINA_BASE = os.environ.get("API_URL_ERINA_BASE", None)
        self.API_URL_BACKEND_WA_BASE = os.environ.get("API_URL_BACKEND_WA_BASE", None)
        self.USERNAME_WA_GATEWAY = os.environ.get("USERNAME_WA_GATEWAY", None)
        self.PASSWORD_WA_GATEWAY = os.environ.get("PASSWORD_WA_GATEWAY", None)
        if not all([self.API_URL_ERINA_BASE, self.API_URL_BACKEND_WA_BASE, self.USERNAME_WA_GATEWAY, self.PASSWORD_WA_GATEWAY]):
            print("Missing one or more required environment variables")
            logger.Log_write("Missing one or more required environment variables", "error")
            raise RuntimeError("Missing .env configuration")
        self.lazy_attend_util = MyUtils()
        self.session = None
        self.setup_session()

    def setup_session(self):
        logger.Log_write('Setting up session')
        self.session = requests.Session()
        url = f"{self.API_URL_BACKEND_WA_BASE}login"
        is_expired_access_token = self.lazy_attend_util.is_expired()
        if not is_expired_access_token:
            logger.Log_write('Getting access token')
            print(">> Getting access token ...")
            self.lazy_attend_util.login_and_save_new_access_token(url, self.USERNAME_WA_GATEWAY, self.PASSWORD_WA_GATEWAY)
            prev_access_token = self.lazy_attend_util.load_previous_access_token()
            self.session.headers.update({"Authorization": f"Bearer {prev_access_token}"})
        else:
            logger.Log_write('Loaded saved access token')
            print(">> Loaded saved access token ...")
            prev_access_token = self.lazy_attend_util.load_previous_access_token()
            self.session.headers.update({"Authorization": f"Bearer {prev_access_token}"})

    def get_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def send_to_erina(self, payload:dict):
        print("Sending absensi ...")
        logger.Log_write(f"Sending absensi payload : {payload}")
        url = f"{self.API_URL_ERINA_BASE}absensi/hadir"
        try:
            r = self.session.post(url=url, json=payload, timeout=10)
            if r.status_code == 200 and r.status_code <=299:
                return True
            else:
                print(r.text)
                logger.Log_write(f'Payload erina : {payload} got {r.text}',"error")
                return False
        except Exception as e:
            print(f"Error sending data for payload erina -> {payload} : {e}")
            logger.Log_write(f"Error sending data for payload erina -> {payload} : {e}","error")
            return False

    def send_to_wa_gateway(self, payload:dict):
        print("Sending notif ...")
        logger.Log_write(f"Sending notif payload : {payload}")
        url = f"{self.API_URL_BACKEND_WA_BASE}attendances"
        try:
            r = self.session.post(url=url, json=payload, timeout=10)
            if r.status_code == 200 and r.status_code <=299:
                return True
            else:
                print(r.text)
                logger.Log_write(f'Payload wa-gateway : {payload} got {r.text}',"error")
                return False
        except Exception as e:
            print(f"Error sending data for payload wa-gateway -> {payload} : {e}")
            logger.Log_write(f"Error sending data for payload wa-gateway -> {payload} : {e}","error")
            return False

    def run(self):
        while True:
            try:
                logger.Log_write('Getting db')
                conn = self.get_db()
                c = conn.cursor()

                now = datetime.now()
                current_date = now.strftime("%Y-%m-%d")
                is_sent = "no"

                logger.Log_write('Getting unsent attendance')
                c.execute("SELECT * FROM attendance WHERE is_sent = ? AND date = ?", (is_sent, current_date))
                unsent_rows = c.fetchall()

                for row in unsent_rows:
                    tipe_kehadiran = "HADIR"
                    payload = {
                        "base": {
                            "nis": row["nis"],
                            "student_id": row["student_id"],
                            "student_name": row["student_name"],
                            "class_id": row["class_id"],
                            "timestamp": row["timestamp"],
                            "date": row["date"]
                        },
                        "erina": {
                            "id": row["student_id"],
                            "time": row["timestamp"],
                            "tipe": tipe_kehadiran
                        },
                        "wa-gateway": {
                            "erina_class_id": row["class_id"],
                            "erina_user_id": row["student_id"],
                            "attendance_name": row["student_name"],
                            "type": tipe_kehadiran
                        }
                    }

                    print(f'Sending : {payload}')
                    logger.Log_write(f'Sending : {payload}')

                    is_sent_erina = self.send_to_erina(payload=payload.get("erina"))
                    if is_sent_erina:
                        c.execute("UPDATE attendance SET is_sent = 'yes' WHERE id = ?", (row["id"],))
                        conn.commit()
                        print("Attendance sent")
                        logger.Log_write(f'Attendance sent')
                    is_sent_wa_gateway = self.send_to_wa_gateway(payload=payload.get("wa-gateway"))
                    if is_sent_wa_gateway:
                        print("Notif sent")
                        logger.Log_write(f'Notif sent')

            except Exception as e:
                print(f"Worker error : {e}")
                logger.Log_write(f"Worker error : {e}","error")
            print('Menunggu absen baru .. [attendance_worker.py]')
            logger.Log_write('Listening ..')
            time.sleep(3) # wait 3 seconds before checking again

def lazy_attend_worker():
    lazy_attend = LazyAttend()
    lazy_attend.run()

if __name__ == "__main__":
    lazy_attend_worker()