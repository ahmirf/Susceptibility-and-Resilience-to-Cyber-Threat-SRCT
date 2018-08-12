'''
Created on Nov 13, 2014

@author: Anjila
'''
from FileOperations import FileOperations
from globalTracker import REPORT

FIXATION_INTRIALCODE=1
UP_PROBE_INTRIALCODE = 5
dOWN_PROBE_INTRIALCODE = 6
PRACTISEIMAGE_INTRIALCODE=3

class IndexGenerator:
    def __init__(self):
        self.fileOperation = FileOperations()
    
    # 0        1        2            3            4            5            6            7            8            9            10
    # S.N.    date    subject    trialcode    currentblock    number    up_type    down_type    trialtimeout    correct    latency
    def calculateindex(self, filename):
        self.DAFI=0.0
        self.PAFI=0.0
        N_UP=0.0
        N_DOWN=0.0
        D_UP=0.0
        D_DOWN=0.0
        P_UP=0.0
        P_DOWN=0.0
        #*****************************************************************************************#
        #*******************for N_up and N _down************************#
        self.neutral_neutralCount = 0
        self.neutral_neutral_case = False
        self.upProbeInNeutral_neutral = 0
        self.downProbeInNeutral_neutral = 0
        self.responseTimeOnUpProbe_inNeutral_neutral = 0.0
        self.responseTimeOnDownProbe_inNeutral_neutral = 0.0
        #*****************************************************************************************#
        #************************for D_up *****************************************#
        self.negative_up_anyCount=0
        self.probeUp_inNegative_up=0 
        self.negative_up=False
        self.responseTimeOnProbe_Up_Negative_Up=0.0
        #*****************************************************************************************#
        #************************for D_down *****************************************#
        self.negative_down_anyCount=0
        self.probeDown_inNegative_down=0
        self.negative_down=False
        self.responseTimeOnProbe_Down_Negative_Down=0.0
        #*****************************************************************************************#
        #************************for P_up *****************************************#
        self.positive_Up_anyCount=0
        self.ProbeUp_inPositive_up=0
        self.positive_up=False
        self.responseTimeOnProbe_Up_Positie_Up=0.0
        
        #*****************************************************************************************#
        #************************for P_up *****************************************#
        self.positive_Down_anyCount=0
        self.probeDown_inPositie_down=0
        self.positive_down=False
        self.responseTimeOnProbe_Down_Positive_Down=0.0
        #*****************************************************************************************#
        lines = self.fileOperation.read(filename) 
        data = []
        lineNumberToNeglectForTraining=0
        lineNumber=0
        for eachLine in lines:
            lineNumber+=1
            if eachLine.strip() == "" or eachLine.strip()[0] == '#':
                continue
            else:
                data = eachLine.split("\t")
                if len(data) > 12:
                    print "length >11"
                else:
                    if data[3].strip().upper()==REPORT.TRIALCODE[FIXATION_INTRIALCODE]:
                        continue
                    if data[3].strip().upper()==REPORT.TRIALCODE[PRACTISEIMAGE_INTRIALCODE]:
                        #neglect the training data
                        lineNumberToNeglectForTraining=lineNumber+1
                        #if the trialcode=PRACTISE_PIC then we neglect upto the next line which contains the probe tracks
                        continue
                    if lineNumber<=lineNumberToNeglectForTraining:
                        continue;
                    
                    if self.positive_up:#P_UP
                        self.positive_Up_anyCount+=1
                        self.positive_up=False
                        
                        if int(data[9].strip())==1 and data[3].strip().upper() == REPORT.TRIALCODE[UP_PROBE_INTRIALCODE]:
                            self.ProbeUp_inPositive_up+=1
                            self.responseTimeOnProbe_Up_Positie_Up+=float(data[10].strip())*1000
                            
                    if self.positive_down:#P_DOWN
                        self.positive_Down_anyCount+=1
                        self.positive_down=False
                        if int(data[9].strip())==1 and data[3].strip().upper() == REPORT.TRIALCODE[dOWN_PROBE_INTRIALCODE]:
                            self.probeDown_inPositie_down+=1
                            self.responseTimeOnProbe_Down_Positive_Down+=float(data[10].strip())*1000
                        
                    if self.negative_up:#D_UP
                        self.negative_up_anyCount+=1
                        self.negative_up=False
                        if int(data[9].strip())==1 and data[3].strip().upper() == REPORT.TRIALCODE[UP_PROBE_INTRIALCODE]:
                            self.probeUp_inNegative_up+=1
                            self.responseTimeOnProbe_Up_Negative_Up+=float(data[10].strip())*1000
                    
                    if self.negative_down:#D_DOWN
                        self.negative_down_anyCount+=1
                        self.negative_down=False
                        if int(data[9].strip())==1 and data[3].strip().upper() == REPORT.TRIALCODE[dOWN_PROBE_INTRIALCODE]:
                            self.probeDown_inNegative_down+=1
                            self.responseTimeOnProbe_Down_Negative_Down+=float(data[10].strip())*1000
                        
                    if self.neutral_neutral_case:#N_UP and N_DOWN
                        self.neutral_neutral_case = False
                        if int(data[9].strip())==1 and data[3].strip().upper() == REPORT.TRIALCODE[UP_PROBE_INTRIALCODE]:
                            self.neutral_neutralCount += 1
                            self.upProbeInNeutral_neutral += 1
                            self.responseTimeOnUpProbe_inNeutral_neutral += float(data[10].strip()) * 1000
                        elif int(data[9].strip())==1 and data[3].strip().upper() == REPORT.TRIALCODE[dOWN_PROBE_INTRIALCODE]:
                            self.neutral_neutralCount += 1
                            self.downProbeInNeutral_neutral += 1
                            self.responseTimeOnDownProbe_inNeutral_neutral += float(data[10].strip()) * 1000
                        elif not (data[3].strip().upper() == REPORT.TRIALCODE[dOWN_PROBE_INTRIALCODE] or data[3].strip().upper() == REPORT.TRIALCODE[UP_PROBE_INTRIALCODE]):
                            print "this is due to incorrect data"
                            
                    if data[6].strip().upper() == "NEUTRAL" and data[7].strip().upper() == "NEUTRAL":#N_UP and N_DOWN             
                        self.neutral_neutral_case = True
                        
                    if data[6].strip().upper() == "NEGATIVE":#D_UP            
                        self.negative_up=True
                        
                    if data[7].strip().upper() == "NEGATIVE":#D_DOWN   
                        self.negative_down=True
                        
                    if data[6].strip().upper() == "POSITIVE":#P_UP
                        self.positive_up=True
                        
                    if data[7].strip().upper() == "POSITIVE":#P_DOWN     
                        self.positive_down=True
                    
        #*****************************************************************************************#                    
        if not self.neutral_neutralCount == (self.upProbeInNeutral_neutral + self.downProbeInNeutral_neutral):
            print "please verify the number of " + REPORT.TRIALCODE[UP_PROBE_INTRIALCODE] + " and " + REPORT.TRIALCODE[dOWN_PROBE_INTRIALCODE] + " .Their sum do not match the total number of total neutral neutral"
           
        print "all the calculations are done by neglecting the incorrect responses i.e. if correct=0 then that data is neglected" 
        print "#*****************************************************************************************#"
        print "total no. of CASE: UP_NEUTRAL_DOWN_NEUTRAL = " + str(self.neutral_neutralCount)
        print "\n#**********************N_UP***************************#\n"
        print "total no. of CASE: UP_PROBE in UP_NEUTRAL_DOWN_NEUTRAL = " + str(self.upProbeInNeutral_neutral)
        print "sum of response time  for CASE: UP_PROBE in UP_NEUTRAL_DOWN_NEUTRAL = " + str(self.responseTimeOnUpProbe_inNeutral_neutral)
        if not self.upProbeInNeutral_neutral==0:
            N_UP=self.responseTimeOnUpProbe_inNeutral_neutral / self.upProbeInNeutral_neutral
        print "average response time for CASE: UP_PROBE in UP_NEUTRAL_DOWN_NEUTRAL = (N_UP) " + str(N_UP)
        print "\n#**********************N_DOWN***************************#\n"
        print "total no. of CASE:DOWN_PROBE in UP_NEUTRAL_DOWN_NEUTRAL = " + str(self.downProbeInNeutral_neutral)
        print "sum of response time  for CASE: DOWN_PROBE in UP_NEUTRAL_DOWN_NEUTRAL = " + str(self.responseTimeOnDownProbe_inNeutral_neutral)
        if not self.downProbeInNeutral_neutral==0:
            N_DOWN=self.responseTimeOnDownProbe_inNeutral_neutral / self.downProbeInNeutral_neutral
        print "average response time for CASE: DOWN_PROBE in UP_NEUTRAL_DOWN_NEUTRAL (N_DOWN) = " + str(N_DOWN)
        print "*************************************************************************************************\n"
        print "\n#**********************D_UP***************************#\n"
