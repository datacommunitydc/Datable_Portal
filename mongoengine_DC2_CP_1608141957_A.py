#!/usr/bin/env python

print "\n===== \n"
from mongoengine import *
import datetime
import csv

connect('DC2_CP')

class General_info(Document):
    # Datable Candidate Application, Section 1, "Required's", part 1

    #"First Name"
    first_name = StringField(required=True, 
                             default='')
    #"Last Name"
    last_name = StringField(required=True,
                            default='')
    #"Email Address"
    email = StringField(required=True,
                        default='')   
                        
    meta = {'allow_inheritance': True}

class Social(Document):
    # Datable Candidate Application, Section 1, "Required's", part 2
    
    #"Github Profile URL"    
    github_url = StringField(required=True,
                             default='')
    #"LinkedIn Profile URL"
    linkedin_url = StringField(required=True,
                               default='')
    #"Meetup Profile URL"
    meetup_url = StringField(required=True,
                             default='')
    #"Twitter Profile URL"
    twitter_url = StringField(required=True,
                              default='')
                              
    meta = {'allow_inheritance': True}                            

class Professional_outlook(Document):
    # Datable Candidate Application, Section 1, "Required's", part 3

    #"Are you currently looking for a position or willing to be contacted about positions?"
    is_open_to_positions = BooleanField(required=True,
                                        default=False)
    #"What Degrees have you earned?"
    degrees = ListField(StringField(required=True),
                        default=list)
    #"Are you a US Citizen?"
    is_citizen = BooleanField(required=True,
                              default=False)
    #"Do you have a Security Clearance?"
    security_clearance = ListField(StringField(required=True),
                                   default=list)
    #"Data Community DC Events Attended"
    dc2_events_attanded = ListField(StringField(required=True),
                                    default=list)
    #"Favorite Data Community DC Event & Speaker"
    favorite_dc2_eventAndSpeaker = StringField(required=True,
                                               default='')
    
    meta = {'allow_inheritance': True}
    
class Community(Document):
    # Datable Candidate Application, Section 2, "Community Engagement"
    
    #"Are you a community organizer?"
    is_comm_organizer = BooleanField(required=True, 
                                     default=False)
    #"Do you volunteer for others' community events?"
    is_volunteer_for_other_comm_events = BooleanField(required=True,
                                                      default=False)
    #"Have you ever presented your work at an event?"
    is_presenter_of_own_work_at_event = BooleanField(required=True, 
                                                     default=False)
    #"Where have you presented?"
    where_presented = StringField()
    #"Have you provided successful introductions to another community organizer?"
    is_provider_of_successful_intro_to_comm_org = BooleanField(required=True, 
                                                               default=False)
    
    meta = {'allow_inheritance': True}

class Experience(Document):
    # Datable Candidate Application, Section 3, "Experience"

    #"What's your experience level?"
    experience_level = StringField(required=True,
                                   max_length=1, 
                                   choices=(('E', 'Entry 0 years'),
                                            ('J', 'Junior 1-3 years'), 
                                            ('M', 'Mid-level 3-5 years'),
                                            ('S', 'Senior 5+ years'),
                                            ('V', 'Veteran 10+ years')),
                                            default='E')
    #"What sectors have you worked in?"
    sectors = ListField(StringField(required=True),
                                    default=list)
    #"Have you ever founded a startup, or joined a startup in the early stages, that achieved market traction or better?"
    is_startup_exp = BooleanField(required=True,
                                  default=False)
    #"Have you ever been involved with BD, sales, or managed a client relationship?"
    is_BD_sales_or_client_relationships = BooleanField(required=True, 
                                                       default=False)
    #"Have you accepted or would you accept freelance work?"
    is_freelance = BooleanField(required=True,
                                default=False)
    #"Have you managed teams before?"
    team_manage_exp = ListField(StringField(required=True),
                                            default=list)
    
    meta = {'allow_inheritance': True}

