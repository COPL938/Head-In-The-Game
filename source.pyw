import pygame, time
from datetime import datetime, date
from json import dump, load
from plyer import notification


def main(): #The main function that controls the game. 
    pygame.init() #Initialize pygame. This needs to be done before anything else can work because both threads need to access the pygame events.

    screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE) # Sets the size of the screen
    pygame.display.set_caption('Head In The Game')
    screen.fill((43, 43, 43))  #Sets the background color of the screen
    global biggest_width
    biggest_width = 0 #Variable that holds the width of objects for spacing

    #Colors are defined here
    bg = (43, 43, 43)
    black = (0, 0, 0)
    black_active = (64, 64, 64)
    cyan = (66, 155, 245)
    cyan_active = (66, 125, 245)
    grey = (166, 166, 166)
    info_color = (75, 116, 107)
    overdue_red = (159, 0, 80)
    prompt_purple = (158, 114, 196)
    task_blue = (85, 112, 44)
    task_green = (15, 145, 32) 
    text_yellow = (226, 197, 12) 
    title_yellow = (27, 86, 94)




    # Housekeeping Functions
    def start_up(): #Create the temp and task dicts and the copleting variable
        
        def find_todays_tasks(): #Sorts the tasks into the apropriate lists.
            #todays_tasks will hold the tasks that need to be done today. This is purely for the notifications.
            global todays_tasks
            todays_tasks = []
            
            today = datetime.now() #Gets today's date for the calcualtions. It is outside the loop because there is no need to have it re-run many times.
            for task in tasks:
                try:
                    date = datetime.strptime(tasks[task]['date'], '%m/%d/%y')
                    diff = today - date #Gets the difference between today's date and the date of the task. 
                    diff = diff.days
                except:
                    diff = -1
                
                if diff > 0: #If the number of days between the date and today it positve, the task is overdue add its dict key to the todays_tasks list
                    todays_tasks.append(task)
                
                elif diff == 0: #If the number of days between the date and today it 0, the task needs to be done today and add its dict key to the todays_tasks list
                    todays_tasks.append(task)
        
            
        def start_main():
            global tasks, temp, task_num, completing
            completing = '' #This will hold the name of the task that will be marked complete in the complete_task function

            # Tasks dictionary will hold the user's tasks and related info in nested dictionaries. 
            tasks = {}

            #Add the contents of the task.json file to the tasks dictionary.
            try:
                with open('tasks.json') as file:
                    raw = load(file)
                tasks.update(raw)
            except Exception as e:
                tasks = {}
            #Find the highest task number used so far
            keys = list(tasks.keys())
            num = 0 #Variable to find the highest task number used already
            for key in keys:
                key = key.split('_')
                key_num = int(key[-1])
                if key_num > num:
                    num = key_num
            num += 1 #The number that will be used is one higher than the highest task number still in use.
            task_num = f'Task_{num}' #Holds the key for the nested dictionary in temp

            temp = {                #Temp dictionary will hold whatever task the user is creating or completing.
                task_num: {
                    'title': '',
                    'description': '',
                    'priority': '',
                    'date': '',
                    'time to start': '',
                    'time to complete': ''
                }
            }

        start_main()
        find_todays_tasks()

 
    def shut_down(): #Save contents of the task dict to tasks.json file and delets the temp dict
        global tasks, temp
        with open('tasks.json', 'w') as file:
            dump(tasks, file, indent=4)
        del(temp) 

    def home_button(active): #Creates a home button that will be on every screen other than the home button and shows the time and date.
        if active == 'home': #Changes the color of the home button
            home_button_color = cyan_active
        else:
            home_button_color = cyan
        global home_rect
        font = pygame.font.Font('klavika-light.ttf', 20)
        home = font.render(' HOME ', True, black, home_button_color)
        home_rect = home.get_rect()
        home_rect.topleft = (15, 70)
        screen.blit(home, home_rect)

    def clear(active_button): #Clears the screen then adds the home button. This function exists solely to make it that I don't have to use the same 2 lines tons of times.
        screen.fill(bg)
        home_button(active_button)

    def date_time_label(): #Shows the time and date
        font = pygame.font.Font('klavika-light.ttf', 20)
        ctime = datetime.now().strftime('%I:%M:%S %p') #These will display the time and date
        if int(ctime[:2]) < 10: ctime = ctime.replace('0', '', 1) 
        cdate = datetime.now().strftime('%A, %m/%d/%y')
        time_text = font.render(ctime, True, title_yellow, bg)
        time_rect = time_text.get_rect()
        time_rect.topleft = (15, 15)
        date_text = font.render(cdate, True, title_yellow, bg)
        date_rect = date_text.get_rect()
        date_rect.topleft = (15, 40)
        
        screen.blit(time_text, time_rect)
        screen.blit(date_text, date_rect)


    # Work Functions

    def manage_tasks(task_func, button): # A function to manage the tasks 

        def screen_title(text):#Creates a title for the page
            font = pygame.font.Font('klavika-light.ttf', 35)
            text = font.render(text, True, title_yellow)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 30)
            screen.blit(text, text_rect)

        def display_tasks(complete, adding): #Displays the tasks

            def title(text, x, y): #A function that creates the title for each task
                font = pygame.font.Font('klavika-light.ttf', 15)
                title = font.render(text, True, task_green)
                title_rect = title.get_rect()
                title_rect.centery = y
                title_rect.left = x
                screen.blit(title, title_rect)
                global big_task_width
                if title_rect.width > big_task_width: big_task_width = title_rect.width #Puts the width of the widest rect in that variable to maintain spacing

            def info(text, x, y): #Displays the info for the task
                font = pygame.font.Font('klavika-light.ttf', 13)
                description = font.render(text, True, info_color)
                description_rect = description.get_rect() 
                description_rect.topleft = (x, y)
                screen.blit(description, description_rect)
                global big_task_width
                if description_rect.width > big_task_width: big_task_width = description_rect.width #Puts the width of the widest rect in that variable to maintain spacing

            x = 25
            y = 115
            
            global big_task_width
            big_task_width = 0 #To Figure out the width of the widest text so the next column does not overlap.
            columns = 1 #I only want 3 columns, this will stop a fourth from being created

            count = 1 #To display the task numbers for the complete task function
            for task in tasks:
                if task == 'completing': continue 
                if y > pygame.display.get_surface().get_height() - 100: #If the list of tasks is longer than can fit in one column, start a second column
                    if columns == 3: return #I only want 2 columns, this will stop a third from being created
                    y = 90
                    if complete: #Moves the second column beneath the complete task stuff.
                        y = 300
                    if adding: #Keeps only one column in the adding screen
                        break
                        
                    x = x + big_task_width + 50 #For spacing
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created
                    
                # Displays the taks and their information
                if complete: title(f'Task #{count} - {tasks[task]["title"]}', x, y)
                else: title(f'{tasks[task]["title"]}', x, y)
                x += 10 #Indents the descriptions
                y += 10 #Increasing the Y value moves the following description down so they're not overlapping 
                info(tasks[task]['description'], x, y)
                y += 15
                if not complete and not adding: #On the complete page, only show the title and description
                    info(tasks[task]['priority'], x, y)
                    y += 15
                if not complete and not adding: #On the complete page, only show the title and description                
                    info(tasks[task]['date'], x, y)
                    y += 15
                if not complete and not adding: #On the complete page, only show the title and description
                    info(str(tasks[task]['time to start']), x, y)
                    y += 15
                if not complete and not adding: #On the complete page, only show the title and description
                    info(str(tasks[task]['time to complete']), x, y)
                    y += 25
                if complete or adding:
                    y += 10 #Keeps enough space between the tasks
                x -= 10 #Unindents for the next title

                count += 1 #To display task numbers for the complete_task function

        def tasks_buttons(button): #Creates the buttons to manage tasks
            #Changes the color of the buttons
            add_task_color = cyan
            complete_task_color = cyan
            if button == 'add_task':
                add_task_color = cyan_active
            elif button == 'complete_task':
                complete_task_color = cyan_active
                
            
            global addTask_rect, addTask_text, completeTask_rect

            font = pygame.font.Font('klavika-light.ttf', 20)
            biggest_width = 0
            x = width - 15
            y = (pygame.display.get_surface().get_height() / 2) / 3

            #Button to add a task
            addTask_text = font.render('  ADD A TASK  ', True, black, add_task_color)
            addTask_rect = addTask_text.get_rect()
            addTask_rect.topright = (x, y)
            screen.blit(addTask_text, addTask_rect)
            if addTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
                biggest_width = addTask_rect.width
            y += y #Moves the next button down


            #Button to remove a task
            completeTask_text = font.render(' COMPLETE TASK ', True, black, complete_task_color)
            completeTask_rect = completeTask_text.get_rect()
            completeTask_rect.topright = (x, y)
            screen.blit(completeTask_text, completeTask_rect)
            if completeTask_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
                biggest_width = completeTask_rect.width
            y += y #Moves the next button down


        def add_task(add_func, button):
            clear(button)
            screen_title('ADD A TASK')
            display_tasks(False, True)


            def display_prompt(text, x, y): #A function that creates the prompt for each input
                font = pygame.font.Font('klavika-light.ttf', 25)
                title = font.render(text, True, prompt_purple, bg)
                title_rect = title.get_rect()
                title_rect.topleft = (x, y)
                screen.blit(title, title_rect)
                return  title_rect.right + 5, title_rect.centery

            def display_instr(text, left, y): # A function to display instructions for the user
                font = pygame.font.Font('klavika-light.ttf', 15)
                title = font.render(text, True, prompt_purple, bg)
                title_rect = title.get_rect()
                title_rect.left = left
                title_rect.centery = y
                screen.blit(title, title_rect)

            def done():
                global func
                for task in temp:
                    if temp[task]['title'] == '': 
                        shut_down()
                        start_up()
                        func = 'home screen'
                    else:
                        tasks.update(temp)
                        shut_down() #Saves everything to tasks.json file and deleted the temp and task dicts
                        start_up() #Recreates thet temp and task dicts and completed variable
                        #Those two need to be done so that multiple tasks can be added in one app session.
                        working['tasks']['adding_task'] = False
                        func = 'home screen'
                
                


            def addTask_main(color_to_change, colored_button):
                x = 500
                y = 90
                
                input_font = pygame.font.Font('klavika-light.ttf', 20) #For the inputs


                #Rects need to be global so they can be acessed in the game loop
                global adding_title_backdrop, adding_desc_backdrop, adding_priority_backdrop, adding_date_backdrop, adding_time_backdrop, adding_startTime_backdrop
                #input strings
                
                #change the color of the textbox when it's selected
                title_color = desc_color = priority_color = date_color = time_color = start_color = black
                if color_to_change == 'title': title_color = black_active
                elif color_to_change == 'desc': desc_color = black_active
                elif color_to_change == 'priority': priority_color = black_active
                elif color_to_change == 'date': date_color = black_active
                elif color_to_change == 'time': time_color = black_active
                elif color_to_change == 'start_time': start_color = black_active


                # Title    
                #Create the prompts and rectangles for inputs
                display_prompt('Title       ', x, y)  #The whitespace is to everwrite ant task info that is too long
                y += 35                                                           #Moves the next box down
                title = input_font.render(temp[task_num]['title'], True, text_yellow)     #Renders the text
                adding_title_backdrop = pygame.draw.rect(screen, title_color, (x, y, 400, 30)) #Creates the rect for the text
                adding_title_rect = title.get_rect()                                     #Creates a rect for the text
                adding_title_rect.topleft = (x+5, y+5)                                      #Moves the rect to the right coordinates
                screen.blit(title, adding_title_rect)                                  #Moves them onto the screen
                y += 40
                #Cursor
                if color_to_change == 'title':
                    cursor = pygame.Rect(adding_title_rect.topright, (2, adding_title_rect.height))
                    if time.time() % 1 > 0.5: pygame.draw.rect(screen, text_yellow, cursor)

                #Description
                display_prompt('Description                ', x, y)
                y += 35
                desc = input_font.render(temp[task_num]['description'], True, text_yellow)
                adding_desc_backdrop = pygame.draw.rect(screen, desc_color, (x, y, 400, 30))
                adding_desc_rect = desc.get_rect()
                adding_desc_rect.topleft = (x+5, y+5)  
                screen.blit(desc, adding_desc_rect)      
                y += 40
                #Cursor
                if color_to_change == 'desc':
                    cursor = pygame.Rect(adding_desc_rect.topright, (2, adding_desc_rect.height))
                    if time.time() % 1 > 0.5: pygame.draw.rect(screen, text_yellow, cursor)


                #Priority
                instr_left, instr_y = display_prompt('Priority', x, y) #Those two variables are for the instrucitons
                display_instr('(high/medium/low)       ', instr_left, instr_y)
                y += 35
                priority = input_font.render(temp[task_num]['priority'], True, text_yellow)
                adding_priority_backdrop = pygame.draw.rect(screen, priority_color, (x, y, 400, 30))
                adding_priority_rect = priority.get_rect()
                adding_priority_rect.topleft = (x+5, y+5)
                screen.blit(priority, adding_priority_rect)        
                y += 40
                if color_to_change == 'priority':
                    cursor = pygame.Rect(adding_priority_rect.topright, (2, adding_priority_rect.height))
                    if time.time() % 1 > 0.5: pygame.draw.rect(screen, text_yellow, cursor)


                #Due date
                instr_left, instr_y = display_prompt('Due Date ', x, y)
                display_instr('(mm/dd/yy)     ', instr_left, instr_y)
                y += 35
                date = input_font.render(temp[task_num]['date'], True, text_yellow)
                adding_date_backdrop = pygame.draw.rect(screen, date_color, (x, y, 400, 30))
                adding_date_rect = date.get_rect()
                adding_date_rect.topleft = (x+5, y+5)
                screen.blit(date, adding_date_rect)
                y += 40
                if color_to_change == 'date':
                    cursor = pygame.Rect(adding_date_rect.topright, (2, adding_date_rect.height))
                    if time.time() % 1 > 0.5: pygame.draw.rect(screen, text_yellow, cursor)

                
                #Time to start
                instr_left, instr_y = display_prompt('What time do you want to start?', x, y)
                display_instr('(hh:mm AM/PM)', instr_left, instr_y)
                y += 35
                startTime = input_font.render(temp[task_num]['time to start'], True, text_yellow)
                adding_startTime_backdrop = pygame.draw.rect(screen, start_color, (x, y, 400, 30))
                adding_startTime_rect = startTime.get_rect()
                adding_startTime_rect.topleft = (x+5, y+5)
                screen.blit(startTime, adding_startTime_rect)
                y += 40
                if color_to_change == 'start_time':
                    cursor = pygame.Rect(adding_startTime_rect.topright, (2, adding_startTime_rect.height))
                    if time.time() % 1 > 0.5: pygame.draw.rect(screen, text_yellow, cursor)


                #Time
                instr_left, instr_y = display_prompt('How long will it take to complete?', x, y)
                display_instr('(min)', instr_left, instr_y)
                y += 35
                complete_time = input_font.render(temp[task_num]['time to complete'], True, text_yellow)
                adding_time_backdrop = pygame.draw.rect(screen, time_color, (x, y, 400, 30))
                adding_time_rect = complete_time.get_rect()
                adding_time_rect.topleft = (x+5, y+5)
                screen.blit(complete_time, adding_time_rect)
                if color_to_change == 'time':
                    cursor = pygame.Rect(adding_time_rect.topright, (2, adding_time_rect.height))
                    if time.time() % 1 > 0.5: pygame.draw.rect(screen, text_yellow, cursor)


                #Buttons
                global add_done_button, add_cancel_button
                done_button_font = pygame.font.Font('klavika-light.ttf', 30)

                #Change button colors
                done_color = cyan
                cancel_color = cyan
                if colored_button == 'add_task_done':
                    done_color = cyan_active
                if colored_button == 'add_task_cancel':
                    cancel_color = cyan_active
                
                #Done button
                done_button = done_button_font.render('   DONE   ', True, black, done_color)
                add_done_button = done_button.get_rect()
                add_done_button.topright = (695, 535)
                screen.blit(done_button, add_done_button)

                #Cancel Cutton
                cancel_button = done_button_font.render(' CANCEL ', True, black, cancel_color)
                add_cancel_button = cancel_button.get_rect()
                add_cancel_button.topleft = (705, 535)
                screen.blit(cancel_button, add_cancel_button)

            if 'done' in add_func:
                done()
            else:
                if 'title' in add_func: addTask_main('title', button)
                elif 'desc' in add_func: addTask_main('desc', button)
                elif 'priority' in add_func: addTask_main('priority', button)
                elif 'date' in add_func: addTask_main('date', button)
                elif 'time' in add_func: addTask_main('time', button)
                elif 'start' in add_func: addTask_main('start_time', button)
                else: addTask_main('', button)


        def complete_task(complete_func, button):
            clear(button)
            screen_title('COMPLETE A TASK')
            display_tasks(True, False)

            def done():

                global completing
                try:
                    completing = int(completing) - 1
                    keys = list(tasks.keys())
                    my_key = keys[completing]
                    del(tasks[my_key])

                    working['tasks']['completing_task'] = False
                    global func
                    func = 'home screen'

                    completing = ''
                except Exception as e:
                    working['tasks']['completing_task'] = False
                    func = 'home screen'

                    completing = ''

                    
            def complete_main(clicked, colored_button):

                if clicked: color = black_active
                else: color = black

                x = 500 #To position the text box
                y = 90

                #Creates the prompt
                prompt_font = pygame.font.Font('klavika-light.ttf', 25)
                prompt = prompt_font.render('Which task would you like to mark completed?', True, prompt_purple)
                prompt_rect = prompt.get_rect()
                prompt_rect.topleft = (x, y)
                screen.blit(prompt, prompt_rect)
                y += 35 #Moves the instructions down

                #For the prompt instructions
                inst_font = pygame.font.Font('klavika-light.ttf', 20)
                inst = inst_font.render('Please only type in the number.', True, prompt_purple)
                inst_rect = inst.get_rect()
                inst_rect.topleft = (x, y)
                screen.blit(inst, inst_rect)
                y += 30 #Moves the input down

                #For the warning instructions
                warning_font = pygame.font.Font('klavika-light.ttf', 15)
                warning = warning_font.render('This can not be undone.', True, title_yellow)
                warning_rect = warning.get_rect()
                warning_rect.topleft = (x, y)
                screen.blit(warning, warning_rect)
                y += 25 #Moves the input down

                #For the input
                input_font = pygame.font.Font('klavika-light.ttf', 20) #For the inputs
                global complete_backdrop, completing    #Global so that the game loop can see if the mouse clicked it
                user_input = input_font.render(completing, True, text_yellow) #Displays the input
                complete_backdrop = pygame.draw.rect(screen, color, (x, y, 400, 30)) #Black backdrop
                user_input_rect = user_input.get_rect()                              #Rect to hold the text
                user_input_rect.topleft = (x+5, y+5)                                 #Centers the text in the backdrop
                screen.blit(user_input, user_input_rect)                           #Puts the rects onto the screen
                
                #Cursor
                cursor = pygame.Rect(user_input_rect.topright, (2, user_input_rect.height))
                if clicked:
                    if time.time() % 1 > 0.5: pygame.draw.rect(screen, text_yellow, cursor)

                #Buttons
                global complete_done_button, complete_cancel_button
                done_button_font = pygame.font.Font('klavika-light.ttf', 30)

                #Changes the color of the buttons
                done_button_color = cyan
                cancel_button_color = cyan
                if colored_button == 'task_complete_done':
                    done_button_color = cyan_active
                elif colored_button == 'task_complete_cancel':
                    cancel_button_color = cyan_active
                #Done button
                done_button = done_button_font.render('   DONE   ', True, black, done_button_color)
                complete_done_button = done_button.get_rect()
                complete_done_button.topright = (695, 215)
                screen.blit(done_button, complete_done_button)

                #Cancel Cutton
                cancel_button = done_button_font.render(' CANCEL ', True, black, cancel_button_color)
                complete_cancel_button = cancel_button.get_rect()
                complete_cancel_button.topleft = (705, 215)
                screen.blit(cancel_button, complete_cancel_button)

            if 'active' in complete_func:
                complete_main(True, button)
            elif 'done' in complete_func:
                done()
            else:
                complete_main(False, button)



        clear(button)
        if task_func == 'home screen':
            working['tasks']['main'] = True
            screen_title('MANAGE TASKS')
            display_tasks(False, False)
            tasks_buttons(button)
        elif 'add task' in task_func:
            add_task(task_func, button)
        elif 'complete task' in task_func:
            complete_task(task_func, button)
        else:
            working['tasks']['main'] = True
            screen_title('MANAGE TASKS')
            display_tasks(False)
            tasks_buttons()

    def view_schedule(schedule_func, button): # A function that will show the entire schedule
        clear(button)

        #Everything here is a placeholder
        def screen_title():
            font = pygame.font.Font('klavika-light.ttf', 35)
            text = font.render('VIEW SCHEDULE', True, title_yellow)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 30)
            screen.blit(text, text_rect)

        def sort_tasks(): #Sorts the tasks into the apropriate lists.
            #Lists to hold the sorted tasks
            overdue = [] 
            high = []
            med = []
            low = []
            
            today = datetime.now() #Gets today's date for the calcualtions. It is outside the loop because there is no need to have it re-run many times.
            for task in tasks:
                try:
                    date = datetime.strptime(tasks[task]['date'], '%m/%d/%y')
                    diff = today - date #Gets the difference between today's date and the date of the task. 
                    diff = diff.days
                except:
                    diff = -1
                
                if diff > 0: #If the number of days between the date and today it positve, the taskis overdue add its dict key to the overdue list
                    overdue.append(task)
                elif diff == 0: #IF the task is due today
                    try:
                        task_time = datetime.strptime(tasks[task]['time to start'], '%I:%M %p') #Get the time of the task
                        if task_time.hour <= today.hour and task_time.minute < today.minute: #If the tasks's time is before now add it to the overdue task list.
                            overdue.append(task)

                        else: #If the task is due today, but the time hasn't come yet, sort it like any other task.    
                            if 'high' in tasks[task]['priority'].lower(): #If the priority is high, add it to the high list
                                high.append(task)
                            elif 'med' in tasks[task]['priority'].lower(): #If the priority is medium, add it to the med list
                                med.append(task)
                            elif 'low' in tasks[task]['priority'].lower():  #If the priority is low, add it to the low list
                                low.append(task)
                    except:
                        low.append(task) #If the format is wrong and the program can't read it, the task goes into the low list.
                elif 'high' in tasks[task]['priority'].lower(): #If the priority is high, add it to the high list
                    high.append(task)
                elif 'med' in tasks[task]['priority'].lower(): #If the priority is medium, add it to the med list
                    med.append(task)
                elif 'low' in tasks[task]['priority'].lower():  #If the priority is low, add it to the low list
                    low.append(task)
                else:        #If the priority is anything else (i.e. the user screwed it up), add it to the low list.
                    low.append(task)

            return overdue, high, med, low

        def schedule_main():
            overdue, high, med, low = sort_tasks()
            big_schedule_width = 0

            x = 25
            y = 115

            columns = 1 #I only want 4 columns, this will stop a fourth from being created
            count = 1 #To display the task numbers for the complete task function
                
            for task in overdue:
                #Manages columns
                if y > pygame.display.get_surface().get_height() - 100: #If the list of tasks is longer than can fit in one column, start a second column
                    if columns == 4: return #I only want 3 columns, this will stop a third from being created
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created
                    y = 115
                    if columns == 4: big_schedule_width *= 2
                    x = big_schedule_width + 30 #For spacing
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created


                #adds the title for the overdue task in red
                title_font = pygame.font.Font('klavika-light.ttf', 15)
                title = title_font.render(tasks[task]['title'], True, overdue_red)
                title_rect = title.get_rect()
                title_rect.centery = y
                title_rect.left = x
                screen.blit(title, title_rect)
        
                if title_rect.width > big_schedule_width: big_schedule_width = title_rect.width #Puts the width of the widest rect in that variable to maintain spacing
                y += 15
                x += 10

                #overdue task info in yellow
                for item in tasks[task]:
                    if item == 'title': continue #Skip the title
                    font = pygame.font.Font('klavika-light.ttf', 12)
                    description = font.render(tasks[task][item], True, info_color)
                    description_rect = description.get_rect() 
                    description_rect.topleft = (x, y)
                    screen.blit(description, description_rect)
                    if description_rect.width > big_schedule_width: big_schedule_width = description_rect.width #Puts the width of the widest rect in that variable to maintain spacing

                    y += 17

                x -= 10
                y += 20


            for task in high:
                #Manages columns
                if y > pygame.display.get_surface().get_height() - 100: #If the list of tasks is longer than can fit in one column, start a second column
                    if columns == 4: return #I only want 3 columns, this will stop a third from being created
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created
                    y = 115
                    if columns == 4: big_schedule_width *= 2
                    x = big_schedule_width + 30 #For spacing
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created


                #adds the title for the high task in green
                title_font = pygame.font.Font('klavika-light.ttf', 15)
                title = title_font.render(tasks[task]['title'], True, task_green)
                title_rect = title.get_rect()
                title_rect.centery = y
                title_rect.left = x
                screen.blit(title, title_rect)
        
                if title_rect.width > big_schedule_width: big_schedule_width = title_rect.width #Puts the width of the widest rect in that variable to maintain spacing
                y += 15
                x += 10

                #overdue task info in yellow
                for item in tasks[task]:
                    if item == 'title': continue #Skip the title
                    font = pygame.font.Font('klavika-light.ttf', 12)
                    description = font.render(tasks[task][item], True, info_color)
                    description_rect = description.get_rect() 
                    description_rect.topleft = (x, y)
                    screen.blit(description, description_rect)
                    if description_rect.width > big_schedule_width: big_schedule_width = description_rect.width #Puts the width of the widest rect in that variable to maintain spacing

                    y += 17

                x -= 10
                y += 20

                
            for task in med:
                #Manages columns
                if y > pygame.display.get_surface().get_height() - 100: #If the list of tasks is longer than can fit in one column, start a second column
                    if columns == 4: return #I only want 3 columns, this will stop a third from being created
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created
                    y = 115
                    if columns == 4: big_schedule_width *= 2
                    x = big_schedule_width + 30 #For spacing
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created


                #adds the title for the medium task in green
                title_font = pygame.font.Font('klavika-light.ttf', 15)
                title = title_font.render(tasks[task]['title'], True, task_green)
                title_rect = title.get_rect()
                title_rect.centery = y
                title_rect.left = x
                screen.blit(title, title_rect)
        
                if title_rect.width > big_schedule_width: big_schedule_width = title_rect.width #Puts the width of the widest rect in that variable to maintain spacing
                y += 15
                x += 10

                #overdue task info in yellow
                for item in tasks[task]:
                    if item == 'title': continue #Skip the title
                    font = pygame.font.Font('klavika-light.ttf', 12)
                    description = font.render(tasks[task][item], True, info_color)
                    description_rect = description.get_rect() 
                    description_rect.topleft = (x, y)
                    screen.blit(description, description_rect)
                    if description_rect.width > big_schedule_width: big_schedule_width = description_rect.width #Puts the width of the widest rect in that variable to maintain spacing

                    y += 17

                x -= 10
                y += 20


            for task in low:
                #Manages columns
                if y > pygame.display.get_surface().get_height() - 100: #If the list of tasks is longer than can fit in one column, start a second column
                    if columns == 4: return #I only want 3 columns, this will stop a third from being created
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created
                    y = 115
                    if columns == 4: big_schedule_width *= 2
                    x = big_schedule_width + 30 #For spacing
                    columns += 1 #I only want 3 columns, this will stop a fourth from being created


                #adds the title for the low task in green
                title_font = pygame.font.Font('klavika-light.ttf', 15)
                title = title_font.render(tasks[task]['title'], True, task_green)
                title_rect = title.get_rect()
                title_rect.centery = y
                title_rect.left = x
                screen.blit(title, title_rect)
        
                if title_rect.width > big_schedule_width: big_schedule_width = title_rect.width #Puts the width of the widest rect in that variable to maintain spacing
                y += 15
                x += 10

                #overdue task info in yellow
                for item in tasks[task]:
                    if item == 'title': continue #Skip the title
                    font = pygame.font.Font('klavika-light.ttf', 12)
                    description = font.render(tasks[task][item], True, info_color)
                    description_rect = description.get_rect() 
                    description_rect.topleft = (x, y)
                    screen.blit(description, description_rect)
                    if description_rect.width > big_schedule_width: big_schedule_width = description_rect.width #Puts the width of the widest rect in that variable to maintain spacing

                    y += 17

                x -= 10
                y += 20




        if schedule_func == 'home screen':
            screen_title()
            schedule_main()

    def home(button): #Creates the home screen
        
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
            def start_end_dates(): #Finds the day of the month to start and end on.
                #To keep track of the number of days per month
                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                months_30_days = ['April', 'June', 'September', 'November']
                months_31_days = ['January', 'March', 'May', 'July', 'August', 'October', 'December']

                today = datetime.now()
                #Finds the number of days in the current month
                if months[today.month - 1] in months_30_days: #-1 because the index starts at 0
                    current_end_day = 30
                elif months[today.month - 1] in months_31_days:
                    current_end_day = 31

                
                #finds the number of days in the previous month
                if months[today.month - 2] in months_31_days: #-1 because the index starts at 0, -1 to get the previous month
                    working_end_day = 31
                elif months[today.month - 2] in months_30_days:
                    working_end_day = 30
                else:
                    working_end_day = 28
                
                
                if date(today.year, today.month, 1).isoweekday() == 7: #If the week starts on Sunday
                    start_date = 1
                    current_month = True #To keep track of when to go back to day 1
                else:   
                    #Finds the start day
                    start_date = date(22, today.month-1, (working_end_day - (date(22, today.month, 1).isoweekday() - 1))).day
                    current_month = False #To keep track of when to go back to day 1
                return(start_date, working_end_day, current_end_day, current_month)
            
            
            cal_width = pygame.display.get_surface().get_width()/7 #Divides the width of the screen by 7 so that the calendar takes up the width of the entire screen even if the user resizes.
            global cal_top
            cal_top = height * .42
            cal_height = (height - cal_top - 10 - 10) / 5 # -10 so there is a bit of space at the bottom and -10 because of the days labels
            x = 0 #Starts the calendar at the left edge
            y = cal_top + 10 #Keeps the calendar at the bottom of the screen
            month_font = pygame.font.Font('C:\Windows\Fonts\consola.ttf', 25) #Font to display name of the month
            day_font = pygame.font.Font('C:\Windows\Fonts\consola.ttf', 10)     #Font to display weekdays


            #Name of the month
            month = datetime.now().strftime('%B')
            month = month_font.render(month, True, title_yellow)
            month_rect = month.get_rect()#Creates rect object for the name of the month
            month_rect.bottomleft = (0, cal_top - 20)
            screen.blit(month, month_rect)

            #Weekdays
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            for weekday in days:
                day_text = day_font.render(weekday, True, title_yellow)
                day_rect = day_text.get_rect()
                day_rect.topleft = (cal_width * (days.index(weekday)), cal_top - 5)
                screen.blit(day_text, day_rect)

            day, working_end_day, current_end_day, current_month = start_end_dates() #Finds the day of the month to start on, the last day of the previous month, the last day of the current month, and if it needs to start on a previous month to fill the calendar properly

            
            for i in range(5): #Creates 5 rows
                for i in range(7): #Creates 7 days in a row
                    pygame.draw.rect(screen, grey, (x, y, cal_width, cal_height), 1)  # Creates the box for each day
                    if not current_month and day > working_end_day: 
                        day = 1 #Resets the day to the current month (from the previous one)
                        current_month = True #Now the 
                    elif current_month and day > current_end_day:
                        day = 1 #Resets the day for the next month
                    set_nums(x, y, day) #Adds the number to the box
                    x += cal_width #Adds to the x variable so the next square is not in the same place
                    day += 1 #Adds one to the day variable to raise the number in the day 
                x = 0 #Moves the x variable back to 0 so the next row starts on the left edge
                y += cal_height #Moves the next row down


        def list_tasks(): # Shows the list of tasks on the home screen
            
            def title(): #A function that creates the title for the page
                #Creates the text and rect objects for the title
                font = pygame.font.Font('klavika-light.ttf', 30)
                text = font.render('TASKS', True, title_yellow)
                text_rect = text.get_rect()
                x = (width - biggest_width - 20) / 3 
                text_rect.center = (x, 30)
                screen.blit(text, text_rect)

            def show_tasks(): #Displays the task list
                # x and y coordinates for the tasks
                y = 50 
                x = 1.5 * (width / 7)
                big_task_width = 0 #To Figure out the width of the widest text so the next column does not overlap.
                second_column = False #I only want 2 columns, this will stop a third from being created

                for task in tasks:
                    if task == 'completing': continue
                    if y > cal_top - 35: #If the list of tasks is longer than can fit in one column, start a second column
                        continue
                        
                    # Displays the title and descrition of each task
                    title_font = pygame.font.Font('klavika-light.ttf', 15)
                    title = title_font.render(tasks[task]['title'], True, task_blue)
                    title_rect = title.get_rect() 
                    title_rect.topleft = (x, y)
                    desc = title_font.render(tasks[task]['description'], True, info_color)
                    desc_rect = desc.get_rect() 
                    desc_rect.topleft = (x + 10, y + 15)
                    if title_rect.width > big_task_width: #Figures out the width of the widest text so the next column does not overlap.
                        big_task_width = title_rect.width
                    if desc_rect.width > big_task_width + 10:
                        big_task_width = desc_rect.width

                    screen.blit(title, title_rect)
                    screen.blit(desc, desc_rect)
                    y += 40

            title()
            show_tasks()


        def schedule(): # Displays the schedule on the home screen
            width = pygame.display.get_surface().get_width() # Gets the width of the screen
            working_width = ((width - biggest_width) / 2 ) - 20
            working_width = working_width + working_width 

            def title():
                font = pygame.font.Font('klavika-light.ttf', 30)
                text = font.render('SCHEDULE', True, title_yellow)
                text_rect = text.get_rect()
                x = 2 * ((width - biggest_width -20 ) / 3 )
                text_rect.center = (x, 30)
                screen.blit(text, text_rect)

                global schedule_left 
                schedule_left = text_rect.left

            def display_schedule():

                #FINDS THE TASKS TO BE DISPLAYED   
                task_count = 0
                #Lists to hold the sorted tasks
                overdue = [] 
                high = []
                med = []
                low = []
                to_do_list = []  
                
                #Finds and sorts the tasks
                today = datetime.now() #Gets today's date for the calcualtions. It is outside the loop because there is no need to have it re-run many times.
                for task in tasks:
                    try:
                        date = datetime.strptime(tasks[task]['date'], '%m/%d/%y')
                        diff = today - date #Gets the difference between today's date and the date of the task. 
                        diff = diff.days
                    except:
                        diff = -1
                    if diff > 0: #If the number of days between the date and today it positve, the task is overdue add its dict key to the overdue list
                        overdue.append(task)
                    elif diff == 0: #If the task is due today
                        try:
                            task_time = datetime.strptime(tasks[task]['time to start'], '%I:%M %p') #Get the time of the task
                            if task_time.hour <= today.hour and task_time.minute < today.minute: #If the tasks's time is before now add it to the overdue task list.
                                overdue.append(task)

                            else: #If the task is due today, but the time hasn't come yet, sort it like any other task.    
                                if 'high' in tasks[task]['priority'].lower(): #If the priority is high, add it to the high list
                                    high.append(task)
                                elif 'med' in tasks[task]['priority'].lower(): #If the priority is medium, add it to the med list
                                    med.append(task)
                                elif 'low' in tasks[task]['priority'].lower():  #If the priority is low, add it to the low list
                                    low.append(task)
                        except:
                            low.append(task)     
                    elif 'high' in tasks[task]['priority'].lower(): #If the priority is high, add it to the high list
                        high.append(task)
                    elif 'med' in tasks[task]['priority'].lower(): #If the priority is medium, add it to the med list
                        med.append(task)
                    elif 'low' in tasks[task]['priority'].lower():  #If the priority is low, add it to the low list
                        low.append(task)
                    else:        #If the priority is anything else (i.e. the user screwed it up), add it to the low list.
                        low.append(task)
                
                #Adds the tasks to the to_do_list list in order or priority.
                
                for high_task in high:
                    to_do_list.append(high_task) 
                for med_task in med:
                    to_do_list.append(med_task)
                for low_task in low:
                    to_do_list.append(low_task)   
                

                #DISPLAY THE TASKS
                x = schedule_left
                y = 50


                for task in overdue: #Overdue tasks 
                    
                    if y >= cal_top - 35: continue #don't do anything on this iteration of the loop if the tasks will go onto the calendar 
                    title_font = pygame.font.Font('klavika-light.ttf', 15)
                    title = title_font.render(tasks[task]['title'], True, overdue_red, bg)
                    title_rect = title.get_rect() 
                    title_rect.topleft = (x, y)

                    start = title_font.render(f'Start At: {tasks[task]["time to start"]}', True, info_color, bg)
                    start_rect = start.get_rect()
                    start_rect.topleft = (x + 30, y + 15)

                
                    screen.blit(title, title_rect)
                    screen.blit(start, start_rect)
                    y += 40

                for task in to_do_list: #All other tasks in order of priority 
                    if y > cal_top - 35: continue #don't do anything on this iteration of the loop
                    title_font = pygame.font.Font('klavika-light.ttf', 15)
                    title = title_font.render(tasks[task]['title'], True, task_green)
                    title_rect = title.get_rect() 
                    title_rect.topleft = (x, y)

                    start = title_font.render(f'Start At: {tasks[task]["time to start"]}', True, info_color, bg)
                    start_rect = start.get_rect()
                    start_rect.topleft = (x + 30, y + 15)

                    
                    screen.blit(title, title_rect)
                    screen.blit(start, start_rect)
                    y += 40
                
            title()
            display_schedule()



        def buttons(button): #Creates the buttons at the left of the screen 
            font = pygame.font.Font('klavika-light.ttf', 20)
            buttons_list = ['', ' MANAGE TASKS ', ' VIEW SCHEDULE ', ''] # List of buttons. The empty strings at the start and end maintain spacing. The spaces at he begining and end of each word are for the same reason
            y = 2 * (250/len(buttons_list))
            biggest_width = 0 # Will hold the width of the widest button to maintain spacing with other objects.

            global manageTasks_rect, viewSchedule_rect #Making these variables global lets you see if the mouse is clicking them as buttons

            #Changes the color of the buttons
            tasks_button_color = cyan
            schedule_button_color = cyan
            if button == 'manage_tasks':
                tasks_button_color = cyan_active
            elif button == 'manage_schedule':
                schedule_button_color = cyan_active


            # Button for adding a task
            manageTasks_text = font.render(buttons_list[1], True, black, tasks_button_color)
            manageTasks_rect = manageTasks_text.get_rect()
            manageTasks_rect.topleft = (5, y)
            screen.blit(manageTasks_text, manageTasks_rect)
            if manageTasks_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
                biggest_width = manageTasks_rect.width
            y += 250/len(buttons_list) #Moves the next button farther down



            # Button for deleting a task
            viewSchedule_text = font.render(buttons_list[2], True, black, schedule_button_color)
            viewSchedule_rect = viewSchedule_text.get_rect()
            viewSchedule_rect.topleft = (5, y)
            screen.blit(viewSchedule_text, viewSchedule_rect)
            if viewSchedule_rect.width > biggest_width: #Sets the value of biggest_width to the width of that rect if it is larger than the current value of biggest_width
                biggest_width = viewSchedule_rect.width
            y += 250/len(buttons_list) #Moves the next button farther down


            


        screen.fill(bg)
        global running_schedule, running_tasks
        working['schedule']['running'] = False #Keeps the schedule and task functions from being run until it's the correct time.
        working['tasks']['running'] = False
        create_calendar()
        buttons(button)
        list_tasks()
        schedule()

    #User Events

    #Event to check when notificatins should be sent and send them
    CHECK_NOTIFICATION = pygame.USEREVENT + 1
    pygame.time.set_timer(CHECK_NOTIFICATION, 60000) #This event will happen every 1 minute
    #Event to save the tasks in the tasks dict to the tasks.json file.
    SAVETASKS  = pygame.USEREVENT + 2 
    pygame.time.set_timer(SAVETASKS, 900000) #This event will happen every 15 minutes


    # Game Processing
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
            'adding_title': False, #Controlling what key presses do
            'adding_desc': False, #Controlling what key presses do
            'adding_priority': False, #Controlling what key presses do
            'adding_date': False, #Controlling what key presses do
            'adding_time': False, #Controlling what key presses do
            'adding_start': False, #Controlling what key presses do
            'completing_task': False, #Keeps the complete_task function from being run
            'completing_task_editing': False, #Controlling what key presses do
        }
    }


    global width, func, button_color # A variable to keep the width of the window, a variable to keep track of what nested function(s) should be running, and a variable to change the color of buttons when the mouse is over them
    button_color = '' #All buttons should be the original color

    # The game loop
    start_up()


    running = True
    while running:

        width = pygame.display.get_surface().get_width() #It is inside the loop so that it changes if the window is resized
        height = pygame.display.get_surface().get_height() #It is inside the loop so that it changes if the window is resized

        for event in pygame.event.get(): #Manage events
            #If the user hits the close button.
            if event.type == pygame.QUIT:
                running = False
                shut_down()
            
            elif event.type == CHECK_NOTIFICATION: 
                desktop_notifications()

            elif event.type == SAVETASKS:
                shut_down()
                start_up() 

            elif event.type == pygame.MOUSEBUTTONDOWN:  
                mouse_pos = pygame.mouse.get_pos()
                
                if working['home']['start']: #makes the functions that will lead to the pages off the home screen
                    if manageTasks_rect.collidepoint(mouse_pos):
                        working['home']['start'] = False
                        working['schedule']['running'] = False
                        working['tasks']['running'] = True
                        func = 'home screen'

                    elif viewSchedule_rect.collidepoint(mouse_pos):
                        working['home']['start'] = False
                        working['tasks']['running'] = False
                        working['schedule']['running'] = True
                        func = 'home screen'

                elif not working['home']['start']: #Makes the home button on every page but the home screen
                    if home_rect.collidepoint(mouse_pos):
                        working['home']['start'] = True
                        home(button_color)

                
                if working['tasks']['running']: # To hande the events in the tasks
                    if working['tasks']['main']:
                        #Handles the events in the main page
                        if addTask_rect.collidepoint(mouse_pos): #If the button to add a task is clicked
                            #Makes sure that only the function to add a task runs.
                            working['tasks']['main'] = False
                            working['tasks']['editing_task'] = False
                            working['tasks']['completing_task'] = False
                            working['tasks']['adding_task'] = True
                            func = 'add task'
                        
                        elif completeTask_rect.collidepoint(mouse_pos): #If the button to complete a task is clicked
                            #Makes sure that only the function to add a task runs.
                            working['tasks']['main'] = False
                            working['tasks']['adding_task'] = False
                            working['tasks']['completing_task_editing'] = True
                            func = 'complete task'

                    elif working['tasks']['adding_task']:
                        if adding_title_backdrop.collidepoint(mouse_pos):  #Add to title
                            #So that the keys being pressed only add to the title
                            working['tasks']['adding_title'] = True
                            working['tasks']['adding_desc'] = False
                            working['tasks']['adding_priority'] = False
                            working['tasks']['adding_date'] = False
                            working['tasks']['adding_time'] = False
                            working['tasks']['adding_start'] = False

                            func = 'add task title' #When the title text box is selected, this will tell it to change the color
                        
                        elif adding_desc_backdrop.collidepoint(mouse_pos):  #Adding to description
                            #So that the keys being pressed only add to the description
                            working['tasks']['adding_title'] = False
                            working['tasks']['adding_desc'] = True
                            working['tasks']['adding_priority'] = False
                            working['tasks']['adding_date'] = False
                            working['tasks']['adding_time'] = False
                            working['tasks']['adding_start'] = False

                            func = 'add task desc' #When the description text box is selected, this will tell it to change the color
                        
                        elif adding_priority_backdrop.collidepoint(mouse_pos): #Adding to priority
                            #So that the keys being pressed only add to the priority
                            working['tasks']['adding_title'] = False
                            working['tasks']['adding_desc'] = False
                            working['tasks']['adding_priority'] = True
                            working['tasks']['adding_date'] = False
                            working['tasks']['adding_time'] = False
                            working['tasks']['adding_start'] = False

                            func = 'add task priority' #When the priority text box is selected, this will tell it to change the color

                        elif adding_date_backdrop.collidepoint(mouse_pos):  #Adding to the date
                            #So that the keys only add to the date
                            working['tasks']['adding_title'] = False
                            working['tasks']['adding_desc'] = False
                            working['tasks']['adding_priority'] = False
                            working['tasks']['adding_date'] = True
                            working['tasks']['adding_time'] = False
                            working['tasks']['adding_start'] = False

                            func = 'add task date' #When the date text box is selected, this will tell it to change the color

                        elif adding_time_backdrop.collidepoint(mouse_pos): #Adding to the time
                            #So that the keys only add to the time
                            working['tasks']['adding_title'] = False
                            working['tasks']['adding_desc'] = False
                            working['tasks']['adding_priority'] = False
                            working['tasks']['adding_date'] = False
                            working['tasks']['adding_start'] = False
                            working['tasks']['adding_time'] = True

                            func = 'add task time' #When the time text box is selected, this will tell it to change the color
                        
                        elif adding_startTime_backdrop.collidepoint(mouse_pos): #Adding to the start time
                            #So that the keys only add to the start time
                            working['tasks']['adding_title'] = False
                            working['tasks']['adding_desc'] = False
                            working['tasks']['adding_priority'] = False
                            working['tasks']['adding_date'] = False
                            working['tasks']['adding_start'] = True
                            working['tasks']['adding_time'] = False 

                            func = 'add task start'

                        elif add_done_button.collidepoint(mouse_pos): #Done button
                            #Make the textboxes stop working
                            working['tasks']['adding_title'] = False
                            working['tasks']['adding_desc'] = False
                            working['tasks']['adding_priority'] = False
                            working['tasks']['adding_date'] = False
                            working['tasks']['adding_time'] = False 
                            working['tasks']['adding_start'] = False


                            func = 'add task done'

                        elif add_cancel_button.collidepoint(mouse_pos): #Cancel buttom
                            func = 'home screen'
                            working['tasks']['adding_task'] = False
                        
                        else:
                            #So that the keys don't add to anything if the user clicks outside the rect
                            working['tasks']['adding_title'] = False
                            working['tasks']['adding_desc'] = False
                            working['tasks']['adding_priority'] = False
                            working['tasks']['adding_date'] = False
                            working['tasks']['adding_time'] = False
                            working['tasks']['adding_start'] = False

                            func = 'add task'


                    elif working['tasks']['completing_task_editing']:
                        if complete_backdrop.collidepoint(mouse_pos):  #Makes the box change color when clicked
                            func = 'complete task active' #When the title text box is selected, this will tell it to change the color
                        else:               #Changes the color of the box back to the original color
                            func = 'complete task'
                        if complete_done_button.collidepoint(mouse_pos): #Done button
                            #Make the textboxes stop working
                            working['tasks']['completing_task_editing'] = False 
                            func = 'complete task done'

                        elif complete_cancel_button.collidepoint(mouse_pos): #Cancel buttom
                            func = 'home screen'
                            working['tasks']['completing_task'] = False
                        
            elif event.type == pygame.KEYDOWN:
                if working['tasks']['running']:
                    if working['tasks']['adding_title']:   #For the title
                        if event.key == pygame.K_BACKSPACE:  #Process backspace - the following lines are the same
                            temp[task_num]['title'] = temp[task_num]['title'][:-1]
                        else:                               #Process key presses - the following lines are the same
                            temp[task_num]['title'] += event.unicode
                    if working['tasks']['adding_desc']:
                        if event.key == pygame.K_BACKSPACE: #For the description
                            temp[task_num]['description'] = temp[task_num]['description'][:-1]
                        else:
                            temp[task_num]['description'] += event.unicode
                    if working['tasks']['adding_priority']: #For the priority
                        if event.key == pygame.K_BACKSPACE:
                            temp[task_num]['priority'] = temp[task_num]['priority'][:-1]
                        else:
                            temp[task_num]['priority'] += event.unicode
                    if working['tasks']['adding_date']:   #For the date
                        if event.key == pygame.K_BACKSPACE:
                            temp[task_num]['date'] = temp[task_num]['date'][:-1]
                        else:
                            temp[task_num]['date'] += event.unicode
                    if working['tasks']['adding_time']:  #For the time
                        if event.key == pygame.K_BACKSPACE:
                            temp[task_num]['time to complete'] = temp[task_num]['time to complete'][:-1]
                        else:
                            temp[task_num]['time to complete'] += event.unicode
                    if working['tasks']['adding_start']: #For the start time
                        if event.key == pygame.K_BACKSPACE:
                            temp[task_num]['time to start'] = temp[task_num]['time to start'][:-1]
                        else:
                            temp[task_num]['time to start'] += event.unicode
                    if working['tasks']['completing_task_editing']: #To complete a task
                        global completing #needs to be global so it can be accessed inside the function
                        if event.key == pygame.K_BACKSPACE:
                            completing = completing[:-1]
                        else:
                            completing += event.unicode
           
            elif event.type == pygame.MOUSEMOTION: #To change the color of buttons when the mouse hovers over them
                mouse_pos = pygame.mouse.get_pos()
                try: #A try and except is necessary because otherwise the program will crash at the start because the buttons have not yet been created. 

                    button_color = ''
                    if working['home']['start']: #makes the functions that will lead to the pages off the home screen
                        if manageTasks_rect.collidepoint(mouse_pos): #Changes the color of the tasks button
                            button_color = 'manage_tasks'
                        elif viewSchedule_rect.collidepoint(mouse_pos): #Changes the color of the schedule button
                            button_color = 'manage_schedule'
                        else: #Sets all button back to their original color
                            button_color = ''
                    #START COMMENT HERE FOR DEBUGGING
                    elif working['tasks']['running']: # To hande the events in the tasks
                        if working['tasks']['main']:
                            #Handles the events in the main page
                            if addTask_rect.collidepoint(mouse_pos): #If the button to add a task is clicked
                                button_color = 'add_task'
                            elif completeTask_rect.collidepoint(mouse_pos): #If the button to complete a task is clicked
                                button_color = 'complete_task'
                            else: button_color = ''

                        elif working['tasks']['adding_task']:
                            if add_done_button.collidepoint(mouse_pos): #Done button
                                button_color = 'add_task_done'
                            elif add_cancel_button.collidepoint(mouse_pos): #Cancel buttom
                                button_color = 'add_task_cancel'
                            else:
                                button_color = ''

                        elif working['tasks']['completing_task_editing']:
                            if complete_done_button.collidepoint(mouse_pos): #Done button
                                button_color = 'task_complete_done'

                            elif complete_cancel_button.collidepoint(mouse_pos): #Cancel buttom
                                button_color = 'task_complete_cancel'
                            else: button_color = ''
                    #END COMMENT HERE
                    #elif working['tasks']['running']: pass
                    elif working['schedule']['running']: pass
                    else: #Otherwise all buttons should be the original color
                        button_color = ''
                    if not working['home']['start']: #To change the color of the home button
                        if home_rect.collidepoint(mouse_pos):
                            button_color = 'home'
                        else: 
                            if button_color == 'home':
                                button_color = ''
                except: None



        if working['home']['start']: home(button_color)
        elif working['schedule']['running']: view_schedule(func, button_color)
        elif working['tasks']['running']: manage_tasks(func, button_color)

        date_time_label()
        pygame.display.flip()

    pygame.quit()
    
