from studydrive import studydriveapi
from tqdm import tqdm
import os

universityID = 894 # TU Dresden

try:
    file = open("main-account.txt")
    loginData = file.read()
    email = loginData.split(":")[0]
    password = loginData.split(":")[1]
except:
    print("main-account.txt not found")
    print("I'll create the file main-account.txt with your credentials.")
    file = open("main-account.txt", "w+")
    email = input('email: ')
    password = input('Password: ')
    file.write(str(email) + ":" + str(password))
finally:
    file.close()

api = studydriveapi.StudydriveAPI()
api.login(email, password)

# join all courses
myCourseIDs = []
courseIDs = []
for myCourse in api.getMyCourses()["courses"]:
    myCourseIDs.append(myCourse["id"])
for course in api.getUniversityCourses(universityID):
    courseIDs.append(course["course_id"])
for courseID in tqdm(set(courseIDs) - set(myCourseIDs)):
    api.joinCourse(courseID)

# download everything
if not os.path.exists("downloads"):
    os.makedirs("downloads")

for myCourse in tqdm(api.getMyCourses()["courses"]):
    for file in api.getFileListofCourse(myCourse["id"]):
        if file["file_type"] == 60:
            docID = file["file_id"]
            docInfo = api.getDocumentDetails(docID)
            folder = docInfo["file"]["course_name"]
            filename = docInfo["file"]["file_name"]
            if not os.path.exists("downloads/" + folder):
                os.makedirs("downloads/" + folder)
            api.saveDocument(docID, "downloads/{}/{}-{}".format(folder, docID, filename))