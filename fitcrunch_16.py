# -*- coding: utf-8 -*-
'''This program will create instances of the class "sas_result", by recognizing certain structures in the data'''

import subprocess
import os
import easygui
class sas_result(object):
    sas_dic={} #See below, please
    '''This will define the class at every runtime'''
    def __init__(self, sas_folder):
        '''This will define each instance of the class, as being a sas_file'''
        self.foldername=sas_folder
        '''Now the program puts all the instances in a dictionary (where the keys define each instance, and the values
        define the specs), and this is why we added the line sas_dic={} above...'''
        sas_result.sas_dic[self.foldername]=self
        '''Question remains if it at all is necessary to define objects in such a program,
        actually it would be easier to just run it as a script on a folder of choice. We're actually doing procedural programming
        by using OOP, which is difficult to grasp!'''
        self.program='ATSAS'
        self.iterations=0
        self.logfilelist=[]
        self.notes='Bring the noise!!'
        self.programs=['dammin','dammif','bunch','gasbor']
        self.chi_collect={}
        self.pymol_cmd='pymol'
        #self.dmax=75.0
        #self.dmaxunit=''
        #self.rg=30.0
        #self.rgunit=''
        self.folderreader()
    def folderreader(self):
        self.programlist=[]
        for my_file in os.listdir(self.foldername):
            #print path,dirs,files
            #for my_file in files:
                if my_file[-4:]=='.log': #and path==self.foldername:
                    self.iterations+=1
                    self.logfilelist.append(my_file)
        for logfile in self.logfilelist:
            print 'Processing',logfile
            f=file(os.path.join(self.foldername,logfile), 'r')
            lines=f.readlines()
            f.close()
            sim_rounds=0
            my_chis={}
            found_prog= False
            skip_chi= True
            for line in lines:
                if not found_prog:
                    for prog in self.programs:
                        if prog in line.lower():
                            found_prog= True
                            if prog in self.programlist:
                                break
                            else:
                                self.programlist.append(prog)
                                break
                #Now the method will start generating a dictionary of the lineNr. and Chi-values
                if 'Simulated annealing procedure started' in line:
                    skip_chi= False
                if 'chi' in line and not skip_chi:
                    sim_rounds+=1
                    #Checking for numbers...
                    result=[]
                    for word_pos in [-5,-4,-3,-2,-1]:
                        word=line.split()[word_pos]
                        try:
                            chi=float(word)
                        except ValueError:
                            chi=-999
                        result.append(chi)
                    my_chis[sim_rounds]=result
                    print sim_rounds, my_chis[sim_rounds]
            #Done with the current logfile
            a=my_chis[1]
            b=my_chis[sim_rounds]
            #Looking which number is changing...
            right_chi=0
            if a[-5]!=b[-5]:
                right_chi=-5
            elif a[-4]!=b[-4]:
                right_chi=-4
            elif a[-3]!=b[-3]:
                right_chi=-3
            elif a[-3]!=b[-3]:
                right_chi=-3             
            elif a[-2]!=b[-2]:
                right_chi=-2
            elif a[-1]!=b[-1]:
                right_chi=-1
            else:
                print 'Screwup!'
            print 'Found something, its:',right_chi
            chimax=my_chis[1][right_chi]
            chimin=my_chis[sim_rounds][right_chi]
            #print chimax,'-',chimin
            self.chi_collect[logfile]=(sim_rounds,chimax,chimin)
        print self.iterations,'X',self.programlist
        #print self.chi_collect
        self.right_chis={}
        for logfile in self.chi_collect.keys():
            self.right_chis[self.chi_collect[logfile][-1]]=logfile
        print self.right_chis
        print '*******'
        self.top_chis=self.right_chis.keys()
        self.top_chis.sort()
        print self.top_chis[:10]
        self.top_ten=[]
        for top_chis in self.top_chis:
            theten_pdbs=self.right_chis[top_chis]
            theten_pdbs=theten_pdbs[:-3]+'pdb'
            self.top_ten.append(theten_pdbs)
            if len(self.top_ten)>10:
                break
        print self.top_ten        
        subprocess.call(['/Applications/Structural/MACPymol.app','13.pdb'])#self.top_ten[0]])#,self.top_ten[1],self.top_ten[2],self.top_ten[3],self.top_ten[4],
                         #self.top_ten[5],self.top_ten[6],self.top_ten[7],self.top_ten[8],self.top_ten[9]])

start_path=easygui.diropenbox('Please select folder to scan',
                              'Scan folders for files',
                              '/Users/mads/Science/data/sas/saxs/Hamburg/071221/process/Bunch/WtnR65/100330/')
my_sas=sas_result(start_path)
