# -*- coding: utf-8 -*-

##########################################################
#
#        Cloud Radar System (CRS) Reflectivity and 
#        Doppler Velocity Quick View Functions
#	
#        Decription: This script contains the functions
#        used in the main CRS_Recipe_Code.py script to
#        plot CRS reflectivity and Doppler velocity data
# 
#        Authors: Essence Raphael and Yuling Wu 
#        Information and Technology Systems Center (ITSC)
#        University of Alabama in Huntsville
#        
#        Last Edit Date: 30 August 2021
#
##########################################################

#Import Python packages and modules
import re
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta 
from matplotlib.colors import ListedColormap
from matplotlib import cm 
from pathlib import Path

def select_campaign():
    """
    User selects which CRS campaign dataset they would
    like the code to read
    Return name of campaign (CRS dataset)
    """
    campaigns={1:'impacts',2:'goesrplt',3:'olympex',4:'iphex'}
    print("Select the CRS campaign dataset you would like to plot from the list below.")

    for i in campaigns:
        print("Campaign #{}: {}".format(i,campaigns[i]))

    while True:
        num = input ("\n*Enter Campaign Number or 'Q' to quit: ") 
        if num.isdigit():
            if int(num) in campaigns:
                dataset=campaigns[int(num)]
                print('The {} campaign is selected'.format(dataset))
                break
            else: 
                print(num,"is not a valid campaign number. Select a flight from the list:\n")
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            print('\n%%Invalid flight No. format%% \nTry again.\n')
    return dataset

def select_flight_impacts(dataDir):
    """
    User selects among the available flights from the files on their computer
    Return date in 'yyyymmdd' of the selected flight
    """
        
    impacts_files = [path for path in Path(dataDir).rglob('IMPACTS_CRS_L1B_*.h5')]
    impacts_files = [os.path.normpath(i) for i in impacts_files]
    
    #Check whether impacts files were found in the directory. Return 'None' if no
    #files were found. Continue through the code if files were found.
    if len(impacts_files)==0:
        print("%%There are no impacts data files in the currect directory. Try again%%")
        return None
    else: 
        pass
    
    flight_dates = [] 
    
    for i in impacts_files:
        fname_split = re.split(r'_', os.path.basename(i))
        start_date = fname_split[4]
        
        flight_dates.append(datetime.strptime(start_date[:8], '%Y%m%d').date().isoformat())
   
    print('Flight Dates:')
    for i in flight_dates:
        print('{}'.format(i))

    while True:
        num = input ("\n*Enter date in [yyyy-mm-dd] or Q to quit:") 
        if num.isdigit():
            if num in flight_dates:
                fdate = num
                print('Flight date {} is selected.'.format(num))
                break
            else: 
                print(num,"is not a valid flight date. Select a flight from the list.")
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            try:
                Fdate=datetime.strptime(num, '%Y-%m-%d').strftime("%Y-%m-%d")
                if Fdate in flight_dates:
                    fdate=Fdate
                    print('Flight date {} is selected.'.format(fdate))
                    break
                else: 
                    print(Fdate,"is not a valid flight date. Select a flight from the list:")
                    
            except ValueError:
                print('\n%%Invalid flight date format%% \nTry again.\n')
                
    selected_files = [path for path in Path(dataDir).rglob('IMPACTS_CRS_L1B_*'+fdate.replace('-','')+'*.h5')]
    selected_files = [os.path.normpath(i) for i in selected_files]
    return selected_files

def select_time_impacts(selected_files):
    """
    User selects among the available flight time periods 
    Return the selected file name
    """
    
    start_times = []
    end_times = []
    
    time_periods = {}
    
    for i in selected_files:
        fname_split = re.split(r'_', os.path.basename(i))
        
        start_time = fname_split[4]
        start_time = start_time[9:11] + ':' + start_time[11:13] + ':' + start_time[13:]
        start_times.append(start_time)
                
        end_time = fname_split[6]
        end_time = end_time[9:11] + ':' + end_time[11:13] + ':' + end_time[13:15]
        end_times.append(end_time)
        
        time_periods[selected_files.index(i)+1] = start_time + ' to ' + end_time
        
    for i in time_periods:
        print('The IMPACTS flight periods available for this date are: \n #{} - {}'.format(i, time_periods[i]))
        
    while True:
        num = input ("\n*Enter valid flight period no. or Q to quit: ") 
        if num.isdigit():
            if int(num) in time_periods:
                print('Flight period #{}: {} is selected.'.format(int(num),time_periods[int(num)]))
                break
            else: 
                print(int(num),"is not a valid flight period. Select a period no. from the list:")            
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            print('\n%%Invalid flight No. format%% \nTry again.\n')
    return os.path.basename(selected_files[int(num)-1]) #Returns selected file name

