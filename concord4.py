#!/usr/bin/env python3

import sys
import re

class concord:

    def __init__(self, input=None, output=None):
        self.input = input
        self.output = output
        self.concord = self.__create_concord_array()


    def __create_concord_array(self):
        """
        The private function __create_concord_array returns an array
            containing formated strings with the uppercase indexed word
            from the given input file or stdin. The formatted line is
            left-aligned with the keyword starting at column 30 of the 
            string and words are between column 10 and 60
        Parameters: self
        Returns: Array containg formatted line of each keyword
        """
        result = []
        result_dict = {}
        exclude_arr = []
        index_arr = []
        if self.input == None:
             lines = sys.stdin
        else:
            file_text = open(self.input, 'r')
            lines = file_text.readlines()
            file_text.close()
        exclude_arr, index_arr = self.__get_input_stdin(lines)
        

        result_dict = self.__create_result_dict(index_arr, exclude_arr
        , result_dict)

        return_order = sorted(result_dict)

        result = self.__dict_order_arr(result_dict, return_order)

        if self.output != None:
            with open(self.output, 'w') as f:
                for line in result:
                    f.write(line)
                    f.write('\n')
        return result

    def __get_input_stdin(self, input):
        """
        The private function __get_input_stdin creates two arrays, exclude_arr
            and index_arr which contains all the exlude words and index lines
            from the input given
        Parameters: self
                    input - the lines from txt file given or from stdin as an
                        array
        Returns: two arrays, the exclude_arr and index_arr
        """
        exclude_arr = []
        index_arr = []
        exclude_count = 0
        in_index_arr = False
        for line in input:
            exclude_count = exclude_count + 1
            line_strip = line.strip()

            if line_strip == "\"\"\"\"":
                in_index_arr = True
            elif in_index_arr:
                index_arr.append(line_strip)
            elif exclude_count > 2: 
                exclude_arr.append(line_strip.lower())

        return exclude_arr, index_arr

    def __create_result_dict(self, index_arr, exclude_arr, result_dict):
        """
        The private function __create_result_dict checks to see if the word
            is the exclude_arr, if not in the array the key would be added
            to the dictionary if needed at append the formatted line of the
            key to the value. 
        Parameters: self
                    index_arr - an array containing all the indexing lines 
                        from the input
                    exclude_arr - an array containing all the exclude words
                        from the input
                    result_dict - dictionary which has the indexed words as
                        the key and formatted lines as the value
        Returns: result_dict
        """


        for line in index_arr:
            line_arr = re.split('\s+', line)
            if line != "":        
                for word in line_arr:
                    index = re.search(r"\b"+word, line)
                    lowered = word.lower()
                    if lowered not in exclude_arr:
                        if lowered not in result_dict:
                            result_dict[lowered] = []
                        result_dict[lowered].append(
                        self.__format_line(line_arr, lowered, index.start()))
        return result_dict
            
            

    def __format_line(self, line_arr, indexed_word, index):
        """
        The private function __format_line creates a string that is 
            left-aligned with the keyword starting at column 30 of the 
            string and words are between column 10 and 60
        Parameters: self
                    line_arr - array of words from the line
                    indexed_word - lowered cased index word
                    index - the index of the start of the indexed_word
        Returns: the formated line string
        """
        delete = 0
        result = ''
        marker = 1
        index += 10
        
        for word in line_arr:
            if word.lower() == indexed_word:
                multiplier = 30 - index
                temp = result
                result = ((multiplier+9)*' ') + temp
                upper_cased = re.sub(r"\b"+word, word.upper(), word) 
                result += upper_cased
                marker = 0
                index += (multiplier +(len(word)-1))
            elif marker == 0:
                index += (1 + len(word))
                if index > 60:
                    return result
                temp = result
                result = temp + ' ' + word
            elif index <= 30:
                temp = result
                result = temp + word + ' '
            else:
                index -= (len(word) + 1)
        return result

    def __dict_order_arr(self,dictionary, key_arr):
        """
        The private function __dict_order_arr combines all the value arrays
            from the dictionary into the result array
        Parameters: self
                    key_arr - array of strings of the indexed words sorted in
                    alphabetical order
        Returns: result array 
        """
        result = []
        for key in key_arr:
            result_arr = dictionary[key]
            result += result_arr
        return result

    def full_concordance(self):
        """
        The public function full_concordance returns self.concord 
        """
        return (self.concord)