def desktop_notifications(start = False): #Notify the user about tasks that need to be done. At the start of the program, there should be a notification with overdue tasks. The start arg controls this.

    msg = '' #To hold the message of the task
    task_count = 0 #Number of tasks to notify about
 

    if start:
        today = datetime.now()
        
        #Find the tasks. 
        notif_tasks = {}
        #Add the contents of the task.json file to the tasks dictionary.
        try:
            with open('tasks.json') as file:
                raw = load(file)
            notif_tasks.update(raw)
        except Exception as e:
            pass 

        for task in notif_tasks:
            try:
                date = datetime.strptime(notif_tasks[task]['date'], '%m/%d/%y')
                diff = today - date #Gets the difference between today's date and the date of the task. 
                diff = diff.days
            except:
                diff = -1
            if diff == 0: #If the task is for today
                task_time = datetime.strptime(notif_tasks[task]['time to start'], '%I:%M %p')
                if task_time.hour <= today.hour and task_time.minute < today.minute: #If the task's time is before now
                    #Add info to the notification message
                    if task_count > 0: msg += ', '
                    msg += notif_tasks[task]['title']
                    task_count += 1
            elif diff > 0: #If the number of days between the date and today it positve, the task is overdue. Send a notification about it.
                if task_count > 0: msg += ', '
                msg += notif_tasks[task]['title']
                task_count += 1
        #Add the title to the notification
        if task_count == 1: title = 'You have 1 overdue task to do.'
        else: title = f'You have {task_count} overdue tasks to do.'
        
    else:
        
        global todays_tasks

        for item in todays_tasks:
            try: 
                task_time =  datetime.strptime(tasks[item]['time to start'], '%I:%M %p') #Find the time of the task
                #Check to see if the time on the task is the same time as now
                if datetime.now().hour == task_time.hour and datetime.now().minute == task_time.minute:
                    #Add the title and description of the task to the notification message
                    msg += tasks[item]['title']
                    msg += ' - '
                    msg += tasks[item]['description']
                    msg += '\n'
                    task_count += 1
            except Exception as e:
                pass
        
        #Add the title to the notification
        if task_count == 1: title = 'You have 1 task to do.'
        else: title = f'You have {task_count} tasks to do.'
   
   
    #Send the notification if there is one to send
    if msg != '':
        #To format the notifications
        name = 'Head In The Game'
        icon = 'logo.ico'

        #Send the notification
        notification.notify(
            title = title,
            message = msg,
            app_name = name,
            app_icon = icon,
        )



desktop_notifications(True) #Send the notification with overdue tasks.
main()
