import os

class filemanage:
    def delete_line(self,original_file, line_number):
        """ Delete a line from a file at the given line number """
        is_skipped = False
        current_index = 0
        dummy_file = original_file + '.bak'
        # Open original file in read only mode and dummy file in write mode
        with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
            # Line by line copy data from original file to dummy file
            for line in read_obj:
                # If current line number matches the given line number then skip copying
                if current_index != line_number:
                    write_obj.write(line)
                else:
                    is_skipped = True
                current_index += 1
        # If any line is skipped then rename dummy file as original file
        if is_skipped:
            os.remove(original_file)
            os.rename(dummy_file, original_file)
        else:
            os.remove(dummy_file)
    def delete_multiple_lines(self,original_file, line_numbers):
        """In a file, delete the lines at line number in given list"""
        is_skipped = False
        counter = 0
        # Create name of dummy / temporary file
        dummy_file = original_file + '.bak'
        # Open original file in read only mode and dummy file in write mode
        with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
            # Line by line copy data from original file to dummy file
            for line in read_obj:
                # If current line number exist in list then skip copying that line
                if counter not in line_numbers:
                    write_obj.write(line)
                else:
                    is_skipped = True
                counter += 1
        # If any line is skipped then rename dummy file as original file
        if is_skipped:
            os.remove(original_file)
            os.rename(dummy_file, original_file)
        else:
            os.remove(dummy_file)
    def delete_line_by_full_match(self,original_file, line_to_delete):
        """ In a file, delete the lines at line number in given list"""
        is_skipped = False
        dummy_file = original_file + '.bak'
        # Open original file in read only mode and dummy file in write mode
        with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
            # Line by line copy data from original file to dummy file
            for line in read_obj:
                line_to_match = line
                if line[-1] == '\n':
                    line_to_match = line[:-1]
                # if current line matches with the given line then skip that line
                if line_to_match != line_to_delete:
                    write_obj.write(line)
                else:
                    is_skipped = True
        # If any line is skipped then rename dummy file as original file
        if is_skipped:
            os.remove(original_file)
            os.rename(dummy_file, original_file)
        else:
            os.remove(dummy_file)
    def delete_line_by_condition(self,original_file, condition):
        """ In a file, delete the lines at line number in given list"""
        dummy_file = original_file + '.bak'
        is_skipped = False
        # Open original file in read only mode and dummy file in write mode
        with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
            # Line by line copy data from original file to dummy file
            for line in read_obj:
                # if current line matches the given condition then skip that line
                if condition(line) == False:
                    write_obj.write(line)
                else:
                    is_skipped = True
        # If any line is skipped then rename dummy file as original file
        if is_skipped:
            write_obj.close()
            original_file.close()
            os.remove(original_file)
            os.rename(dummy_file, original_file)
        else:
            os.remove(dummy_file)
    def delete_line_with_word(self,file_name, word):
        """Delete lines from a file that contains a given word / sub-string """
        delete_line_by_condition(file_name, lambda x : word in x )
    def delete_shorter_lines(self,file_name, min_length):
        """Delete lines from a file that which are shorter than min_length """
        delete_line_by_condition(file_name, lambda x: len(x) < min_length)