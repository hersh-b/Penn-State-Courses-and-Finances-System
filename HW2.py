# HW2
#Hersh Budhwar
#Due Date: 09/25/2020, 11:59PM
"""                                   
### Collaboration Statement:
             
"""
import random


class Course:
    def __init__(self, cid, cname, credits):
        self.cid = cid #Course id
        self.cname = cname #Course name
        self.creds = credits #Credits


    def __str__(self):
        return(str(self.cid) + "(" + str(self.creds) + "): " + str(self.cname)) #CourseID(Credits): Course Name

    __repr__ = __str__

    def __eq__(self, other): # ==
        if isinstance(other, Course):
            if self.cid == other.cid:
                return True
        return False


class Catalog:
    def __init__(self):
        self.courses = {} #Dictionary containing all the courses offered


    @property
    def courseOfferings(self):
        return(self.courses)

    def addCourse(self, cid, cname, credits):
        if cid in self.courses: #Check if already in
            return("Course already added")
        self.courses[cid] = (Course(cid, cname, credits)) #Not already in, so put it in
        return("Course added successfully")


    def removeCourse(self, cid):
        if cid in self.courses: #Check if in catalog
            self.courses.pop(cid) #Remove
            return("Course removed successfully")
        return("Course not found")


class Semester:
    def __init__(self, sem_num):
        self.semnum = sem_num #Semester num
        self.courses = [] #List of courses in semester


    def __str__(self):
        if len(self.courses) == 0: #Return no courses if none in list
            return("No courses")
        return(str(self.courses)[1:-1]) #Gets rid of brackets


    __repr__ = __str__


    def addCourse(self, course):
        if isinstance(course, Course) and isinstance(course.creds, int): #Makes sure course is a valid course
            if course in self.courses:
                return("Course already added")
            self.courses.append(course) #Appends course if it passes all checks
            return
        else:
            return("Invalid course")


    def dropCourse(self, course):
        if isinstance(course, Course): #converts course to just the ID to work with both scenarios
            course = course.cid

        if isinstance(course, str):
            for i in range(len(self.courses)): #Loops through list to find matches
                if self.courses[i].cid == course:
                    self.courses.pop(i) #Removes
                    return
            return("No such course")
        return ("Invalid course")


    @property
    def totalCredits(self):
        total = 0 #
        for i in self.courses:
            total += i.creds
        return(total)


    @property
    def isFullTime(self):
        if self.totalCredits >= 12: #If greater than or equal to 12 credits
            return True
        return False

    
class Loan:
    def __init__(self, amount):
        self.amount = amount #
        self.loan_id = self.__loanID #Get random id


    def __str__(self):
        return(f"Balance: ${self.amount}") #Balance: #Amount

    __repr__ = __str__


    @property
    def __loanID(self):
        self.loan_id = random.randrange(10000,100000)
        return self.loan_id


class Person:
    '''
        >>> p1 = Person('Jason Lee', '204-99-2890')
        >>> p2 = Person('Karen Lee', '247-01-2670')
        >>> p1
        Person(Jason Lee, ***-**-2890)
        >>> p2
        Person(Karen Lee, ***-**-2670)
        >>> p3 = Person('Karen Smith', '247-01-2670')
        >>> p3
        Person(Karen Smith, ***-**-2670)
        >>> p2 == p3
        True
        >>> p1 == p2
        False
    '''

    def __init__(self, name, ssn):
        self.name = name
        self.ssn = ssn


    def __str__(self):
        return(f"Person({self.name}, ***-**-{self.ssn[-4:]})") #Person(Name, ***-**-Last 4 of SSN)


    __repr__ = __str__


    def get_ssn(self):
        return(self.ssn) #Returns full SSN


    def __eq__(self, other):
        if isinstance(other, Person):
            if self.ssn == other.ssn: #Checks equality based on SSN
                return True
        return False


