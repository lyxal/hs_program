"""
Project: Head Scruitineer Assister

Author: JonoCode9374

Date Created: 10/02/2018

Description: This program helps the head scruitineer of the class to check
all the criteria specified is met by cars.
    
                                                                             """

"""The F1 IN SCHOOLS Logo, F1, FORMULA 1, FIA FORMULA ONE WORLD CHAMPIONSHIP,
GRAND PRIX and related marks are trademarks of Formula One Licensing BV,
a Formula One group company. All rights reserved."""
#TODO: Document this is messy spots
import tkinter, screens, CFD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os

window = tkinter.Tk()
window.title("Jonathan's Car Scruitinizer")

#Go through all needed documents and gather all data required for init
criteria = CFD.CFD_Doc(open(os.path.join(os.path.dirname(__file__), "Documents/Criteria.txt"), encoding="utf-8"))
#quick_regs = CFD.CFD_Doc(open("/Users/jonathan.oswald/Desktop/HS Programs/Documents/quickregs.txt", encoding="utf-8")) #Bit of a problem here
team_file = "" #Will be replaced later w/ an actuall file obj.
team_backup = open(os.path.join(os.path.dirname(__file__),"Documents/Teams.txt")).read()


#Create all the functions needed for buttons
def add_new():
    new.show(); start.hide()

    
def load():
    for widget in load.widgets:
        del widget
    teams = CFD.CFD_Doc(open(os.path.join(os.path.dirname(__file__), "Documents/Teams.txt")))
    people = teams.query("SELECT $Team_Name $Index")

    if len(people) == 0:
        load_widgets.append(tkinter.Label(window, text=str("There seem to be" +\
                                                           " no teams yet.")))
        load_widgets.append(tkinter.Button(window, text="Go Back?", command=back))

        load.add_item(load_widgets[0], 0, 0)
        load.add_item(load_widgets[1], 1, 0)
    else:                                         
        for i in range(len(people)):
            load_widgets.append(tkinter.Label(window, text=str(" ".join(people[i]) +\
                                                               " tests completed")))
            load.add_item(load_widgets[i], i, 0)

        load_widgets.append(tkinter.Entry(window, width=70))
        load_widgets[i+1].insert(tkinter.END, "Enter the team name you want to load here")
        load_widgets.append(tkinter.Button(window, text="Load!", command=do_load))
        load.add_item(load_widgets[i+1], i + 1, 0)
        load.add_item(load_widgets[i+2], i + 2, 0)
    load.show()
    start.hide()

def submit():
    global team_file, original_row, team_name
    
    #Adds a new team to the doc
    file = open("/Users/jonathan.oswald/Desktop/HS Programs/Documents/Teams.txt", "a")
    file.write(str("\n" + entry_1.get() + " : " + entry_2.get()\
                   + " : " + str(entry_1.get() + ".txt") + " : " + str(0) + " : No"))

    original_row = [entry_1.get(), entry_2.get(), str(entry_1.get() + ".txt"), "0", "No"]
    team_name = entry_1.get()
    file.close()
    team_file = open(os.path.join(os.path.dirname(__file__), "Documents/In Progress/{0}.txt".format(entry_1.get())), "w")

    
    
    team_file.write("""#DONOTEDIT\n!Format\n$Section : $Met : $Comment""")

    entry_1.delete(0, tkinter.END); entry_2.delete(0, tkinter.END)
    new.hide()
    tests.show(); comment_bar.grid_forget(); continue_button.grid_forget();
    next_article()


def yes():
    global article_index, team_file
    team_file.write("\n{0} : Yes : NA".format(section))
    article_index += 1
    next_article()

def no():
    comment_bar.grid(row=4,column=0)
    continue_button.grid(row=4,column=1)
    fail_button.config(state=tkinter.DISABLED)
    pass_button.config(state=tkinter.DISABLED)
    skip_button.config(state=tkinter.DISABLED)
    
def comment():
    comment_bar.grid_forget(); continue_button.grid_forget();
    global article_index, team_file
    text = comment_bar.get()
    team_file.write("\n{0} : No : {1}".format(section, text))
    article_index += 1
    next_article()
    fail_button.config(state=tkinter.NORMAL)
    pass_button.config(state=tkinter.NORMAL)
    skip_button.config(state=tkinter.NORMAL)
    comment_bar.delete(0, tkinter.END);
    

def back():
    load.hide()
    start.show()

