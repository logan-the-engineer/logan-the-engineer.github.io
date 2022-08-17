"""
CSE Project #11

class for event objects used in personalized calendar program
"""

CAL_TYPE = ['meeting', 'event', 'appointment', 'other']


class P11_Event():
    def __init__(self, date=None, time='9:00', duration=60, cal_type='meeting'):
        """
        initialize event with specified date, time, duration, and type
        """
        
        # date
        
        if date != None:
            
            self.date = date
            
            date_list = date.split("/")
    
            # ensure list and year are correct length
            if len(date_list) != 3:
    
                self.date = None
                
            else:
                
                # ensure year is valid
                if len(date_list[2]) != 4:
        
                    self.date = None
                
                """
                convert elements in list to integers and continue testing
                assign None if elements not integers
                """
                try:
        
                    for index, element in enumerate(date_list):
        
                        date_list[index] = int(element)
        
                except ValueError:
        
                    self.date = None
        
                else:
        
                    # ensure month is valid
                    if not 1 <= date_list[0] <= 12:
        
                        self.date = None
        
                    # ensure day is valid
                    if not 1 <= date_list[1] <= 31:
        
                        self.date = None
        
                    # ensure year is valid
                    if not 0 <= date_list[2] <= 10000:
        
                        self.date = None        
            
        else:
            
            self.date = date
            
        # time
        
        if time != None:
            
            self.time = time
    
            time_list = time.split(":")
            
            # ensure list is correct length
            if len(time_list) != 2:
    
                self.time = None
            
            else:
                    
                # ensure minute format is valid
                if len(time_list[1]) != 2:
                            
                    self.time = None
                    
                """
                convert elements in list to integers and continue testing
                assign None if elements not integers
                """
                try:
        
                    for index, element in enumerate(time_list):
        
                        time_list[index] = int(element)
        
                except ValueError:
        
                    self.time = None
        
                else:
        
                    # ensure hour is valid
                    if not 0 <= time_list[0] <= 23:
        
                        self.time = None
        
                    # ensure minutes are valid
                    if not 0 <= time_list[1] <= 59:
        
                        self.time = None
        else:
                
            self.time = time
            
        # duration
        
        self.duration = duration
        
        """
        ensure duration is positive integer
        assign None otherwise
        """
        try:
            
            if not duration > 0:
                
                self.duration = None

        except TypeError:
        
            self.duration = None
        
        # cal_type
        
        self.cal_type = cal_type
        
        # ensure cal_type is valid
        if not cal_type in CAL_TYPE:
            
            self.cal_type = None
            
        # valid
        
        # assign False if any attributes are None, otherwise assign True
        if self.date and self.time and self.duration and self.cal_type:
            
            self.valid = True
            
        else:
            
            self.valid = False

    def get_date(self):
        """
        return date (mm/dd/yyyy)
        """
        
        return self.date

    def get_time(self):
        """
        return time (hh:mm)
        """
        
        return self.time

    def get_time_range(self):
        """
        calculate end time, return start and end times in minutes in tuple (start, end)
        """
        
        # separate hour and minute values into list
        start_time_list = self.time.split(":")
        
        # convert list elements to integers
        for index, element in enumerate(start_time_list):
            
            start_time_list[index] = int(element)
            
        # create variables for hours and mins for calculations
        hours = start_time_list[0]
        mins = start_time_list[1]
        
        # create variable for event's duration
        duration = int(self.duration)
        
        # convert start time to minutes
        start_time_int = hours * 60 + mins
        
        # calculate end time in minutes
        end_time_int = start_time_int + duration

        return (start_time_int, end_time_int)

    def __str__(self):
        """
        return string representing event
        """
        
        result_str = "{}: ".format(self.date)

        result_str += "start: {}; ".format(self.time)

        result_str += "duration: {}".format(self.duration)
        
        return result_str


    def __repr__(self):
        if self.date and self.time and self.duration:
            return self.date + ';' + self.time + '+' + str(self.duration)
        else:
            return 'None'

    def __lt__(self, e):
        """
        return True if self's time is less then e's time, and False otherwise
    
        times converted into number of minutes for comparison (ex. 2:00 = 120)
        """
        
        # if either event's time is None, return False
        if self.time == None or e.time == None:
            
            return False
        
        # separate hours and minutes values into lists
        self_time_list = self.time.split(":")
        
        e_time_list = e.time.split(":")
        
        # convert list elements to integers
        for index, element in enumerate(self_time_list):
            
            self_time_list[index] = int(element)
            
        for index, element in enumerate(e_time_list):
            
            e_time_list[index] = int(element)
            
        # create variables for hours and mins for calculations
        self_hours = self_time_list[0]
        self_mins = self_time_list[1]
        
        e_hours = e_time_list[0]
        e_mins = e_time_list[1]
        
        # convert start times to minutes
        self_time_int = self_hours * 60 + self_mins
        
        e_time_int = e_hours * 60 + e_mins
        
        return self_time_int < e_time_int

    def __eq__(self, e):
        '''PROVIDED'''
        return self.date == e.date and self.time == e.time and self.duration == e.duration and self.cal_type == e.cal_type  # and self.status == e.status
