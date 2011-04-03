"""This is not a command extension by itself. Its just a common module being
used by all other command extensions"""
import csv

class Spec(object):
    def __init__(self, csv_file_path, *headers):
        self.csv_file_path = csv_file_path
        self.headers = headers
        self.valid = False
    
    def validate(self):
        self.columns = [column for column in dir(self) if isinstance(column,
                                                                     SpecColumn)] 
        reader = csv.DictReader(open(self.csv_file_path, 'r'),
                                    fieldnames=self.headers)
        reader.next()
        self.cleaned_data = {}
        while True:
            try:
                items = reader.next()
            except StopIteration:
                return True
            for column in self.columns:
                column.validate(items[column.name])
                self.cleaned_data[column.name] = column.data
        self.valid = True
        return True
    
    def cleaned_data(self):
        data = {}
        if self.valid:
            for column in self.columns:
                data[column.name] = column.data
            return data
        raise Exception, "Spec is not validated. It should be validated First"

class SpecMisMatchException(Exception):
    pass            

class SpecColumn(object):
    def __init__(self, header_name, length, data_type, required=False, separator=None):
        self.header_name = header_name
        self.length = length
        self.data_type = data_type
        self.required = required
        self.separator = separator
        
    def validate(self, data):
        if required and not data:
            raise SpecMisMatchException, "This column is a required data\
            and the Supplied data is empty"
        if len(data) > self.length:
            raise SpecMisMatchException, "Supplied data is having more length \
            when compared to the Allotted Length"
        try:
            self.data = self.data_type(data) 
        except Exception, e:
            raise SpecMisMatchException, "Supplied data is different datatype\
            when compared to the specified Data Type"