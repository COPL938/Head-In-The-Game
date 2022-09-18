import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE) # Sets the size of the screen
screen.fill((43, 43, 43)) #Sets the background color of the screen

global biggest_width, width
biggest_width = 0 #Variable that holds the width of objects for spacing
width = pygame.display.get_surface().get_width()

#Colors are defined here
bg = (43, 43, 43)
cyan = (0, 255, 255)
grey = (166, 166, 166)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
magenta = (255, 0, 255)
yellow = (255, 255, 0)




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
    y = 290 #Keeps the calendar at the bottom of the screen
    day = 1
    width = pygame.display.get_surface().get_width()/7 #Divides the width of the screen by 7 so that the calendar takes up the width of the entire screen even if the user resizes.
    for i in range(4): #Creates 4 rows
        for i in range(7): #Creates 7 days in a row
            pygame.draw.rect(screen, grey, (x, y, width, 100), 1)  # Creates the box for each day
            set_nums(x, y, day) #Adds the number to the box
            x += width #Adds to the x variable so the next square is not in the same place
            day += 1 #Adds one to the day variable to raise the number in the day 
        x = 0 #Moves the x variable back to 0 so the next row starts on the left edge
        y += 100 #Moves the next row down


def list_tasks(): # Shows the list of tasks on the home screen
    # tasks dictionary will hold the user's tasks and related info in nested dictionaries
    tasks = {
        'task1': {
            'title': 'Task One',
            'description': 'A placeholder task.',
            'priority' : 'Important',
            'date': '09/17/22'
        }
    } 
    
    def title(): #A function that creates the title for the page
        #Creates the text and rect objects for the title
        font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 30)
        text = font.render('TASKS', True, red)
        text_rect = text.get_rect()
        x = (width - biggest_width - 20) / 3 
        text_rect.center = (x, 30)
        screen.blit(text, text_rect)

    def show_tasks(): #Displays the task list
        for task in tasks:
            # Displays the title and descrition of each task
            title_font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 15)
            font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 10)
            title = title_font.render(tasks[task]['title'], True, green)
            title_rect = title.get_rect() 
            title_rect.topleft = (20, 90)
            desc = title_font.render(tasks[task]['description'], True, magenta)
            desc_rect = desc.get_rect() 
            desc_rect.topleft = (30, 105)
            screen.blit(title, title_rect)
            screen.blit(desc, desc_rect)

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


def buttons(): #Creates the buttons at the right of the screen 
    width = pygame.display.get_surface().get_width() # Gets the width of the screen
    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 20)
    buttons_list = ['', ' ADD TASK ', ' DELETE TASK ', ' EDIT PRIORITIES ', 'VIEW TASKS', ''] # List of buttons. The empty strings at the start and end maintain spacing. The spaces at he begining and end of each word are for the same reason
    y = 2 * (250/len(buttons_list))
    biggest_width = 0 # Will hold the width of the widest button to maintain spacing with other objects.

    global addTask_rect, deleteTask_rect, editPriorities_rect, viewTask_rect #Making these variables global lets you see if the mouse is clicking them as buttons

    # Button for adding a task
    addTask_text = font.render(buttons_list[1], True, black, cyan)
    addTask_rect = addTask_text.get_rect()
    addTask_rect.top = (y)
    addTask_rect.right = (width - 5)
    screen.blit(addTask_text, addTask_rect)
    if addTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
        biggest_width = addTask_rect.width
    y += 250/len(buttons_list) #Moves the next button farther down


    # Button for deleting a task
    deleteTask_text = font.render(buttons_list[2], True, black, cyan)
    deleteTask_rect = deleteTask_text.get_rect()
    deleteTask_rect.top = (y)
    deleteTask_rect.right = (width - 5)
    screen.blit(deleteTask_text, deleteTask_rect)
    if deleteTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
        biggest_width = deleteTask_rect.width
    y += 250/len(buttons_list) #Moves the next button farther down


    # Button for editing priorities
    editPriorities_text = font.render(buttons_list[3], True, black, cyan)
    editPriorities_rect = editPriorities_text.get_rect()
    editPriorities_rect.top = (y)
    editPriorities_rect.right = (width - 5)
    screen.blit(editPriorities_text, editPriorities_rect)
    if editPriorities_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
        biggest_width = editPriorities_rect.width
    y += 250/len(buttons_list) #Moves the next button farther down


    # Button for viewing the tasks
    viewTask_text = font.render(buttons_list[4], True, black, cyan)
    viewTask_rect = viewTask_text.get_rect()
    viewTask_rect.top = (y)
    viewTask_rect.right = (width - 5)
    screen.blit(viewTask_text, viewTask_rect)
    if viewTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
        biggest_width = viewTask_rect.width
    y += 250/len(buttons_list) #Moves the next button farther down


def add_task(): # A function that will add a task 
    screen.fill(bg)
    home_button()


    #Everything here is a placeholder

    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
    text = font.render('ADD A TASK', True, red)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 30)
    screen.blit(text, text_rect)


def delete_task(): # A function that will delete a task
    screen.fill(bg)
    home_button()

    #Everything here is a placeholder

    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
    text = font.render('DELETE A TASK', True, red)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 30)
    screen.blit(text, text_rect)


def edit_priorities(): # A function that will edit the priorities of the tasks
    screen.fill(bg)
    home_button()

    #Everything here is a placeholder

    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
    text = font.render('EDIT PRIORITIES', True, red)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 30)
    screen.blit(text, text_rect)


def view_tasks(): # A function that will view the tasks list
    screen.fill(bg)
    home_button()

    #Everything here is a placeholder

    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 35)
    text = font.render('TASKS', True, red)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 30)
    screen.blit(text, text_rect)


def home_button(): #Creates a home button that will be on every screen other than the home button.
    global home_rect
    font = pygame.font.Font('C:\Windows\Fonts\\times.ttf', 20)
    home = font.render('HOME', True, yellow)
    home_rect = home.get_rect()
    home_rect.topleft = (15, 15)

    screen.blit(home, home_rect)


def home(): #Creates the home screen
    screen.fill(bg)
    create_calendar()
    buttons()
    list_tasks()
    schedule()



    
    
# The game loop
running = True
start = True
while running:

    for event in pygame.event.get():
        #If the user hits the close button.
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if start: #makes the functions that will lead to the pages off the home screen
                if addTask_rect.collidepoint(mouse_pos):
                    start = False
                    add_task()

                elif deleteTask_rect.collidepoint(mouse_pos):
                    start = False
                    delete_task()

                elif editPriorities_rect.collidepoint(mouse_pos):
                    start = False
                    edit_priorities()

                elif viewTask_rect.collidepoint(mouse_pos):
                    start = False
                    view_tasks()
            elif not start: #Makes the home button on every page but the home screen
                if home_rect.collidepoint(mouse_pos):
                    start = True
                    home()
    
    
    if start == True: home()
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()