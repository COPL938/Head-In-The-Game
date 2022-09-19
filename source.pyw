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


def manage_tasks(): # A function to manage the tasks 
    screen.fill(bg)
    home_button()

    #A title for the page
    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
    text = font.render('MANAGE TASKS', True, red)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 30)
    screen.blit(text, text_rect)

    def display_tasks():

        def title(text, x, y): #A function that creates the title for each task
            font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 15)
            title = font.render(text, True, green)
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            screen.blit(text, text_rect)

        def show_tasks(text, x, y): #Displays the info for the task
            for task in tasks:
                font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 10)
                description = font.render(text, True, magenta)
                description_rect = description.get_rect() 
                description_rect.topleft = (x, y)
                screen.blit(description, description_rect)

def manage_schedule(): # A function that will delete a task
    screen.fill(bg)
    home_button()

    #Everything here is a placeholder

    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
    text = font.render('MANAGE SCHEDULE', True, red)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 30)
    screen.blit(text, text_rect)


def home_button(): #Creates a home button that will be on every screen other than the home button and shows the time and date.
    global home_rect
    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 20)
    home = font.render(' HOME ', True, black, cyan)
    home_rect = home.get_rect()
    home_rect.topleft = (15, 70)
    screen.blit(home, home_rect)


def date_time_label():
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
        width = pygame.display.get_surface().get_width() # Gets the width of the screen
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
    running_schedule = False #Keeps the schedule and task functions from being run until it's the correct time.
    running_tasks = False
    create_calendar()
    buttons()
    list_tasks()
    schedule()



    
    
# The game loop
running = True
start = True #This will make the home screen show up
global running_schedule, running_tasks
running_schedule = False #Keeps the schedule and task functions from being run until it's the correct time.
running_tasks = False
global width # A variable to keep the width of the window
while running:
    width = pygame.display.get_surface().get_width() #It is inside the loop so that it changes if the window is resized

    for event in pygame.event.get():
        #If the user hits the close button.
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if start: #makes the functions that will lead to the pages off the home screen
                if manageTasks_rect.collidepoint(mouse_pos):
                    start = False
                    running_tasks = True

                elif manageSchedule_rect.collidepoint(mouse_pos):
                    start = False
                    running_schedule = True

            elif not start: #Makes the home button on every page but the home screen
                if home_rect.collidepoint(mouse_pos):
                    start = True
                    home()
    
    
    if start == True: home()
    elif running_schedule: manage_schedule()
    elif running_tasks: manage_tasks()

    date_time_label()
    pygame.display.flip()

pygame.quit()