def next_article():
    global section
    if article_index == 90:
        show_finish()
        return
    
    article.delete(0.0, tkinter.END)
    current_article = criteria.query("SELECT $Section $Description $Image_Location LIMIT 1 START " +\
                                       str(article_index))
    display = "Section {0}: {1}".format(current_article[0][0], current_article[0][1])

    section = current_article[0][0]

    image.config(file=os.path.join(os.path.dirname(__file__),"Documents/Images/{0}.gif".format(current_article[0][2])))
    width, height = image.width()/100, image.height()/100
    image.subsample(int(width), int(height))
    image_shown.config(image=image)
    
    article.insert(tkinter.END, display)
                                       

def do_load():
    global article_index, original_row, team_file, team_name
    
    teams = CFD.CFD_Doc(open(os.path.join(os.path.dirname(__file__),"Documents/Teams.txt")))
    team_name = load_widgets[len(load_widgets) - 2].get()

    original_row = teams.query(
        "SELECT * WHERE ($Team_Name ==" + "'" + (team_name) + "')")[0]
    for result in teams.query("SELECT $Team_Name WHERE ($Team_Name ==" + "'" + (team_name) + "')"):
        if team_name not in result:
            return

        else:
            article_index = int(teams.query("SELECT $Index WHERE ($Team_Name ==" + "'" + (team_name) + "')")[0][0])
            load.hide()
            tests.show(); comment_bar.grid_forget(); continue_button.grid_forget();

            team_file = open(os.path.join(os.path.dirname(__file__),"Documents/In Progress/{0}".format(
                teams.query("SELECT $File WHERE ($Team_Name == '{0}')".format(team_name))[0][0])), "a")
            next_article()
            break
        
def save_work():

    file = open(os.path.join(os.path.dirname(__file__),"Documents/Teams.txt"))
    contents = file.read()
    file.close()
    try:
        file = open(os.path.join(os.path.dirname(__file__),"Documents/Teams.txt"), "w")
        print(original_row)
        file.write( 
            contents.replace(" : ".join(original_row), "{0} : {1} : {2} : {3} : {4}".format(original_row[0], original_row[1], original_row[2],
                                   article_index, original_row[4])))
  
    except Exception as e: file.write(team_backup); print(e.args)
    finally: file.close();
    
    global team_file
    try:
        team_file.close()
    except: pass
    window.destroy()

def na():
    global article_index, team_file
    team_file.write("\n{0} : NA : NA".format(section))
    article_index += 1
    next_article()

def show_finish():
    teams = CFD.CFD_Doc(open(os.path.join(os.path.dirname(__file__),"Documents/Teams.txt")))
    has_email = teams.query("SELECT $Emailed WHERE ($Team_Name == '{0}')".format(original_row[0]))[0]
    print(has_email)
    tests.hide()
    finish.show()

    if has_email[0] == "No":
        resend_button.grid_forget()
        delete_button.grid_forget()
        message3.grid_forget()
    else:
        message2.grid_forget()
        send_button.grid_forget()
        

