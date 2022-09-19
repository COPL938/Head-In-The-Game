from tkinter import Y
import pygame
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE) # Sets the size of the screen
pygame.display.set_caption('Head In The Game')
screen.fill((43, 43, 43)) #Sets the background color of the screen

global biggest_width
biggest_width = 0 #Variable that holds the width of objects for spacing

#Colors are defined here
bg = (43, 43, 43)
cyan = (0, 255, 255)
grey = (166, 166, 166)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
magenta = (255, 0, 255)
yellow = (255, 255, 0)

# tasks dictionary will hold the user's tasks and related info in nested dictionaries
global tasks
tasks = {
    'task1': {
        'title': 'Task One',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/17/22',
        'completed': False
    },
    'task2': {
        'title': 'Task Two',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/18/22',
        'completed': False
    },
    'task3': {
        'title': 'Task Three',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/19/22',
        'completed': False
    },
    'task4': {
        'title': 'Task Four',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/17/22',
        'completed': False
    },
    'task5': {
        'title': 'Task Five',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/18/22',
        'completed': False
    },
    'task6': {
        'title': 'Task Six',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/19/22',
        'completed': False
    },
    'task7': {
        'title': 'Task Seven',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/17/22',
        'completed': False
    },
    'task8': {
        'title': 'Task Eight',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/18/22',
        'completed': False
    },
    'task9': {
        'title': 'Task Nine',
        'description': 'A placeholder task.',
        'priority' : 'Important',
        'date': '09/19/22',
        'completed': False
    },
} 


def home_button(): #Creates a home button that will be on every screen other than the home button and shows the time and date.
    global home_rect
    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 20)
    home = font.render(' HOME ', True, black, cyan)
    home_rect = home.get_rect()
    home_rect.topleft = (15, 70)
    screen.blit(home, home_rect)

def clear(): #Clears the screen then adds the home button. This function exists solely to make it that I don't have to use the same 2 lines tons of times.
    screen.fill(bg)
    home_button()

def date_time_label(): #Shows the time and date
    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 20)
    ctime = datetime.now().strftime('%I:%M:%S %p') #These will display the time and date
    if int(ctime[:2]) < 10: ctime = ctime.replace('0', '', 1) 
    cdate = datetime.now().strftime('%A, %m/%d/%y')
    time_text = font.render(ctime, True, yellow, bg)
    time_rect = time_text.get_rect()
    time_rect.topleft = (15, 15)
    date_text = font.render(cdate, True, yellow, bg)
    date_rect = date_text.get_rect()
    date_rect.topleft = (15, 40)
    
    screen.blit(time_text, time_rect)
    screen.blit(date_text, date_rect)



def manage_tasks(func): # A function to manage the tasks 

    def screen_title(text):#Creates a title for the page
        font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
        text = font.render(text, True, red)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 30)
        screen.blit(text, text_rect)

    def display_tasks(): #Displays the tasks

        def title(text, x, y): #A function that creates the title for each task
            font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 15)
            title = font.render(text, True, green)
            title_rect = title.get_rect()
            title_rect.center = (x, y)
            screen.blit(title, title_rect)
            global big_task_width
            if title_rect.width > big_task_width: big_task_width = title_rect.width #Puts the width of the widest rect in that variable to maintain spacing

        def info(text, x, y): #Displays the info for the task
            font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 10)
            description = font.render(text, True, magenta)
            description_rect = description.get_rect() 
            description_rect.topleft = (x, y)
            screen.blit(description, description_rect)
            global big_task_width
            if description_rect.width > big_task_width: big_task_width = description_rect.width #Puts the width of the widest rect in that variable to maintain spacing

        x = 150
        y = 90
        
        global big_task_width
        big_task_width = 0 #To Figure out the width of the widest text so the next column does not overlap.
        columns = 1 #I only want 3 columns, this will stop a fourth from being created

        for task in tasks:
            if y > 600: #If the list of tasks is longer than can fit in one column, start a second column
                if columns == 3: return #I only want 2 columns, this will stop a third from being created
                y = 90
                x = x + big_task_width + 70 #For spacing
                columns += 1 #I only want 3 columns, this will stop a fourth from being created
                
            # Displays the taks and their information
            title(tasks[task]['title'], x, y)
            x += 10 #Indents the descriptions
            y += 20 #Increasing the Y value moves the following description down so they're not overlapping 
            info(tasks[task]['description'], x, y)
            y += 15
            info(tasks[task]['priority'], x, y)
            y += 15
            info(tasks[task]['date'], x, y)
            y += 15
            info(str(tasks[task]['completed']), x, y)
            y += 25
            x -= 10 #Unindents for the next title

    def tasks_buttons(): #Creates the buttons to manage tasks
        global addTask_rect, editTask_rect, deleteTask_rect

        font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 20)
        biggest_width = 0
        x = width - 15
        y = (pygame.display.get_surface().get_height() / 2) / 3

        #Button to add a task
        addTask_text = font.render(' ADD TASK ', True, black, cyan)
        addTask_rect = addTask_text.get_rect()
        addTask_rect.topright = (x, y)
        screen.blit(addTask_text, addTask_rect)
        if addTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
            biggest_width = addTask_rect.width
        y += y #Moves the next button down


        #Button to edit a task
        editTask_text = font.render(' EDIT TASK ', True, black, cyan)
        editTask_rect = editTask_text.get_rect()
        editTask_rect.topright = (x, y)
        screen.blit(editTask_text, editTask_rect)
        if editTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
            biggest_width = editTask_rect.width
        y += y/2 #Moves the next button down. The y/2 is because y was doubled at the last button.


        #Button to remove a task
        deleteTask_text = font.render(' DELETE TASK ', True, black, cyan)
        deleteTask_rect = deleteTask_text.get_rect()
        deleteTask_rect.topright = (x, y)
        screen.blit(deleteTask_text, deleteTask_rect)
        if deleteTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
            biggest_width = deleteTask_rect.width
        y += y #Moves the next button down


    def add_task():
        clear()
        screen_title('ADD A TASK')

    def edit_task():
        clear()
        screen_title('EDIT A TASK')

    def delete_task():
        clear()
        screen_title('DELETE A TASK')

    clear()
    if func == 'home screen':
        working['tasks']['main'] = True
        screen_title('MANAGE TASKS')
        display_tasks()
        tasks_buttons()
    elif func == 'add task':
        add_task()
    elif func == 'edit task':
        edit_task()
    elif func == 'delete task':
        delete_task()


