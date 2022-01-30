from classes.StudydriveAPI import StudydriveAPI
from tqdm import tqdm

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

api = StudydriveAPI(email, password)
api.joinAllCourses(894)
api.sortCourses()

for myCourse in tqdm(api.getMyCourses()["courses"]):
    api.saveAllFilesOfACourse(myCourse["id"])