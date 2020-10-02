import sys
sys.path.append('c:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab2')
import lab2

lab2.input_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab3\\input.txt'

lab2.output_file_name = 'C:\\Users\\Влад\\Desktop\\7 semester\\Fundamentals-of-Software-Engineering-Economics-and-project-management-1\\lab3\\output.txt'

class NewApp(lab2.App):
    pass

if __name__ == "__main__":
    lab = NewApp()
    
    lab.get_rid_of_cycles()
    lab.detect_start()
    lab.define_start()
    lab.detect_finish()
    lab.define_finish()

    lab.partly_sort()
    NewApp.print_message_in_out_file('Исходный список работ сетевого графика\n', True)
    NewApp.print_message_in_out_file('%10s%10s%10s\n' % ('A', 'B', 't'))

    lab.print_jobs()