class Staff(Person):
    def __init__(self, name, ssn, supervisor=None):
        super().__init__(name,ssn) #Gets values from person class
        self.supervisor = supervisor


    def __str__(self):
        return(f"Staff({self.name}, {self.id})") #Staff(Name, ID)

    __repr__ = __str__


    @property
    def id(self):
        output = "905"
        initials_list = self.name.split(" ")
        for i in initials_list:
            output += str(i[0:1].lower())
        output += self.ssn[-4:]
        return(output)


    @property   
    def getSupervisor(self):
        return self.supervisor


    def setSupervisor(self, new_supervisor):
        if isinstance(new_supervisor, Staff): #Checks validity
            self.supervisor = new_supervisor #Set
            return("Completed!")
        return()


    def applyHold(self, student):
        if isinstance(student, Student): #Check validity
            student.hold = True
            return("Completed!")
        return


    def removeHold(self, student):
        if isinstance(student, Student): #Check
            student.hold = False
            return ("Completed!")
        return


    def unenrollStudent(self, student):
        if isinstance(student, Student): #Check
            student.active = False
            return ("Completed!")
        return


class Student(Person):
    def __init__(self, name, ssn, year):
        random.seed(1)
        super().__init__(name, ssn) #Initialize with subclass of person for values
        self.year = year
        self.hold = False
        self.active = True
        self.sem = None
        self.semesters = {}
        self.account = self.__createStudentAccount() #Gets a student account in connection


    def __str__(self):
        return(f"Student({self.name}, {self.id}, {self.year})") #Student(Name, ID, Year)


    __repr__ = __str__


    def __createStudentAccount(self):
        if self.active:
            return StudentAccount(self)
        return


    @property
    def id(self):
        output = ""
        initials_list = self.name.split(" ") #Splits into each part of name
        for i in initials_list: #Incase of middle names
            output += str(i[0:1].lower())
        output += self.ssn[-4:] #Gets last four numbers
        return(output)


    def registerSemester(self):
        if not self.hold and self.active:
            self.semesters[len(self.semesters) + 1] = [Semester(len(self.semesters) + 1)] #Makes a semester with a key of 1 and the semester's sem_num = the same
            return
        return("Unsuccessful operation")


    def enrollCourse(self, cid, catalog, semester):
        if self.active and not self.hold:
            classes = catalog.courseOfferings #Shortcut
            if cid in classes: #If offered
                if classes[cid] not in self.semesters[semester][0].courses: #If not already in
                    self.semesters[semester][0].addCourse(classes[cid]) #Add
                    self.account.balance += (self.account.ppc * classes[cid].creds) #add to balance
                    return ("Course added successfully")
                return("Course already enrolled")
            return("Course not found")
        return("Unsuccessful operation")


    def dropCourse(self, cid, semester):
        if self.active and not self.hold:

            classCreds = 0

            for i in range(len(self.semesters[semester][0].courses)): #Gets credits for later
                if self.semesters[semester][0].courses[i].cid == cid:
                    classCreds = self.semesters[semester][0].courses[i].creds

            x = self.semesters[semester][0].dropCourse(cid)
            if x is None:
                self.account.balance -= (self.account.ppc * classCreds) #Adds back balance
                return("Course dropped successfully")
            elif x == "No such course":
                return("Course not found")
            elif x == "Invalid course":
                return x
        return("Unsuccessful operation")


    def getLoan(self, amount):
        if not self.hold and self.active:
            if len(self.semesters) != 0 and self.semesters[1][0].isFullTime: #If full time and has classes
                newLoan = Loan(amount) #Creates loan
                if newLoan.loan_id in self.account.loans: #If loan id already exists
                    self.account.loans[newLoan.loan_id].amount += newLoan.amount
                else: #Loan id is unique
                    self.account.loans[newLoan.loan_id] = newLoan
                return
            return("Not full-time")
        return("Unsuccessful operation")


class StudentAccount:
    def __init__(self, student):
        self.student = student #Initialize
        self.balance = 0
        self.loans = {}
        self.ppc = 1000


    def __str__(self):
        return(f"Name: {self.student.name}\nID: {self.student.id}\nBalance: ${self.balance}") # \n = new line

    __repr__ = __str__


    def makePayment(self, amount, loan_id=None):
        if loan_id is not None: #If using loans
            if loan_id in self.loans: #If loan exists
                if amount <= self.loans[loan_id].amount: #If amount is valid
                    self.balance -= amount
                    self.loans[loan_id].amount -= amount
                    return self.balance
                return(f"Loan Balance: {self.loans[loan_id].amount}")
            return self.loans

        self.balance -= amount #No loan
        return self.balance


    def chargeAccount(self, amount):
        self.balance += amount #Just adds it
        return self.balance


######################################################################


def createStudent(person):
    return Student(person.name, person.get_ssn(), "Freshman") #Gets values from person and puts them into student (+ freshman)

