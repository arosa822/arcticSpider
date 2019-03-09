from app import db
from app.models import User,Resort,Conditions

def addUser(name,email):
    u = User(username= name,email = email)
    print(User)
    print(u)
    return

def addResort(location):
    r = Resort(location = location)
    print(Resort)
    print(r)

def main():
    addUser('alex','alex.com')
    addResort('keystone')
    return

if __name__=='__main__':
    main()
