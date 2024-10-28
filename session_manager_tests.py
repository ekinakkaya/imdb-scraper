from imdb_scraper.session_manager import SessionManager

#from imdb_scraper.config import SESSIONS_FILE
SESSIONS_FILE = "./.test_sessions.json"

import os

class InitTest:
    def __init__(self):
        pass

    def test(self):
        if os.path.exists(SESSIONS_FILE):
            os.remove(SESSIONS_FILE)

        self.session_manager = SessionManager(SESSIONS_FILE)

        if os.path.exists(SESSIONS_FILE):
            #os.remove(SESSIONS_FILE)
            return True
        return False
        

class NewSessionTest:
    def __init__(self):
        pass

    def test(self):
        if os.path.exists(SESSIONS_FILE):
            os.remove(SESSIONS_FILE)

        self.session_manager = SessionManager(SESSIONS_FILE)
        if os.path.exists(SESSIONS_FILE):
            session = self.session_manager.create_session()
            if session != None and session["session_id"] != None:
                print(session["session_id"])
                return True
        return False


class AddJobsTest:
    def __init__(self) -> None:
        pass
    
    def test(self):
        if os.path.exists(SESSIONS_FILE):
            os.remove(SESSIONS_FILE)

        self.session_manager = SessionManager(SESSIONS_FILE)
        if os.path.exists(SESSIONS_FILE):
            session = self.session_manager.create_session()

            if session != None and session["session_id"] != None:
                print(session["session_jobs"])
                job_id = self.session_manager.add_job_to_session(session["session_id"], "link_scraping", "2000-01-01,2001-01-01")
                job = self.session_manager.get_job(session["session_id"], job_id)
                print(job)

                if job != None and job["job_type"] == "link_scraping":
                    return True
        return False


class AddAndFinishJobsTest:
    def __init__(self) -> None:
        pass
    
    def test(self):
        if os.path.exists(SESSIONS_FILE):
            os.remove(SESSIONS_FILE)

        self.session_manager = SessionManager(SESSIONS_FILE)
        if os.path.exists(SESSIONS_FILE):
            session = self.session_manager.create_session()

            if session != None and session["session_id"] != None:
                print(session["session_jobs"])
                job_id = self.session_manager.add_job_to_session(session["session_id"], "link_scraping", "2000-01-01,2001-01-01")
                job = self.session_manager.get_job(session["session_id"], job_id)
                self.session_manager.finish_job(session["session_id"], job_id)
                job = self.session_manager.get_job(session["session_id"], job_id)
                print(job)

                if job != None and job["job_type"] == "link_scraping" and job["job_end_time"] != None:
                    return True
        return False


if __name__ == "__main__":
    test_results = []
    
    test_results.append(InitTest().test())
    test_results.append(NewSessionTest().test())
    test_results.append(AddJobsTest().test())
    test_results.append(AddAndFinishJobsTest().test())
    
    os.remove(SESSIONS_FILE)

    for i in range(len(test_results)):
        print("test " + str(i) + " " + str(test_results[i]))