def email():
    global team_file
    team_file.close()
    #Code taken from https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f
    #Modified slightly to work with this program

    ADDRESS = ""#Enter your email address here
    PASSWORD = "" #Enter your password here


    #Generate the message


    temp_file = open(os.path.join(os.path.dirname(__file__),"Documents/In Progress/{0}.txt".format(
        team_name)), "r").read()

    message = """Hey {0},

Here are the results of your car when compared to the Technical Regulations:
	
	{1}
	
Feel free to email me if you have any questions about any tests.
From Jonathan Oswald
""".format(original_row[0], temp_file)
    
    #Send the message

    print(original_row[1])

    s = smtplib.SMTP(host='your-smtp-host-here', port=YOUR_PORT_HERE) #You might have to google what host you have.
    s.starttls()
    s.login(ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From'] = ADDRESS
    msg['To'] = original_row[1]
    msg['Subject'] = "Your Car's Results"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg


    #And now change the row to say that yes, the team has been

    file = open(os.path.join(os.path.dirname(__file__), "Documents/Teams.txt"))
    contents = file.read()
    file.close()
    try:
        file = open(os.path.join(os.path.dirname(__file__), "Documents/Teams.txt", "w"))
        file.write( 
            contents.replace(" : ".join(original_row), "{0} : {1} : {2} : {3} : Yes".format(original_row[0], original_row[1], original_row[2],
                                   article_index)))
  
    except Exception as e: file.write(team_backup);
    finally: file.close();

    show_finish()

def delete():
    file = open(os.path.join(os.path.dirname(__file__), "Documents/Teams.txt"))
    contents = file.read()
    file.close()
    try:
        file = open(os.path.join(os.path.dirname(__file__),"Documents/Teams.txt"), "w")
        file.write(contents.replace(" : ".join(original_row), ""))
  
    except Exception as e: file.write(team_backup);
    finally: file.close();

def resend():
    #Code taken from https://medium.freecodecamp.org/send-emails-using-code-4fcea9df63f
    #Modified slightly to work with this program

    ADDRESS = ""#Enter your email address here
    PASSWORD ="" #Enter your password here

    #Generate the message


    temp_file = open(os.path.join(os.path.dirname(__file__), "Documents/In Progress/{0}.txt".format(
        team_name), "r")).read()

    message = """Hey {0},

Here are the results of your car when compared to the Technical Regulations:
	
	{1}
	
Feel free to email me if you have any questions about any tests.
From YOUR_NAME_HERE
""".format(original_row[0], temp_file)
    
    #Send the message

    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587) #The message from the other function applies here
    s.starttls()
    s.login(ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    msg['From'] = ADDRESS
    msg['To'] = original_row[1]
    msg['Subject'] = "Your Car's Results"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg


    #And now change the row to say that yes, the team has been

    file = open(os.path.join(os.path.dirname(__file__), "Documents/Teams.txt"))
    contents = file.read()
    file.close()
    try:
        file = open(os.path.join(os.path.dirname(__file__), "Documents/Teams.txt"), "w")
        file.write( 
            contents.replace(" : ".join(original_row), "{0} : {1} : {2} : {3} : Yes".format(original_row[0], original_row[1], original_row[2],
                                   article_index)))
  
    except Exception as e: file.write(team_backup);
    finally: file.close();

def show_more():
    pass

#Some quick vars

article_index = 0
original_row = ""
section = ""
        

#Create all the screens

#Start screen
start = screens.Screen("Welcome", window)
start_button = tkinter.Button(window, text="New Team", command=add_new)
load_button = tkinter.Button(window, text="Load Team", command=load)

start.add_item(start_button, 0, 3)
start.add_item(load_button, 0, 4)

start.show()

#New team screen
new = screens.Screen("Add New Team", window)

info_1 = tkinter.Label(window, text="Enter Team Name: ")
entry_1 = tkinter.Entry(window, width=60)
info_2 = tkinter.Label(window, text="Enter The Nominated Email: ")
entry_2 = tkinter.Entry(window, width=60)
submit_button = tkinter.Button(window, text="Submit", command=submit)


new.add_item(info_1, 2, 3)
new.add_item(entry_1, 2, 4)
new.add_item(info_2, 3, 3)
new.add_item(entry_2, 3, 4)
new.add_item(submit_button, 5, 0)

#Test screen

tests = screens.Screen("Technical Tests", window)

more_button = tkinter.Button(window, text="Load More", width=20, command=show_more)
pass_button = tkinter.Button(window, text="Passed", width=20, command=yes)
fail_button = tkinter.Button(window, text="Failed", width=20, command=no)
skip_button = tkinter.Button(window, text="Not Applicable", width=20, command=na)
comment_bar = tkinter.Entry(window, width=60)
blank = tkinter.Label(window)
continue_button = tkinter.Button(window, text="Submit", command=comment)
article = tkinter.Text(window, width=125, height=5)
image = tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "documents/Images/NA.gif"))
image_shown = tkinter.Label(image=image)

tests.add_item(article, 0, 0)
tests.add_item(pass_button, 0, 1)
tests.add_item(fail_button, 1, 1)
tests.add_item(comment_bar, 5, 0)
tests.add_item(continue_button, 5, 1)
tests.add_item(image_shown, 1, 0)
tests.add_item(skip_button, 2, 1)

#Load team screen
 
load = screens.Screen("Load A Team", window)
load_widgets = list()

#Finishing Screen

finish = screens.Screen("All Done!", window)

message = tkinter.Label(window, text="Well Done! You're finished!")
message2 = tkinter.Label(window, text="It seems an email hasn't been sent yet")
message3 = tkinter.Label(window, text="An email has been sent. You can delete this team now")
send_button = tkinter.Button(window, text="Send Email?", command=email)
resend_button = tkinter.Button(window, text="Resend Email?", command=resend)
delete_button = tkinter.Button(window, text="Delete Team?", command=delete)

finish.add_item(message, 0, 1)
finish.add_item(message2, 1, 1)
finish.add_item(message3, 1, 1)
finish.add_item(send_button, 2, 1)
finish.add_item(delete_button, 2, 1)
finish.add_item(resend_button, 2, 2)

#Taken from StackOverflow -- Matt Gregory's Answer. Link: https://stackoverflow.com/a/111160/9363594
#And yes, I did upvote the answer. Thanks for asking.

#But modified to suit this program (duh.)

window.protocol("WM_DELETE_WINDOW", save_work)