class Background(Document):
    # Datable Candidate Application, Section 4, "Data Practitioner Background"

    #"Please describe three data science or data related projects..."
    three_data_projects = StringField(required=True,
                                      default='') 
    #"What Data Science techniques have you worked with?"
    data_science_techniques = ListField(StringField(required=True),
                                        default=list)
    #"When was the last time you committed code?"
    last_time_committed_code = StringField(required=True,
                                           max_length=5, 
                                           choices=(('Today', 'Today'),
                                                    ('1Week', 'Within last week'), 
                                                    ('1Mnth', 'Within last month'),
                                                    ('6Mnth', 'Within last 6 months'),
                                                    ('None', 'Not committed to coding')),
                                                    default='None')
    #"What languages & libraries do you use?"
    languages_and_libraries = ListField(StringField(required=True),
                                        default=list)
    
    meta = {'allow_inheritance': True}

class About_You(Document):
    # Datable Candidate Application, Section 5, "About You"

    #"Please Provide Any Links to Personal Websites, Resume, Portfolios, etc."
    links_to_personals = ListField(URLField(required=True),
                                   default=list)
    #"Describe yourself in one sentence."
    self_description = StringField(required=True,
                                   default='')  
    
    meta = {'allow_inheritance': True}

class Old(Document):
    # Unique fields from Google database "Scrubbed Candidate Pool - Candidate_Pool"
    ## Note that any duplicates from "Datable Candidate Application" fields in other classes were removed in 'Old` class.

    #"Candidate #"
    candidate_num = StringField(required=True,
                                default='')
    #"Startup and/or Business Experience?"
    startup_and_or_business_exp = StringField(required=True,
                                              default='')
    #"How have you worked in/with teams?"
    have_worked_in_and_or_with_teams = StringField(required=True,
                                                   default='')                                          

    meta = {'allow_inheritance': True}

# Users
class User(General_info, 
           Social, 
           Professional_outlook, 
           Community, 
           Experience, 
           Background, 
           About_You,
           Old):

    user_id = StringField(required=True,
                          default='')
    notes = StringField(required=True,
                          default='')
    
    # User Stats
    created_at = DateTimeField(default=datetime.datetime.now)
    total_log_ins = IntField(default=0)


def test():
    ## Test adding a user 1
    bob = User(email='bob@example.com')
    bob.first_name = 'Bob'
    bob.last_name = 'Ross'
    bob.is_citizen = True
    bob.save()
    bob.degrees = ["B.S."]
    bob.save()
    bob.degrees.append("M.S.")
    bob.save()
    bob.last_time_committed_code = "Today"
    bob.save()
    
    ## Test adding a user 2
    daffy = User(email='daffy@example.com', 
                first_name='Daffy', 
                last_name='Duck').save()


