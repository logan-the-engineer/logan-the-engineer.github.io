"""
CSE Project #11

class for calendar objects used in personalized calendar program
"""

class P11_Calendar():
    def __init__(self):
        """
        initialize calendar with empty event_list
        """
        
        self.event_list = []
        
    def add_event(self,e):
        """
        append event e to event_list attribute if no time conflicts
        """
        
        """
        check for time conflicts if event_list isn't empty
        
        append new event to event_list and return True otherwise
        """
        if len(self.event_list) != 0:
        
            # iterate through each event in event_list
            for event in self.event_list:
                
                # create variables for start and end times of new and existing event
                existing_event_start, existing_event_end = event.get_time_range()
                
                new_event_start, new_event_end = e.get_time_range()
                
                """
                return False if start or end times of new event is during
                 existing event on same day
                 
                append new event to event_list and return True otherwise
                """
                if event.date == e.date and (new_event_start in \
                    range(existing_event_start, existing_event_end+1) or \
                        new_event_end in \
                            range(existing_event_start, existing_event_end+1)):
                    
                    return False
                    
            self.event_list.append(e)
                    
            return True
        
        else:
            
            self.event_list.append(e)
            
            return True
    
    def delete_event(self,date,time):
        """
        delete event at specified date and time from self.event_list and return True
        
        if unable to delete, return False
        """
        
        # return False if event_list empty
        if len(self.event_list) == 0:
            
            return False
        
        else:
            
            # iterate through each event in event_list
            for index, event in enumerate(self.event_list):
                
                # delete event and return True if date and time match specified ones
                if event.date == date and event.time == time:
                    
                    del self.event_list[index]
        
                    return True
            
            # return False if no deletion occurs
            return False
    
    def day_schedule(self,date):
        """
        return list of events on specified date
    
        list sorted by events' times in increasing order
        """
        
        # check if date is valid
        
        date_list = date.split("/")

        # ensure list and year are correct length
        if len(date_list) != 3:

            return []
            
        else:
            
            # ensure year is valid
            if len(date_list[2]) != 4:
    
                return []
            
            """
            convert elements in list to integers and continue testing
            Return empty list if elements not integers
            """
            try:
    
                for index, element in enumerate(date_list):
    
                    date_list[index] = int(element)
    
            except ValueError:
    
                return []
    
            else:
    
                # ensure month is valid
                if not 1 <= date_list[0] <= 12:
    
                    return []
    
                # ensure day is valid
                if not 1 <= date_list[1] <= 31:
    
                    return []
    
                # ensure year is valid
                if not 0 <= date_list[2] <= 10000:
    
                    return []
        
        # list of events on specified date
        events_on_date = []
        
        # iterate through each event in event_list
        for event in self.event_list:
            
            # append event and its time to events_on_date
            if event.date == date:
                
                event_time_hours, event_time_mins = event.time.split(":")
                
                event_time_int = int(event_time_hours) * 60 + int(event_time_mins)
                
                events_on_date.append([event_time_int, event])
        """
        list of events resulting from sorting events_on_date by times in
         increasing order
        """
        events_on_date_sorted = [event_on_date[1] for event_on_date in sorted(events_on_date)]
        
        return events_on_date_sorted
           
    def __str__(self):
        """
        return string representing events in calendar
        """
        
        result_str = "Events in Calendar:\n"
        
        # print each event on a new line
        for event in self.event_list:
            
            result_str += event.__str__() + ("\n")
    
        return result_str
    
    def __repr__(self):
        s = ''
        for e in self.event_list:
            s += e.__repr__() + ";"
        return s[:-1]
    
    def __eq__(self,cal):
        '''PROVIDED: returns True if all events are the same.'''
        if not isinstance(cal,P11_Calendar):
            return False
        if len(self.event_list) != len(cal.event_list):
            return False
        L_self = sorted(self.event_list)
        L_e = sorted(cal.event_list)
        for i,e in enumerate(L_self):
            if e != L_e[i]:
                return False
        return True
        