def select_flight_goesrplt(dataDir):
    """
    User selects among the available flights from the files on their computer 
    Return date in 'yyyymmdd' of the selected flight
    """
    goesrplt_files = [path for path in Path(dataDir).rglob('GOESR_CRS_L1B_*.nc')]
    goesrplt_files = [os.path.normpath(i) for i in goesrplt_files]         
    
    #Check whether goesrplt files were found in the directory. Return 'None' if no
    #files were found. Continue through the code if files were found.
    if len(goesrplt_files)==0:
        print("%%There are no goesrplt data files in the currect directory. Try again%%")
        return None, None
    else: 
        pass
    
    flight_dates = [] 
    
    for i in goesrplt_files:
        fname_split = re.split(r'_', os.path.basename(i))
        start_date = fname_split[3]
        
        flight_dates.append(datetime.strptime(start_date, '%Y%m%d').date().isoformat())
   
    print('Flight Dates:')
    for i in flight_dates:
        print('{}'.format(i))

    while True:
        num = input ("\n*Enter date in [yyyy-mm-dd] or Q to quit:") 
        if num.isdigit():
            if num in flight_dates:
                fdate = num
                print('Flight date {} is selected.'.format(num))
                break
            else: 
                print(num,"is not a valid flight date. Select a flight from the list.")
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            try:
                Fdate=datetime.strptime(num, '%Y-%m-%d').strftime("%Y-%m-%d")
                if Fdate in flight_dates:
                    fdate=Fdate
                    print('Flight date {} is selected.'.format(fdate))
                    break
                else: 
                    print(Fdate,"is not a valid flight date. Select a flight from the list:")
                    
            except ValueError:
                print('\n%%Invalid flight date format%% \nTry again.\n')
                
    selected_files = [path for path in Path(dataDir).rglob('GOESR_CRS_L1B_*'+fdate.replace('-','')+'*.nc')]
    selected_files = [os.path.normpath(i) for i in selected_files]
    return os.path.basename(selected_files[0]), fdate.replace('-','') 


def select_flight_olympex(dataDir):
    """
    User selects among the available flights from the files on their computer
    Returns the date in 'yyyymmdd' of the selected flight
    """
        
    olympex_files = [path for path in Path(dataDir).rglob('olympex_CRS_*.nc')] 
    olympex_files = [os.path.normpath(i) for i in olympex_files]
    
    #Check whether olympex files were found in the directory. Return 'None' if no
    #files were found. Continue through the code if files were found.
    if len(olympex_files)==0:
        print("%%There are no olympex data files in the currect directory. Try again%%")
        return None, None
    else: 
        pass
    
    flight_dates = [] 
    
    for i in olympex_files:
        fname_split = re.split(r'_|-', os.path.basename(i))
        start_date = fname_split[2]
        
        flight_dates.append(datetime.strptime(start_date, '%Y%m%d').date().isoformat())
   
    print('Flight Dates:')
    for i in flight_dates:
        print('{}'.format(i))

    while True:
        num = input ("\n*Enter date in [yyyy-mm-dd] or Q to quit:") 
        if num.isdigit():
            if num in flight_dates:
                fdate = num
                print('Flight date {} is selected.'.format(num))
                break
            else: 
                print(num,"is not a valid flight date. Select a flight from the list.")
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            try:
                Fdate=datetime.strptime(num, '%Y-%m-%d').strftime("%Y-%m-%d")
                if Fdate in flight_dates:
                    fdate=Fdate
                    print('Flight date {} is selected.'.format(fdate))
                    break
                else: 
                    print(Fdate,"is not a valid flight date. Select a flight from the list:")
                    
            except ValueError:
                print('\n%%Invalid flight date format%% \nTry again.\n')
                
    selected_files = [path for path in Path(dataDir).rglob('olympex_CRS_'+fdate.replace('-','')+'*.nc')]
    selected_files = [os.path.normpath(i) for i in selected_files]
    return selected_files,fdate.replace('-','')


