'''
Created on Aug 4, 2014

@author: Anjila
'''

class FileOperations:
    def __init__(self):
        print "In Fileoperations.py"
#         FileOperations.py initiated
        pass
        
    def write(self, fileLocation, text):
        try:
            with open(fileLocation, "a") as myfile:
                myfile.write(text)
        except Exception, e:
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% error %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print "ERROR: "+e
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% error %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            
    def read(self,fileLocation):
        try:
            datafile = open(fileLocation, 'r')
            lines= datafile.readlines()
            datafile.close()
            return lines
        except Exception, e:
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% error %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
            print "ERROR: "+e
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% error %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"