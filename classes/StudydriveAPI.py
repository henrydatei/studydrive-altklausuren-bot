import requests
import os

class StudydriveAPI:
    token = None
    baseurl = "https://api.studydrive.net/"

    def __init__(self, username, password):
        self.token = self.login(username, password)

    def login(self, user, passwd):
        param = {"client_id": 4,
            "client_secret": "nmGaT4rJ3VVGQXu75ymi5Cu5bdqb3tFnkWw9f1IX",
            "grant_type":"password",
            "username": user,
            "password": passwd}
        req = requests.post('{}oauth/token'.format(self.baseurl), data=param)
        req.raise_for_status()
        return req.json()['access_token']

    def saveDocument(self, docID, filename): # from https://stackoverflow.com/questions/56950987/download-file-from-url-and-save-it-in-a-folder-python
        # create folder for downloads
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        headers = {"authorization": "Bearer " + self.token}
        req = requests.get('{}api/app/v1/documents/{}/download'.format(self.baseurl, docID), headers = headers, stream = True)

        if req.ok:
            with open("downloads/" + filename, "wb") as f:
                for chunk in req.iter_content(chunk_size = 1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(req.status_code, req.text))

    def uploadDocument(self, klausur):
        # get upload hash
        headers = {"authorization": "Bearer " + self.token}
        req = requests.post('{}api/app/v1/documents/upload/init'.format(self.baseurl), headers = headers)
        req.raise_for_status()
        hash = req.json()["upload_hash"]

        # upload
        file = open("downloads/" + klausur.name, "rb")
        parameters = {'name': klausur.name, 
            'description': klausur.description, 
            'professor': klausur.professor, 
            'course_id': klausur.courseID, 
            'semester_id': klausur.semesterID, 
            'type': klausur.type, 
            'anonymous': 1, 
            'self_made': 0, 
            'upload_hash': hash}
        files = {'file': file}
        req = requests.post('{}api/app/v1/documents/upload'.format(self.baseurl), headers = headers, data = parameters, files = files)
        # print(req.json())

        # finalize
        parameters = {'upload_hash': hash}
        req = requests.post('{}api/app/v1/documents/upload/{}/finalize'.format(self.baseurl, hash), headers = headers, params = parameters)
        return req.json()

    def joinCourse(self, courseID):
        headers = {"authorization": "Bearer " + self.token}
        req = requests.post('{}api/app/v1/courses/{}/join'.format(self.baseurl, courseID), headers = headers)
        return req.json()

    def joinAllCourses(self, universityID):
        headers = {"authorization": "Bearer " + self.token}
        req = requests.get('{}/api/app/v1/universities/{}/courses'.format(self.baseurl, universityID), headers = headers)
        courses = req.json()
        for course in courses:
            self.joinCourse(course["course_id"])

    def getMyCourses(self):
        headers = {"authorization": "Bearer " + self.token}
        req = requests.get('{}api/app/v1/users/left_sidebar'.format(self.baseurl), headers = headers)
        req.raise_for_status()
        return req.json()

    def setCourseOrder(self, courses):
        headers = {"authorization": "Bearer " + self.token}
        req = requests.post('{}api/app/v1/community/order'.format(self.baseurl), headers = headers, data = {'context':'course', 'ids[]': courses})
        req.raise_for_status()
        return req.json()

    def sortCourses(self):
        list = []
        ids = []
        courses = self.getMyCourses()
        for courseData in courses['courses']:
            courseID = courseData['course_id']
            courseName = courseData['course_name']
            list.append([courseID,courseName])
        sortedList = sorted(list, key = lambda tup: tup[1])
        for courseData in sortedList:
            id = courseData[0]
            ids.append(id)
        print(self.setCourseOrder(ids[::-1]))

    def getDocumentInformation(self, docID):
        pass

    def isDocumentUp(self, docID):
        pass

    def getMyCourses(self):
        headers = {"authorization": "Bearer " + self.token}
        req = requests.get('{}api/app/v1/myself/courses'.format(self.baseurl), headers = headers)
        req.raise_for_status()
        return req.json()

    def saveAllFilesOfACourse(self, courseID, type = 30): # 30 für Altklausur?
        pass