def manage_schedule(func): # A function that will delete a task
    clear()

    #Everything here is a placeholder

    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
    text = font.render('MANAGE SCHEDULE', True, red)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 30)
    screen.blit(text, text_rect)


def home(): #Creates the home screen
    
    def create_calendar(): #Creates the calendar at the bottom of the screen
        def set_nums(x, y, day): #Adds the numbers to the calendar
            day = str(day) 
            x += 2 #Adding 2 to the x and y coordinates moves the number slightly off the line of the calendar box
            y += 2
            font = pygame.font.Font('C:\Windows\Fonts\consola.ttf', 20)
            text = font.render(day, True, grey)
            text_rect = text.get_rect() #Creates the rect objects for the text
            text_rect.topleft = (x, y)
            screen.blit(text, text_rect) #Adds the rect objects to the screen

        x = 0 #Starts the calendar at the left edge
        y = 300 #Keeps the calendar at the bottom of the screen
        day = 1
        width = pygame.display.get_surface().get_width()/7 #Divides the width of the screen by 7 so that the calendar takes up the width of the entire screen even if the user resizes.
        for i in range(5): #Creates 5 rows
            for i in range(7): #Creates 7 days in a row
                pygame.draw.rect(screen, grey, (x, y, width, 75), 1)  # Creates the box for each day
                if day == 32: day = 1 #Resets the calendar back to day 1
                set_nums(x, y, day) #Adds the number to the box
                x += width #Adds to the x variable so the next square is not in the same place
                day += 1 #Adds one to the day variable to raise the number in the day 
            x = 0 #Moves the x variable back to 0 so the next row starts on the left edge
            y += 75 #Moves the next row down


    def list_tasks(): # Shows the list of tasks on the home screen
        
        def title(): #A function that creates the title for the page
            #Creates the text and rect objects for the title
            font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 30)
            text = font.render('TASKS', True, red)
            text_rect = text.get_rect()
            x = (width - biggest_width - 20) / 3 
            text_rect.center = (x, 30)
            screen.blit(text, text_rect)

        def show_tasks(): #Displays the task list
            y = 90 # x and y coordinates for the tasks
            x = 1.5 * (width / 7)
            big_task_width = 0 #To Figure out the width of the widest text so the next column does not overlap.
            second_column = False #I only want 2 columns, this will stop a third from being created

            for task in tasks:
                if y > 255: #If the list of tasks is longer than can fit in one column, start a second column
                    if second_column: return #I only want 2 columns, this will stop a third from being created
                    y = 90
                    x = x + big_task_width + 15
                    second_column = True #I only want 2 columns, this will stop a third from being created
                    
                # Displays the title and descrition of each task
                title_font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 15)
                font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 10)
                title = title_font.render(tasks[task]['title'], True, green)
                title_rect = title.get_rect() 
                title_rect.topleft = (x, y)
                desc = title_font.render(tasks[task]['description'], True, magenta)
                desc_rect = desc.get_rect() 
                desc_rect.topleft = (x + 10, y + 15)
                if title_rect.width > big_task_width: #Figures out the width of the widest text so the next column does not overlap.
                    big_task_width = title_rect.width
                if desc_rect.width > big_task_width + 10:
                    big_task_width = desc_rect.width

                screen.blit(title, title_rect)
                screen.blit(desc, desc_rect)
                y += 45

        title()
        show_tasks()


    def schedule(): # Displays the schedule on the home screen
        width = pygame.display.get_surface().get_width() # Gets the width of the screen
        working_width = ((width - biggest_width) / 2 ) - 20
        working_width = working_width + working_width 

        def title():
            font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 30)
            text = font.render('SCHEDULE', True, red)
            text_rect = text.get_rect()
            x = 2 * ((width - biggest_width -20 ) / 3 )
            text_rect.center = (x, 30)
            screen.blit(text, text_rect)



        title()


    def buttons(): #Creates the buttons at the left of the screen 
        font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 20)
        buttons_list = ['', ' MANAGE TASKS ', ' MANAGE SCHEDULE ', ''] # List of buttons. The empty strings at the start and end maintain spacing. The spaces at he begining and end of each word are for the same reason
        y = 2 * (250/len(buttons_list))
        biggest_width = 0 # Will hold the width of the widest button to maintain spacing with other objects.

        global manageTasks_rect, manageSchedule_rect #Making these variables global lets you see if the mouse is clicking them as buttons

        # Button for adding a task
        manageTasks_text = font.render(buttons_list[1], True, black, cyan)
        manageTasks_rect = manageTasks_text.get_rect()
        manageTasks_rect.topleft = (5, y)
        screen.blit(manageTasks_text, manageTasks_rect)
        if manageTasks_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
            biggest_width = manageTasks_rect.width
        y += 250/len(buttons_list) #Moves the next button farther down



        # Button for deleting a task
        manageSchedule_text = font.render(buttons_list[2], True, black, cyan)
        manageSchedule_rect = manageSchedule_text.get_rect()
        manageSchedule_rect.topleft = (5, y)
        screen.blit(manageSchedule_text, manageSchedule_rect)
        if manageSchedule_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
            biggest_width = manageSchedule_rect.width
        y += 250/len(buttons_list) #Moves the next button farther down


    screen.fill(bg)
    global running_schedule, running_tasks
    working['schedule']['running'] = False #Keeps the schedule and task functions from being run until it's the correct time.
    working['tasks']['running'] = False
    create_calendar()
    buttons()
    list_tasks()
    schedule()



    
