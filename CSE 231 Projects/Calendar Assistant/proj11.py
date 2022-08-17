"""
CSE Project #11 - Calendar Assistant

Description

    This calendar assistant records and updates events. It is 
    implemented using two classes and a driver. It uses a
    24-hour clock and mm/dd/yyyy date formatting. For a
    detailed description, read "Project11.pdf"

Notable Methods of Implementation

    classes, lists, functions, try-except statements

Algorithm

    create calendar
        create P11_Calendar instance
    
    prompt for desired option
        if a:
            prompt for event until valid
            add event if no time conflicts
        if d:
            prompt for event details
            delete event if it exists
        if l:
            prompt for date whose events to list
            list date's events if date is valid and events exist
        if q:
            end program
"""

from p11_calendar import P11_Calendar
from p11_event import P11_Event

MENU = '''Welcome to your own personal calender.
  Available options:
    (A)dd an event to calender
    (D)elete an event
    (L)ist the events of a particular date
    (Q)uit'''

def check_time(time, duration):
    """
    return True if time and duration are valid, and False otherwise
    """
    
    # duration
    
    """
    ensure duration is positive integer
    return False otherwise
    """
    try:
        
        if not duration > 0:
            
            return False

    except TypeError:
    
        print("heehee")
    
        return False
    
    # time
    
    if time != None:

        time_list = time.split(":")
        
        # ensure list is correct length
        if len(time_list) != 2:

            return False
        
        else:
                
            # ensure minute format is valid
            if len(time_list[1]) != 2:
                        
                return False
                
            """
            convert elements in list to integers and continue testing
            return False if elements not integers
            """
            try:
    
                for index, element in enumerate(time_list):
    
                    time_list[index] = int(element)
    
            except ValueError:
    
                return False
    
            else:
    
                # ensure hour is valid
                if not 6 <= time_list[0] <= 17:
    
                    return False
    
                # ensure minutes are valid
                if not 0 <= time_list[1] <= 59:
    
                    return False
                
                # ensure event won't end after latest allowed time
                if time_list[0] * 60 + time_list[1] + int(duration) > 1020:
                    
                    return False
                
    else:
            
        return False
    
    # return True if all tests passed
    return True
            
def event_prompt():
    """
    return event with desired details

    reprompt as necessary until event is valid
    """
    
    # prompt for desired event details
    desired_date_str = input("Enter a date (mm/dd/yyyy): ")
    desired_start_time_str = input("Enter a start time (hh:mm): ")
    desired_duration_int = int(input("Enter the duration in minutes (int): "))
    desired_event_type = \
        input("Enter event type ['meeting','event','appointment','other']: ")
    
    # if start time or duration is invalid, mark event as invalid
    if check_time(desired_start_time_str, desired_duration_int) == False:
        
        valid_event = False
        
    else:
        
        valid_event = True
    
    # make event
    desired_event = P11_Event(desired_date_str, desired_start_time_str, \
                              desired_duration_int, desired_event_type)
    
    # if event's valid attribute is False, mark event as invalid
    if desired_event.valid == False:
        
        valid_event = False
        
    
    # reprompt for event details until valid event created
    while valid_event == False:
        
        print("Invalid event. Please try again.")
        
        # prompt for desired event details
        desired_date_str = input("Enter a date (mm/dd/yyyy): ")
        desired_start_time_str = input("Enter a start time (hh:mm): ")
        desired_duration_int = int(input("Enter the duration in minutes (int): "))
        desired_event_type = \
            input("Enter event type ['meeting','event','appointment','other']: ")
        
        # if start time or duration is invalid, mark event as invalid
        if not check_time(desired_start_time_str, desired_duration_int):
            
            valid_event = False
            
        else:
            
            valid_event = True
        
        desired_event = P11_Event(desired_date_str, desired_start_time_str, \
                                  desired_duration_int, desired_event_type)
        
        # if event's valid attribute is False, mark event as invalid
        if desired_event.valid == False:
            
            valid_event = False
    
    return desired_event
    
def main():
    
    print(MENU)
    
    # initialize calendar
    calendar = P11_Calendar()
    
    # prompt for option
    desired_option_str = input("Select an option: ").lower()
    
    # execute for all non-q options
    while desired_option_str != "q":
        
        # add event
        if desired_option_str == "a":
            
            # prompt for event until valid
            event = event_prompt()
            
            print("Add Event")
            
            # add event and return True or return False
            add_event_Bool = calendar.add_event(event)
            
            if add_event_Bool:
                
                print("Event successfully added.")
                
            else:
                
                print("Event was not added.")
        
        # delete event
        elif desired_option_str == "d":
            
            print("Delete Event")
            
            # prompt for details of desired event
            desired_date_str = input("Enter a date (mm/dd/yyyy): ")
            desired_start_time_str = input("Enter a start time (hh:mm): ")
            
            # delete event and return True or return False
            delete_event_Bool = calendar.delete_event(desired_date_str, \
                                                      desired_start_time_str)
            
            if delete_event_Bool:
                
                print("Event successfully deleted.")
                
            else:
                
                print("Event was not deleted.")
        
        # list events on date
        elif desired_option_str == "l":
            
            print("List Events")
            
            # prompt for desired date
            desired_date_str = input("Enter a date (mm/dd/yyyy): ")
            
            # return list of date's events or empty list if date invalid/no events
            list_events_list = calendar.day_schedule(desired_date_str)
            
            if list_events_list == []:
                
                print("No events to list on  " + desired_date_str)
                
            else:
                
                # print string of each event in list if unempty
                for event in list_events_list:
                    
                    print(event.__str__())
        
        print(MENU)
        
        # reprompt for option
        desired_option_str = input("Select an option: ").lower()

            
if __name__ == '__main__':
    
    main()
