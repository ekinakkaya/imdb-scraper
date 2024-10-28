import json
import os
import uuid
import datetime

from imdb_scraper.logger import globalLoggerInstance
from imdb_scraper.config import SESSIONS_FILE


class SessionManager:

    def __init__(self, SESSIONS_FILE=SESSIONS_FILE):
        self.sessions = []
        self.current_session = None
        self.current_session_id = None
        self.logger = globalLoggerInstance
        self.SESSIONS_FILE = SESSIONS_FILE

        self.read_sessions_file_to_memory()
        self.create_sessions_file()


    def create_sessions_file(self):
        if os.path.exists(self.SESSIONS_FILE):
            return

        sessions = []
        self.sessions = sessions
        with open(self.SESSIONS_FILE, "w+") as file:
            json.dump(sessions, file, indent=2)
            self.logger.info("new sessions file has been created")

         
    def read_sessions_file_to_memory(self):
        if os.path.exists(self.SESSIONS_FILE):
            with open(self.SESSIONS_FILE, "r") as file:
                self.sessions = json.load(file)
                json.dumps(self.sessions)
                self.logger.info("sessions file has been read and saved to self.sessions")

            
    def update_sessions_file(self):
        with open(self.SESSIONS_FILE, "w") as file:
            json.dump(self.sessions, file, indent=2)
            self.logger.info("session has been saved to sessions file.")
            
    
    def create_session(self):
        session = {
            "session_id": str(uuid.uuid4()),
            "session_start_time": int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
            "session_end_time": None,
            "session_jobs": []
        }

        self.sessions.append(session)
        self.update_sessions_file()
        self.logger.info("new session has been created and saved to sessions file.")
        return session


    def finish_session(self, session_id):
        session = self.get_session(session_id)

        if session != None:
            session["session_end_time"] = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            
            for i in range(len(self.sessions)):
                if self.sessions[i]["session_id"] == session_id:
                    self.sessions[i] = session

            self.update_sessions_file()


    def get_session(self, id):
        for session in self.sessions:
            #print("comparing " + id + " | " + session["session_id"])
            if session["session_id"] == id:
                return session
        
        return None
        
    
    def get_current_session(self):
        return self.current_session


    def add_job_to_session(self, session_id, job_type, job_data: str):
        session = self.get_session(session_id)

        if session == None:
            return

        print(session)

        job = {
            "job_id": str(uuid.uuid4()),
            "job_start_time": int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
            "job_end_time": None,
            "job_type": job_type,
            "job_data": job_data
        }

        jobs = []
        jobs.append(job)
        session["session_jobs"] = jobs

        for i in range(len(self.sessions)):
            if self.sessions[i]["session_id"] == session_id:
                self.sessions[i]["session_jobs"] = jobs

        self.update_sessions_file()

        return job["job_id"]

    
    def get_job(self, session_id, job_id):

        session = self.get_session(session_id)

        for job in session["session_jobs"]:
            if job["job_id"] == job_id:
                return job
        
        return None
        
    
    def finish_job(self, session_id, job_id):
        job = self.get_job(session_id, job_id)

        if job != None:
            print("lmaoooooo")
            job["job_end_time"] = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            session = self.get_session(session_id)
            for i in range(len(session["session_jobs"])):
                if session["session_jobs"][i]["job_id"] == job_id:
                    session["session_jobs"][i] = job

                    for j in range(len(self.sessions)):
                        if self.sessions[j]["session_id"] == session_id:
                            self.sessions[j] = session

        self.update_sessions_file()