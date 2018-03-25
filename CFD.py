#CFD (Colon Formatted Document) Parser
#Turns a txt file in the CFD form into a dict() obj
#Also includes CQL (CFD Query Language)

import _io

class CFD_Doc():
    def __init__(self, p_source):
        """
        Takes: A source of text either a file or a str/bytes/etc object
        Does: Inits the class
        Returns: Nothing
        """

        if type(p_source) == _io.TextIOWrapper:
            self.contents = parse(p_source.read()\
                                  .split("\n"))
            p_source.close()
        elif type(p_source) in [str, bytes]:
            self.contents = parse(p_source.split("\n"))
        else:
            raise TypeError("p_source not of str/file/bytes type")

    def query(self, p_query):
        """
        Takes: A sql-style query called CQL
        Does: Creates a list with items matching the criteria
        Returns: The created list
        """

        self.results = list()
        self.word_type = ""
        self.start = 0
        self.limit = -1

        self.columns = list()
        self.conditions = list()

        self.updated = list()
        self.cols = list()
        self.value = None


        #Note: Delete all the variables using del at end of function

        #Split the query up (i.e parse it)
        x = Split(p_query)
        for word in x:
            if word is " ":
                continue
            
            elif word == "SELECT":
                self.word_type = "Select"
                

            elif word == "WHERE":
                self.word_type = "Condition"
   

            elif word == "START":
                self.word_type = "Start"

            elif word == "LIMIT":
                self.word_type = "Limit"

            elif self.word_type == "Select":
                self.columns.append(word)

            elif self.word_type == "Condition":
                self.conditions.append(word)

            elif self.word_type == "Start":
                try:
                    int(word)
                except ValueError:
                    raise ValueError(str("Invalid literal" + word + "for START"))
                else:
                    self.start = int(word)

            elif self.word_type == "Limit":
                try:
                    int(word)
                except ValueError:
                    raise ValueError(str("Invalid literal" + word + "for START"))
                else:
                    self.limit = int(word)

                
        #Now ensure all the columns exist
        if self.columns == ["*"]:
            self.columns = list()
            for key in self.contents.keys():
                self.columns.append(key)
                
        for column in self.columns:

            if column not in self.contents:
                raise KeyError("Column {0} doesn't exist in target CFD Object"\
                               .format(column))
        self.matched = 0
        if self.conditions == []:
            self.conditions = ["True"]
        #And finally, perform the query
        for i in range(self.start, len(self.contents[self.columns[0]])):
            for condition in self.conditions:
                for key in self.contents.keys():
                    ##

                    self.value = self.contents[key][i]
                    try:
                        int(self.value)
                    except ValueError:
                        try: float(self.value)
                        except: self.value = "'{0}'".format(self.value); 

                    ##
                    condition = condition.replace(key, self.value)

                if eval(condition):
                    self.cols = list()
                    for column in self.columns:
                        self.cols.append(self.contents[column][i])
                    self.results.append(self.cols)
                    self.matched += 1

                if self.matched == self.limit:
                    break
            if self.matched == self.limit:
                break

        del self.cols, self.columns, self.word_type, self.conditions
        del self.updated, self.start, self.limit, self.matched, self.value
        return self.results;
            
def parse(text):
    output = dict()
    next_line = "Entry"
    variables = list()



    for line in text:
        line = line.strip("\ufeff")
        if line == "\n" or line == " " or line == "":
            continue
        if line[0] == "#":
            continue

        if line == "!Format":
            next_line = "Format"
            continue

        if next_line == "Format":
            variables = line.split(":")
            for variable in variables:
                output[variable.rstrip().lstrip()] = list()
            next_line = "Entry"
            continue

        if next_line == "Entry":
            if len(line.split(":")) == len(variables):
                entries = line.split(":")
                i = 0
                for entry in entries:
                    output[variables[i].lstrip().rstrip()].append(entry.lstrip()\
                                                                  .rstrip())
                    i += 1
            else:
                break

    return output

def Split(p_word, p_keys=[" "], p_keep_key=True):
    """
    Takes: A word to split, a single key or a list of keys and a bool indicating whether to keep the key

    Does: Splits the word according to the key(s) like s.split() but in a smarter way

    Returns: The splitted string
    """

    EMPTY = ""
    words = list() #This list will contain all the splitted words.
    temp_word = EMPTY
    SPECIAL_LETTERS = "(){}[]\u0022'"
    ignore_key = False
    letter_counts, key_chart = {"normal" : 0, "square" : 0, "curly" : 0, "single-quote" : 0, "double-quote" : 0}, {"{" : "curly", "}" : "curly", "(" : "normal",
                                                                                                                   ")" : "normal", "[" :"square", "]" : "square",
                                                                                                                   "\u0022" : "double-quote", "'" : "single-quote"}
    
    for char in p_word:
        
        
        if char in SPECIAL_LETTERS:
            if letter_counts[key_chart[char]] >= 1: letter_counts[key_chart[char]] -= 1
            else: letter_counts[key_chart[char]] += 1

        if 1 in letter_counts.values(): ignore_key = True
        else: ignore_key = False

        #Special case alert (overides the previous condition)

        #if char is "\u0918": ignore_key = False

        if (char in p_keys) and (ignore_key is False):
            words.append(temp_word)
            temp_word = EMPTY
            if p_keep_key: words.append(char)
        else: temp_word += char

    words.append(temp_word)
    return words