def select_time_olympex(selected_files):
    """
    User selects among the available flight time periods 
    Return the selected file name
    """
    start_times = []
    end_times = []
    
    time_periods = {}
    
    for i in selected_files:
        fname_split = re.split(r'_|-', os.path.basename(i))
        
        start_time = fname_split[3]
        start_time = start_time[:2] + ':' + start_time[2:4] + ':' + start_time[4:]
        start_times.append(start_time)
                
        end_time = fname_split[5]
        end_time = end_time[:2] + ':' + end_time[2:4] + ':' + end_time[4:]
        end_times.append(end_time)
        
        time_periods[selected_files.index(i)+1] = start_time + ' to ' + end_time
        
    for i in time_periods:
        print('The OLYMPEX flight periods available for this date are: \n #{} - {}'.format(i, time_periods[i]))
        
    while True:
        num = input ("\n*Enter valid flight period no. or Q to quit: ") 
        if num.isdigit():
            if int(num) in time_periods:
                print('Flight period #{}: {} is selected.'.format(int(num),time_periods[int(num)]))
                break
            else: 
                print(int(num),"is not a valid flight period. Select a period no. from the list:")            
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            print('\n%%Invalid flight No. format%% \nTry again.\n')
    return os.path.basename(selected_files[int(num)-1])

def select_flight_iphex(dataDir):
    """
    User select among the available flights by list number 
    Return date in 'yyyymmdd' of the selected flight
    """
        
    iphex_files = [path for path in Path(dataDir).rglob('IPHEX_CRS_L1B_*.nc')]
    iphex_files = [os.path.normpath(i) for i in iphex_files]
    
    #Check whether iphex files were found in the directory. Return 'None' if no
    #files were found. Continue through the code if files were found.
    if len(iphex_files)==0:
        print("%%There are no iphex data files in the currect directory. Try again%%")
        return None, None
    else: 
        pass
    
    flight_dates = [] 
    
    for i in iphex_files:
        fname_split = re.split(r'_|-', os.path.basename(i))
        start_date = fname_split[3]
        
        flight_dates.append(datetime.strptime(start_date, '%Y%m%d').date().isoformat())
   
    print('Flight Dates:')
    for i in flight_dates:
        print('{}'.format(i))

    while True:
        num = input ("\n*Enter date in [yyyy-mm-dd] or Q to quit:") 
        if num.isdigit():
            if num in flight_dates:
                fdate = num
                print('Flight date {} is selected.'.format(num))
                break
            else: 
                print(num,"is not a valid flight date. Select a flight from the list.")
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            try:
                Fdate=datetime.strptime(num, '%Y-%m-%d').strftime("%Y-%m-%d")
                if Fdate in flight_dates:
                    fdate=Fdate
                    print('Flight date {} is selected.'.format(fdate))
                    break
                else: 
                    print(Fdate,"is not a valid flight date. Select a flight from the list:")
                    
            except ValueError:
                print('\n%%Invalid flight date format%% \nTry again.\n')
                
    selected_files = [path for path in Path(dataDir).rglob('IPHEX_CRS_L1B_'+fdate.replace('-','')+'*.nc')]
    selected_files = [os.path.normpath(i) for i in selected_files]
    return selected_files,fdate.replace('-','')

    
def select_time_iphex(selected_files):
    """
    User selects among the available flight time periods 
    Return the selected file name
    """
    start_times = []
    end_times = []
    
    time_periods = {}
    
    for i in selected_files:
        fname_split = re.split(r'_|-', os.path.basename(i))
        
        start_time = fname_split[4]
        start_time = start_time[:2] + ':' + start_time[2:4] + ':' + start_time[4:]
        start_times.append(start_time)
                
        end_time = fname_split[6]
        end_time = end_time[:2] + ':' + end_time[2:4] + ':' + end_time[4:6]
        end_times.append(end_time)
        
        time_periods[selected_files.index(i)+1] = start_time + ' to ' + end_time
        
    for i in time_periods:
        print('The IPHEX flight periods available for this date are: \n #{} - {}'.format(i, time_periods[i]))
        
    while True:
        num = input ("\n*Enter valid flight period no. or Q to quit: ") 
        if num.isdigit():
            if int(num) in time_periods:
                print('Flight period #{}: {} is selected.'.format(int(num),time_periods[int(num)]))
                break
            else: 
                print(int(num),"is not a valid flight period. Select a period no. from the list:")            
        elif num=='Q':
            return sys.exit("User selected 'quit'")
        else:
            print('\n%%Invalid flight No. format%% \nTry again.\n')
    return os.path.basename(selected_files[int(num)-1]) #Returns selected file name
 