#         print "total no. of CASE: UP_NEGATIVE_DOWN_ANY = "+str(self.negative_up_anyCount)
        print "total no. of CASE: UP_PROBE in UP_NEGATIVE_DOWN_ANY = "+str(self.probeUp_inNegative_up)
        print "sum of response time  for CASE: UP_PROBE in UP_NEGATIVE_DOWN_ANY  = " +str(self.responseTimeOnProbe_Up_Negative_Up)
        if not self.probeUp_inNegative_up==0:
            D_UP=self.responseTimeOnProbe_Up_Negative_Up/self.probeUp_inNegative_up
        print "average response time for CASE: UP_PROBE in UP_NEGATIVE_DOWN_ANY (D_UP)  = " +str(D_UP)
        print "\n#**********************D_DOWN***************************#\n"
#         print "total no. of CASE: UP_ANY_DOWN_NEGATIVE = "+str(self.negative_down_anyCount)
        print "total no. of CASE: DOWN_PROBE in UP_ANY_DOWN_NEGATIVE = "+str(self.probeDown_inNegative_down)
        print "sum of response time  for CASE: DOWN_PROBE in UP_ANY_DOWN_NEGATIVE  = " +str(self.responseTimeOnProbe_Down_Negative_Down)
        if not self.probeDown_inNegative_down==0:
            D_DOWN=self.responseTimeOnProbe_Down_Negative_Down/self.probeDown_inNegative_down
        print "average response time for CASE: DOWN_PROBE in UP_ANY_DOWN_NEGATIVE (D_DOWN) = " +str(D_DOWN)
        print "\n#**********************Distress Attentional Facilitation Index (Y)***************************#\n"
        self.DAFI=0.5*((N_UP-D_UP)+(N_DOWN-D_DOWN))
        print "Distress Attentional Facilitation Index (Y) = "+str(self.DAFI)
        print "*************************************************************************************************\n"
        print "\n#**********************P_UP***************************#\n"
