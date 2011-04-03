"""This is not a command extension by itself. Its just a common module being
used by all other command extensions"""
import csv

class Spec(object):
    def __init__(self, csv_file_path, headers):
        self.csv_file_path = csv_file_path
        self.headers = headers
        self.valid = False
        
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.csv_file_path)
    
    def validate(self):
        self.columns = [getattr(self, column) for column in dir(self) if isinstance(getattr(self, column),
                                                                                    SpecColumn)]
        reader = csv.DictReader(open(self.csv_file_path, 'r'), self.headers)
        reader.next()
        self.data = []
        while True:
            try:
                items = reader.next()
            except StopIteration:
                break
            row_info = {}
            for column in self.columns:
                try:
                    column.validate(items[column.header_name])
                except SpecMisMatchException, e:
                    print 'SpecMisMatchException:%s' % e.__str__()
                    break
                row_info[column.header_name] = column.data
            self.data.append(row_info)
        self.valid = True
        return True
    
    def clean(self):
        data = {}
        if self.valid:
            for row_data in self.data:
                yield row_data
        else:
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
        
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.header_name)
        
    def validate(self, data):
        if self.required and not data:
            raise SpecMisMatchException, "This column is a required data and the Supplied data is empty.\nData:%s" % data
        if isinstance(data, str) and (len(data) > self.length):
            raise SpecMisMatchException, "Supplied data is having more length when compared to the Allotted Length.\nData:%s" % data
        try:
            self.data = self.data_type(data) 
        except Exception, e:
            raise SpecMisMatchException, "Supplied data is different datatype when compared to the specified Data Type.\nData:%s" % data