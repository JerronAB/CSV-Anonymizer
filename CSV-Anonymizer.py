#tooling:
# CSV-Anonymizer [OPTIONS] [DIRECTORY, FILE, OR FILES (comma-separated)]
    # -a: perform function on all CSV's in given/current directory
    # -d: de-anonymize instead of anonymize; pkl files must be in same directory as CSV's
    # -n: newname (for single files); default is to append "-anon" to the end of the filename.
    # -o: output directory
    # --no-pkl: do not generate files for reversing the anonymizing process. 
    # -i: guided interactive mode; do not exit. 

class PeopleTable: #this is a singleton, so that every instance of CSV "knows" the rosters of all other instances
    _instance = None
    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super().__new__(self)
        return self._instance
    def __init__(self) -> None:
        self.people = set()
        self.EmplIDSet = set()
        self.NameSet = set()
        self.EmailSet = set()
        self.AddressSet = set()
        self.fake_EmplIDSet = set()
        self.fake_NameSet = set()
        self.fake_EmailSet = set()
        self.fake_AddressSet = set()
    def newPerson(object):
        pass

import pickle
class CSV: #kind of circuitous, because it saves all data to object and THEN parses rows.
           #Keeping it for now in case it helps with extra functionality later
    def __init__(self, filename: str,modify=True) -> None:
        self.fileIntake(filename)
        self.modify = modify
        self.emplID_index = int()
        self.email_index = int()
        self.name_index = int()
        self.address_index = int()
    def fileIntake(self, filename: str):
        from csv import reader
        self.filename = filename.split('\\')
        self.filename = self.filename[-1]
        with open(filename, 'r', encoding='ISO-8859-1') as csvfile: #this encoding makes Excel-exported CSV files readable
            self.name = self.filename.replace('.csv','')
            csvData = [row for row in reader(csvfile)]
            self.Columns = list(map(lambda input_str: input_str.replace("ï»¿",""), csvData.pop(0)))
            self.Data = [self.rowParse(row) for row in csvData]
    def export(self,filename: str): 
        from csv import writer
        nonetoString = lambda cells: [str(cell or '') for cell in cells]
        print(f'Writing to... {filename}')
        with open(filename,'w',newline='') as csv_file:
            my_writer = writer(csv_file, delimiter = ',')
            my_writer.writerow(nonetoString(self.Columns))
            for row in self.Data:
                my_writer.writerow(nonetoString(row))
    def rowParse(self,row_list):
        pt = PeopleTable()
        newPerson = Person()
        return newPerson.matchTypes(row_list)
    #for each row, run row through data detection; if data detection valid for item, set index

first_names = ("John", "Jane", "Michael", "Sarah", "Robert", "Emily", "David", "Emma", "William", "Olivia", "James", "Ava", "Joseph", "Sophia", "Daniel", "Isabella", "Matthew", "Mia")
middle_names = ("Lee", "Marie", "Ann", "Joseph", "Elizabeth", "Grace", "Michael", "John", "Lynn", "Rose", "Andrew", "Alex", "Nicole")
last_names = ("Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Martinez", "Wilson", "Anderson", "Taylor", "Thomas")
name_suffixes = ("Jr.", "Sr.", "II", "III", "IV")
name_prefixes = ("Dr.", "Mr.", "Mrs.", "Ms.")
isEmplID = lambda x: len(x) == 9
isName = lambda x: ',  ' in x
isEmail = lambda x: '@' in x
isAddress = lambda x: False #not sure about how to test this one yet

import random
class Person: #ISSUE: How will we get multiple instances of a type included? Advisor names for example. 
              #ANSWER: initiate new instance whenever we find it. 
              #ISSUE: How will we know which instance belongs with which when a type repeats?
    class _emplID: #these may not be necessary at all; thought they may allow for more complex regex-checking and such later
        pass
    class _name:
        pass
    class _address:
        pass
    class _email:
        pass
    def __init__(self) -> None:
        self.emplID = int()
        self.name = str()
        self.address = str()
        self.email = str()
        self.fake_emplID = int()
        self.fake_name = str()
        self.fake_address = str()
        self.fake_email = str()
    def __hash__(self) -> int:
        return hash(f'{self.emplID}{self.name}')
    def __eq__(self, __value: object) -> bool:
        pass
    def matchTypes(self, list_of_values: list): #here's how this SHOULD work: match and note indexes. Generate all fakes. Then return at the end. 
        newList = list_of_values
        print('Matching types...\n')
        def matchMove(category, index, cell): 
            print(f'Category: {category}, Cell: {cell}, Index: {index}')
            self.__dict__[category]=[cell]
            if category == "name": self.genName()
            newList[index] = self.fake_name
        for num, cell in enumerate(list_of_values):
            if isEmplID(cell): matchMove("emplID",num,cell) #test here: if we already found a name, generate new Person class in PeopleTable using recursion
            if isName(cell): matchMove("name",num,cell)
            if isEmail(cell): matchMove("email",num,cell)
            if isAddress(cell): matchMove("address",num,cell)
            return newList
    def genName(self):
        for tup,probability in ((name_prefixes,25),(first_names,100),(middle_names,50),(last_names,100),(name_suffixes,25)):
            if random.randrange(0,100) <= probability: self.fake_name += f'{random.choice(tup)} '
        #rand_select = lambda x: self.fake_name += f'{random.choice(x)} ' <- an attempt at being more in-line
        #(rand_select(tup) for tup,prob in ((name_prefixes,25),(first_names,100),(middle_names,50),(last_names,100),(name_suffixes,25)) if random.randrange(0,100) <= prob)
    def genEmail(self):
        try:
            self.fake_email = f'{self.fake_name}@email.com'
        except:
            self.genName()
            self.genEmail()
    def genEmplID(self):
        pass
    def genAddress(self):
        pass
    def matchReverse(self):
        pass

#next step: figure out what we want the data structures here to look like. How will this all be stored? 

def anonymize(csv_filename: str, newname_fx: callable): #what's the purpose of this fx when class is doing almost all of the work?
    csvData = CSV(csv_filename)
    csvData.export(newname_fx(csv_filename))

def anonymizeFiles(filename_list):
    pass


from argparse import ArgumentParser
# Create the argparse parser
parser = ArgumentParser(description='CSV-Anonymizer')

# Add the command-line options
parser.add_argument('files', nargs='+', help='CSV files to process')
parser.add_argument('-a', action='store_true', help='Perform function on all CSV files in the directory')
parser.add_argument('-d', action='store_true', help='De-anonymize instead of anonymize')
parser.add_argument('-n', dest='newname', metavar='NEWNAME', help='New name for single file')
parser.add_argument('-o', dest='output_dir', metavar='OUTPUT_DIR', help='Output directory')
parser.add_argument('--no-pkl', action='store_true', help='Do not generate files for reversing the anonymizing process')
parser.add_argument('-i', action='store_true', help='Guided interactive mode; do not exit')

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the command-line options
files = args.files
perform_all = args.a
de_anonymize = args.d
newname = args.newname
output_dir = args.output_dir
generate_pkl = not args.no_pkl
interactive_mode = args.i

# Example usage
print('Files:', files)
print('Perform All:', perform_all)
print('De-anonymize:', de_anonymize)
print('New Name:', newname)
print('Output Directory:', output_dir)
print('Generate PKL:', generate_pkl)
print('Interactive Mode:', interactive_mode)


for file in files:
    csv_file = CSV(file)
    csv_file.rowParse
    csv_file.export(f'{output_dir}{csv_file.filename.replace(".csv","")}_temp.csv')