#         print "total no. of CASE: UP_POSITIVE_DOWN_ANY = "+str(self.positive_Up_anyCount)
        print "total no. of CASE: UP_PROBE in UP_POSITIVE_DOWN_ANY = "+str(self.ProbeUp_inPositive_up)
        print "sum of response time  for CASE: UP_PROBE in UP_POSITIVE_DOWN_ANY  = " +str(self.responseTimeOnProbe_Up_Positie_Up)
        if not self.ProbeUp_inPositive_up==0:
            P_UP=self.responseTimeOnProbe_Up_Positie_Up/self.ProbeUp_inPositive_up
        print "average response time for CASE: UP_PROBE in UP_NEGATIVE_DOWN_ANY (P_UP) = " +str(P_UP)
        print "\n#**********************P_DOWN***************************#\n"
        
#         print "total no. of CASE: UP_ANY_DOWN_POSITIVE = "+str(self.positive_Down_anyCount)
        print "total no. of CASE: DOWN_PROBE in UP_ANY_DOWN_POSITIVE = "+str(self.probeDown_inPositie_down)
        print "sum of response time  for CASE: DOWN_PROBE in UP_ANY_DOWN_POSITIVE  = " +str(self.responseTimeOnProbe_Down_Positive_Down)
        if not self.probeDown_inPositie_down==0:
            P_DOWN=self.responseTimeOnProbe_Down_Positive_Down/self.probeDown_inPositie_down
        print "average response time for CASE: DOWN_PROBE in UP_ANY_DOWN_POSITIVE (P_DOWN) = " +str(P_DOWN)
        print "\n#**********************Positive Attentional Facilitation Index (P)***************************#\n"
        self.PAFI=0.5*((N_UP-P_UP)+(N_DOWN-P_DOWN))
        print "Positive Attentional Facilitation Index (P) = "+str(self.PAFI)
        #*****************************************************************************************#
                    
def main():
    print "In attentionIndexgenerator.py"
    fileName = "..\\reports\\ImageDotProbeResult.dat"
    indexCalculator = IndexGenerator()
    indexCalculator.calculateindex(fileName)
    
if __name__ == "__main__":
    main()
                    
                
                
                
        