def time2hrs(t):
    """ convert time to hours(float) """
    return t.hour+t.minute/60+t.second/3600

def totime(a):
    """Obtain time (hours) from a time-string"""
    try:
        t=datetime.strptime(a,'%H:%M:%S').time()
        return time2hrs(t)
    except ValueError:
        print('%%Invalid time. Try again%%')
        return None

def totime_impacts(t,d):
    """Obtain datetime object from a time-string"""
    try:
        t=datetime.strptime(t,'%H:%M:%S').time()
        d=datetime.strptime(d,'%Y-%m-%d').date()
        return datetime.combine(d,t) #returns datatime object containing date/time
    except ValueError:
        print('%%Invalid time. Try again%%')
        return None

def CRSsubset(ds,t1=None,t2=None):
    """
    Subset CRS dataset with selected time interval [t1,t2]
    User inputs valid options:
      1. First enter for interval start t1
         Q: quit program
         ALL: select entire flight
         valid time string in hh:mm:ss 
      2. Enter for interval end time t2
         valid time string in hh:mm:ss 
    If user enters subset into function directly, t1 and t2 must be strings
    Input CRS fullset datase (ds)
    Return CRS subset (cs) of selected interval
    """
    if(t1 and t2):
        t1=totime(t1)
        t2=totime(t2)
        return ds.where((ds.timed>=t1) & (ds.timed<=t2),drop=True)

    while True:
        inp=input("\n*Select subset starting in [hh:mm:ss] UTC"+
                  "\n or 'ALL' for entire flight"+
                  "\n or Q to quit: \n")
        if(inp=='Q'): return sys.exit("User selected 'quit'")
        elif(inp=='ALL'):
            t1,t2=ds.timed[0],ds.timed[-1]
            break
        else:
            t1=totime(inp)
            if(not t1): continue
            t2=None
            while not t2:
                inp2=input("\n*Select subset ending in [hh:mm:ss] UTC "+
                           "\n or Q to quit: \n")
                if(inp=='Q'): return sys.exit("User selected 'quit'")
                else:
                    t2=totime(inp2)
            break

    #--Make sure selected period within flight timeframe
    cs=ds.where((ds.timed>=t1) & (ds.timed<=t2),drop=True)
    if(len(cs.timed)==0): print("%%No data found in selected period."+
                               "\n  Data missing or selection beyond data range.")
    return cs

def CRSsubset_goesrplt(ds,t1=None,t2=None):
    """
    Subset CRS dataset with selected time interval [t1,t2]
    User inputs valid options:
      1. First enter for interval start t1
         Q: quit program
         ALL: select entire flight
         valid time string in hh:mm:ss 
      2. Enter for interval end time t2
         valid time string in hh:mm:ss
    If user enters subset into function directly, t1 and t2 must be strings
    Input CRS fullset datase (ds)
    Return CRS subset (cs) of selected interval
    """
    if(t1 and t2):
        t1=totime(t1)
        t2=totime(t2)
        return ds.where((ds.time>=t1) & (ds.time<=t2),drop=True)

    while True:
        inp=input("\n*Select subset starting in [hh:mm:ss] UTC"+
                  "\n or 'ALL' for entire flight"+
                  "\n or Q to quit: \n")
        if(inp=='Q'): return sys.exit("User selected 'quit'")
        elif(inp=='ALL'):
            t1,t2=ds.time[0],ds.time[-1]
            break
        else:
            t1=totime(inp)
            if(not t1): continue
            t2=None
            while not t2:
                inp2=input("\n*Select subset ending in [hh:mm:ss] UTC"+
                           "\n or Q to quit: \n")
                if(inp=='Q'): return sys.exit("User selected 'quit'")
                else:
                    t2=totime(inp2)
            break

    #--Make sure selected period within flight timeframe
    cs=ds.where((ds.time>=t1) & (ds.time<=t2),drop=True)
    if(len(cs.time)==0): print("%%No data found in selected period."+
                               "\n  Data missing or selection beyond data range.")
    return cs