def test_csv():
    with open('test_candidates160814_trunc4cx10r.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, 
                                delimiter=',',
                                skipinitialspace=True)
        row_id = 0
        for row in spamreader:
            ## header row
            if row_id == 0:
                #print "row_id", row_id
                for i in row:
                    if i == "Candidate #": #<X>
                        index__candidate_num = row.index(i)
                    if i == "When was the last time you committed code?": #<X>
                        index__last_time_committed_code = row.index(i)
                    if i == "What languages & libraries do you use?": #<X>
                        index__languages_and_libraries = row.index(i)
                        #print "index__languages_and_libraries", index__languages_and_libraries
                    if i == "What's your experience level?": #<X>
                        index__experience_level = row.index(i)
                        #print "index__experience_level", index__experience_level
                    if i == "What Data Science techniques have you worked with?":
                        index__data_science_techniques = row.index(i)
                    if i == "Have you managed teams before?":
                        index__team_manage_exp = row.index(i)
                    if i == "Do you have a Security Clearance?":
                        index__security_clearance = row.index(i)
                    if i == "What Degrees have you earned?":
                        index__degrees = row.index(i)
                    if i == """ "Please describe three data science or data related projects you've worked on in the last three years. These can be features of larger projects, consulting projects, classified work described generally, or open source contributions." """:
                        index__three_data_projects = row.index(i)
                    if i == "Data Community DC Events Attended":
                        index__dc2_events_attanded = row.index(i)
                    if i == "Favorite Data Community DC Event & Speaker":
                        index__favorite_dc2_eventAndSpeaker = row.index(i)
                    if i == "Describe yourself in one sentence.":
                        index__self_description = row.index(i)
                    if i == "Have you ever presented your work at an event?":
                        index__is_presenter_of_own_work_at_event = row.index(i)
                    if i == "Where have you presented?":
                        index__where_presented = row.index(i)
                    if i == "Startup and/or Business Experience?": 
                        index__startup_and_or_business_exp = row.index(i)
                    if i == "What sectors have you worked in?":
                        index__sectors = row.index(i)
                    if i == "How have you worked in/with teams?": 
                        index__have_worked_in_and_or_with_teams = row.index(i)
                    if i == "Have you accepted or would you accept freelance work?":
                        index__is_freelance = row.index(i)
                    if i == """ "Have you ever founded a startup, or joined a startup in the early stages, that achieved market traction or better?" """:
                        index__is_startup_exp = row.index(i)
                    if i == """ "Have you ever been involved with BD, sales, or managed a client relationship?" """:
                        index__is_BD_sales_or_client_relationships = row.index(i)
                    if i == "Are you a community organizer?":
                        index__is_comm_organizer = row.index(i)
                    if i == "Do you volunteer for others' community events?":
                        index__is_volunteer_for_other_comm_events = row.index(i)
                    if i == "Have you provided successful introductions to another community organizer?":
                        index__is_provider_of_successful_intro_to_comm_org = row.index(i)
                    if i == "Are you a US Citizen?":
                        index__is_citizen = row.index(i)
                row_id += 1
            ## move to other rows in csv
            else:
                #print "row_id", row_id
                User(candidate_num = row[index__candidate_num],
                            last_time_committed_code = convert__last_time_committed_code(row[index__last_time_committed_code]),
                            languages_and_libraries = convert__languages_and_libraries(row[index__languages_and_libraries]),
                            experience_level = convert__experience_level(row[index__experience_level])).save()
                            #<> complete other `convert` functions
                row_id += 1


def convert__last_time_committed_code(string):
    if string == "Today" or string == "Today!":
        return "Today"
    elif string == "Within the Last week":
        return "1Week"
    elif string == "Within the Last month" or string == "2 weeks ago":
        return "1Mnth"
    elif string == "Within last 6 months" or string == "Within the last 6 months":
        return "6Mnth"
    elif string == "I'm not committed to coding" or string == 'Not committed to coding':
        return "None"
    else:
        return "None"

def convert__languages_and_libraries(string):
    return [x.strip() for x in string.split(',')]

def convert__experience_level(string):
    if string == "Entry 0 years" or string == "Entry Level (0 years)":
        return "E"
    elif string == "Junior 1-3 years" or string == "Junior (1-3 years)":
        return "J"
    elif string == "Mid-level 3-5 years" or string == "Mid-Level (3-5 years)":
        return "M"
    elif string == "Senior 5+ years" or string == "Senior (5+ years)":
        return "S"
    elif string == "Veteran 10+ years" or string == 'Veteran (10+ years)':
        return "V"
    else:
        return "E"


def test_query():
    print "function test_query...\n"
    
    
    users_1Week = User.objects(last_time_committed_code = "1Week")
    print 'len(users_1Week) :', len(users_1Week), "\n"
    
    for user in users_1Week:
        print "user.candidate_num", user.candidate_num
        print "user.experience_level", user.experience_level
        print "user.languages_and_libraries", user.languages_and_libraries
        print "\n"



def main():
    #test()
    User.drop_collection() #clear `User` collection
    
    test_csv()
    test_query()

if __name__ == '__main__':
    main()