global working
# A dictionary to organize the many variables that keep everything running or not running.
working = {
    'home': {
        'start': True
    },
    'schedule': {
        'running': False,
        'main': False #Keeps the schedule function from being run
    },
    'tasks': {
        'running': False, #Keeps the tasks function from being run
        'main': False, 
        'adding_task': False, #Keeps the add_task function from being run
        'deleting_task': False, #Keeps the delete_task function from being run
        'editing_task': False #Keeps the edit_task function from being run
    }
}


global width # A variable to keep the width of the window
# The game loop
running = True
while running:
    width = pygame.display.get_surface().get_width() #It is inside the loop so that it changes if the window is resized

    for event in pygame.event.get():
        #If the user hits the close button.
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if working['home']['start']: #makes the functions that will lead to the pages off the home screen
                if manageTasks_rect.collidepoint(mouse_pos):
                    working['home']['start'] = False
                    working['schedule']['running'] = False
                    working['tasks']['running'] = True
                    func = 'home screen'

                elif manageSchedule_rect.collidepoint(mouse_pos):
                    working['home']['start'] = False
                    working['tasks']['running'] = False
                    working['schedule']['running'] = True
                    func = ''

            elif not working['home']['start']: #Makes the home button on every page but the home screen
                if home_rect.collidepoint(mouse_pos):
                    working['home']['start'] = True
                    home()

            if working['schedule']['running']: 
                # To handle the events in the schedule
                pass

            elif working['tasks']['running']:
                # To hande the events in the tasks
                if working['tasks']['main']:
                    #Handles the events in the main page
                    if addTask_rect.collidepoint(mouse_pos): #If the button to add a task is clicked
                        #Makes sure that only the function to add a task runs.
                        working['tasks']['main'] = False
                        working['tasks']['editing_task'] = True
                        working['tasks']['deleting_task'] = True
                        working['tasks']['adding_task'] = True
                        func = 'add task'
                    
                    elif editTask_rect.collidepoint(mouse_pos): #If the button to edit a task is clicked
                        #Makes sure that only the function to add a task runs.
                        working['tasks']['main'] = False
                        working['tasks']['adding_task'] = True
                        working['tasks']['deleting_task'] = True
                        working['tasks']['editing_task'] = True
                        func = 'edit task'

                    elif deleteTask_rect.collidepoint(mouse_pos): #If the button to delete a task is clicked
                        #Makes sure that only the function to add a task runs.
                        working['tasks']['main'] = False
                        working['tasks']['adding_task'] = True
                        working['tasks']['editing_task'] = True
                        working['tasks']['deleting_task'] = True
                        func = 'delete task'

    
    
    if working['home']['start']: home()
    elif working['schedule']['running']: manage_schedule(func)
    elif working['tasks']['running']: manage_tasks(func)

    date_time_label()
    pygame.display.flip()

pygame.quit()