def CRSsubset_impacts(ds,t0,t1=None, d1=None, t2=None, d2=None):
    """
    Subset CRS dataset with selected time and date interval [t1,d1,t2,d2] 
    User inputs valid options:
      1. First enter for interval start t1
         Q: quit program
         ALL: select entire flight
         valid time string in hh:mm:ss 
      2. Enter for interval start date d1
         in YYYY-MM-DD
      3. Enter for interval endtime t2
         valid time string in hh:mm:ss
      4. Enter for interval end date d2
         in YYYY-MM-DD
    If user enters subset into function directly, t1,d1,t2,and d2 must be strings
    Input CRS fullset datase (ds)
    Return CRS subset (cs) of selected interval
    """
    time_data = ds['Time']['Data']['TimeUTC']
    time_utc = [(t0+timedelta(seconds=float(s))) for s in time_data] #datetime objects
    str_times = [x.strftime("%H:%M:%S") for x in time_utc]
    time_dates = [x.strftime("%Y-%m-%d") for x in time_utc]
    
    if(t1 and t2):
        start=totime_impacts(t1,d1)
        end=totime_impacts(t2,d2)
        subset = [num for num in time_utc if num >=start and num <=end]
        return subset

    while True:
        inp=input("\n*Select subset starting time in [hh:mm:ss] UTC"+
                  "\n or 'ALL' for entire flight"+
                  "\n or Q to quit: \n")
        if(inp=='Q'): return sys.exit("User selected 'quit'")
        elif(inp=='ALL'):
            subset = time_utc
            return subset
        elif inp in str_times:
            t1=inp
            break
        else:
            print(inp,"is not a valid flight time and/or format. Try again.")
    while True:
        inp2=input("\n*Select subset starting date in [YYYY-MM-DD] UTC or Q to quit:")
        if(inp2=='Q'): return sys.exit("User selected 'quit'")
        elif inp2 in time_dates:
            d1=inp2
            break
        else:
            print(inp2,"is not a valid flight date and/or format. Try again.")
    while True:
        inp3=input("\n*Select subset ending time in [hh:mm:ss] UTC or Q to quit: ")
        if(inp3=='Q'): return sys.exit("User selected 'quit'")
        elif inp3 in str_times:
            t2=inp3
            break
        else:
            print(inp3,"is not a valid flight time and/or format. Try again.") 
    while True:
        inp4=input("\n*Select subset ending date in [YYYY-MM-DD] UTC or Q to quit:")
        if(inp4=='Q'): return sys.exit("User selected 'quit'")
        elif inp4 in time_dates:
            d2=inp4
            break
        else:
            print(inp4,"is not a valid flight date and/or format. Try again.")
        
    start=totime_impacts(inp,inp2)
    end=totime_impacts(inp3,inp4)
    subset = [num for num in time_utc if num >=start and num <=end]
    
    #--Make sure selected period within flight timeframe
    if(len(subset)==0): print("%%No data found in selected period."+
                               "\n  Data missing or selection beyond data range.")
    return subset 

def radarCmaps():
    """
    Make Color maps for radar Ref and DopV
    User can use predefined color maps in cmaps
    Return color maps
    """
    basecmp = cm.get_cmap('gist_ncar', 256)
    newcols = basecmp(np.linspace(0, 1, 200))
    topoff  = cm.get_cmap('gray', 128)
    combo   = np.vstack((newcols[:180,:],topoff(np.linspace(0.7, 1, 20))))
    aerocmp = ListedColormap(combo, name='aerocmp')
    cmaps  ={'Ref':aerocmp,'DopV':cm.gist_ncar}
    return cmaps

def plot_CRS2D(datap,xvar,ZB,plot_start,plot_end,reverseZ=True):
    """
    datap: Variables to be plotted, reflectivity and Doppler velocity
    xvar: Horizontal coord., we use [time]
    ZB: Vertical coord., we use radar [range]
        ZB=0 means at radar/airccraft location/altitude;
        ZB largest means near the ground
    plot_start: Plot start date/time object for plot title
    plot_end: Plot end date/time object for plot title
    Note that reverseZ=True would have data away from radar (large ZB) plotted
         at bottom, and near radar range plotted at top.
    Return image object "fig" than can be used to save the plot
    """
    vnames ={'Ref':"Reflectivity",'DopV':'Doppler Vel.'}
    units  ={'Ref':'[dBZ]',       'DopV':'[m/s]'}
    levs   ={'Ref':np.arange(-20,40,2), 'DopV':np.arange(-20,20,2)} #User can adjust colorscale range and intervals
    
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(12, 6))
    fig.tight_layout()
    fig.subplots_adjust(top=0.9,bottom=0.1,hspace=0.2)

    for iv,vnm in enumerate(vnames):
        ax,lev,unit,cmp = axs[iv],levs[vnm],units[vnm],radarCmaps()[vnm]
        var=np.array([*zip(*datap[vnm])]) #<--move time to col dim (x), and altitude/range to row(y)
        xlab='Time (UTC)' if iv==1 else ''
        
        #Divide the flight period into multiple segments and plot separately 
        #for more efficient memory usage
        div =int(len(xvar)/9)
        
        cp = ax.contourf(xvar[:div], ZB, var[:,:div],lev,cmap=cmp)
        cp = ax.contourf(xvar[:div*2], ZB, var[:,:div*2],lev,cmap=cmp)
        cp = ax.contourf(xvar[div*2:div*3], ZB, var[:,div*2:div*3],lev,cmap=cmp)
        cp = ax.contourf(xvar[div*3:div*4], ZB, var[:,div*3:div*4],lev,cmap=cmp)
        cp = ax.contourf(xvar[div*4:div*5], ZB, var[:,div*4:div*5],lev,cmap=cmp)
        cp = ax.contourf(xvar[div*5:div*6], ZB, var[:,div*5:div*6],lev,cmap=cmp)
        cp = ax.contourf(xvar[div*6:div*7], ZB, var[:,div*6:div*7],lev,cmap=cmp)
        cp = ax.contourf(xvar[div*7:div*8], ZB, var[:,div*7:div*8],lev,cmap=cmp)
        cp = ax.contourf(xvar[div*8:], ZB, var[:,div*8:],lev,cmap=cmp)
        
        ax.set_ylabel('Range from Radar [km]')
        ax.set_xlabel(xlab)
        if(reverseZ):
            ax.set_ylim(ymin=20,ymax=5)
            ytpos=4.5
        else:
            ax.set_ylim(ymin=5,ymax=20)
            ytpos=20.6

        ax.text(xvar[int(len(xvar)*.5)],ytpos,vnames[vnm],
               {'fontsize':13,'ha':'center'})
        
        #Extract the number of seconds over the entire flight period
        period_sec = (xvar[-1] - xvar[0]).seconds 
        
        #Place time ticks on the x-axis of plot based on flight period length
        # User can manually change this value to preferred number of ticks by replacing the "6" value
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=int(period_sec/6))) 
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S')) #<--Format times on x-axis to hh:mm:ss
        
        #Create plot title based on file dates; a different title is given based on whether the data
        #covers a single date or multiple dates
        if plot_start.date() != plot_end.date():
            plot_title1 = 'CRS Reflectivity and Doppler Velocity ' + plot_start.strftime("%B %d, %Y") + ' - ' + plot_end.strftime("%B %d, %Y")
            fig.suptitle(plot_title1,fontsize=14,x=0.415)
        else:
            plot_title2 = 'CRS Reflectivity and Doppler Velocity ' + plot_start.strftime("%B %d, %Y")
            fig.suptitle(plot_title2,fontsize=14,x=0.415)
        
        #Create and label colorbar
        clb=fig.colorbar(cp,ax=ax) 
        clb.set_label(unit)
        print("Fig.{} is done for {}".format(iv, vnm))

    plt.show()
    return fig

def SAVEsubset(cs,fig,fname,dirpath,start,end):
    """
    User selects whether to save the plot image
    cs:  selected subset dataset
    fig: radar image of cs 
    fname: original CRS file name
    dirpath: where saved image will be located
    start: start date/time of plot
    end: end date/time of plot 
    """
    Save=input("\n*Save plot(y/n)?")
    if(Save.lower()=='y'):
        campaign=fname.split('_')[0]
        instr=fname.split('_')[1]
        fig.savefig(os.path.join(dirpath, campaign+ '_'+instr+ '_'+start+ '_'+end+'.png'),dpi=100,bbox_inches='tight')
        plt.close(fig)
        print("Image saved to ", dirpath+campaign+ '_'+instr+ '_'+start+ '_'+end+'.png\n') 
    else: 
        print("No image was saved.\n")         


