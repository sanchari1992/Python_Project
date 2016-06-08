# Notes (to be removed)
##############################################
#######         MOST IMPORTANT:      #########
#                                            #
#                   SCRIPTS                  #
#                                            #
##############################################
#
# Caller Number, Location, Vehicle Direction, Distance From Antenna, Caller Sector, Allocated Channel, Time Duration]]
# 1. Write into Reports (per hour + overall)
# 2. Remove trash
# 3. IN Q4., SAME RANDOM NUMBERS OF WHAT??

#print("\n\nQ1. 6 Hours 6 Km Road 160 Users\n\n")
#print("\n\nQ2. 6 Hours 8 Km Road 160 Users\n\n")
#print("\n\nQ3. 6 Hours 6 Km Road 320 Users\n\n")
#print("\n\nQ4. PART A 6 Hours 6 Km Road 320 Users HoM = 5dB Random Seed\n\n")
#print("\n\nQ4. PART B 6 Hours 6 Km Road 320 Users HoM = 0dB Random Seed\n\n")


# Imports

import random as random
import numpy as np
import math as math


# Importing other modules

import sys
ant_Disc_Path = "////C://Users//sanch_000//Documents//AA Semester 2//ENTS656//PYTHON PROJECT"
sys.path.append(ant_Disc_Path)
import Module as Module


# SEED FUNCTION
#np.random.seed(10)
#random.seed(10)

# General Parameters

road_Length_m = 6000
sim_Step_Size_sec = 1
tot_Sim_Time_hour = 1

# Basestation Properties

bstn_Ant_Height_m = 50
perp_Distance_m = 20
Tx_Power_dBm = 43
line_Loss_dB = 2
ant_Gain_boresight_dBi = 15
traffic_Channels_perSector = 15
alpha_Freq_MHz = 860
beta_Freq_MHz = 865

# Mobile Properties

mobile_Height_m = 1.5
handoff_Margin_dB = 3
mobile_Rx_Threshold_dBm = -102

# User Properties

number_Of_Users = 160
call_Rate_perHour = 2
call_Duration_mins = 3
user_Speed_mps = 15
direction = ['North', 'South']
caller_Sector = ['alpha','beta']


# SHADOWING VALUE CALCULATION
# WE KEEP IT IN THE MAIN PROGRAM AS WE DO NOT WANT ITS VALUES TO CHANGE DYNAMICALLY EVERYTIME WE CALL IT.

'''Number of 10m sections in then given road length'''
section = 10
shadow_Sections = int(road_Length_m/section)
shadow_Values_List = []
for index_1 in range(0,shadow_Sections-1):
    shadow_Value = np.random.normal(0,2)
    shadow_Values_List.append([index_1*10, shadow_Value])
# End of Shadowing Calculation


# Caller Lists

all_Channel_List_alpha = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
free_Channel_List_alpha = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
busy_Channel_List_alpha = []

all_Channel_List_beta = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
free_Channel_List_beta = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
busy_Channel_List_beta = []

caller_Profile = []
for j in range(1,number_Of_Users+1):
    caller_Profile.append([j])
'''print(caller_Profile)'''

# User calling check

new_Call_Flag = 'N'

# Handoff Flag
handOff_Flag = 'N'

# setting time to run parameters

run_Time = 3600*6
hour_Count = 0

# Parameters to save one hour counts

call_Attempts_Hour = 0
call_Established_Hour_alpha = 0
call_Established_Hour_beta = 0
successful_Calls_Hour_alpha = 0
successful_Calls_Hour_beta = 0
successful_HandOffs_Hour_alpha = 0
successful_HandOffs_Hour_beta = 0
failed_HandOffs_Hour_alpha = 0
failed_HandOffs_Hour_beta = 0
dropped_Calls_Hour_alpha = 0
dropped_Calls_Hour_beta = 0
blocked_Calls_Capacity_Hour_alpha = 0
blocked_Calls_Capacity_Hour_beta = 0

total_Call_Attempts_Hour = 0
total_Call_Established_Hour_alpha = 0
total_Call_Established_Hour_beta = 0
total_Successful_Calls_Hour_alpha = 0
total_Successful_Calls_Hour_beta = 0
total_Successful_HandOffs_Hour_alpha = 0
total_Successful_HandOffs_Hour_beta = 0
total_Failed_HandOffs_Hour_alpha = 0
total_Failed_HandOffs_Hour_beta = 0
total_Dropped_Calls_Hour_alpha = 0
total_Dropped_Calls_Hour_beta = 0
total_Blocked_Calls_Capacity_Hour_alpha = 0
total_Blocked_Calls_Capacity_Hour_beta = 0

# Implementation to make code run every 1 second

for t in range(1,run_Time+1):
    # Traversing LOOP for every user
    for i in caller_Profile:
        if (len(i) == 1):
            # 1. First, Check whether user choses to make a call
            # 2. Picking up a random location along the road (starting from Northernmost point of road as 0 metre ,
            # 3. Providing it with a random direction (either North or South)
            # 4. Calculating it's distance from the antenna

            prob_Making_Call = (call_Rate_perHour/3600) * sim_Step_Size_sec
            rndm_Toss_1 = random.random()
            user_Calls = 'N'
            if (rndm_Toss_1 <= prob_Making_Call):
                # User wants to make a call
                user_Calls = 'Y'
                call_Attempts_Hour = call_Attempts_Hour + 1

            if (user_Calls == 'Y'):
                # CALL FUNCTION TO GENERATE RANDOM LOCATION AND DIRECTION
                j = []
                j = Module.location_Assign(i,road_Length_m,direction,perp_Distance_m)
                for indx in range(len(j)):
                    i[indx] = (j[indx])

                location = i[1]
                vehicle_Direction = i[2]
                distance_From_Antenna_m = i[3]

        # Check if User has an Active call from before
        if(len(i) > 6):
            user_Calls = 'Y'

        # Set up EIRP, Losses and RSL to be checked whether successful call establishment is possible or not
        if (user_Calls == 'Y'):
            # FADING VALUE CALCULATION
            fading_Value_dB_alpha = Module.fading_Calc()
            fading_Value_dB_beta = Module.fading_Calc()
            
            # End of Fading Value Calculation

            # PATHLOSS using OKAMURA-HATA MODEL
            prop_Loss_tuple = Module.propagation_Loss(alpha_Freq_MHz, beta_Freq_MHz, mobile_Height_m, bstn_Ant_Height_m, distance_From_Antenna_m)
            propagation_Loss_dB_alpha = prop_Loss_tuple[0]
            propagation_Loss_dB_beta = prop_Loss_tuple[1]
            
            # SHADOW VALUE for that section of road
            location = i[1]
            for indx_1 in shadow_Values_List:
                if(location >= indx_1[0] and location < (indx_1[0] + 10)):
                    shadow_Value = indx_1[1]

            # EIRP CALCULATION ( Boresight + Antenna Discrimination)
            angle_tuple = Module.EIRP_Calc_alpha(Tx_Power_dBm, line_Loss_dB, ant_Gain_boresight_dBi, location, road_Length_m, perp_Distance_m)
            EIRP_boresight = angle_tuple[0]
            angle_Theta_alpha_deg = angle_tuple[1]
            angle_Theta_beta_deg = angle_tuple[2]

            # Fetching the Antenna Discriminator value from the Antenna Pattern Module for alpha sector
            ant_Discr_alpha = Module.antenna_Discrimination(angle_Theta_alpha_deg)
            '''print("Angle = " + str(angle_Theta_alpha_deg) + "Antenna Disc" + str(ant_Discr_alpha))'''

            # Calculating the RSL for the alpha Sector
            path_Loss = propagation_Loss_dB_alpha - shadow_Value + fading_Value_dB_alpha
            RSL_alpha = EIRP_boresight - ant_Discr_alpha - path_Loss


            # Fetching the Antenna Discriminator value from the Antenna Pattern Module for beta sector
            ant_Discr_beta = Module.antenna_Discrimination(angle_Theta_beta_deg)
            '''print("Angle = " + str(angle_Theta_beta_deg) + "Antenna Disc" + str(ant_Discr_beta))'''

            # Calculating the RSL for the beta Sector
            path_Loss = propagation_Loss_dB_beta - shadow_Value + fading_Value_dB_beta
            RSL_beta = EIRP_boresight - ant_Discr_beta - path_Loss

            # SELECTING THE SECTOR WITH HIGHER RSL VALUE
            # If both RSL values turn up equal, choose alpha for vehicles moving North and beta for vehicles moving South

            # Updating the caller list such as [Caller Number, Location, Direction, Distance from Antenna, Caller Sector]
            # If Caller Sector is not in list, append it.
            # Else Modify it.
            # As Serving Sector < Other Sector, I SWAP the Serving and Other Sectors.

            handOff_Flag = 'N'
            if(RSL_alpha > RSL_beta):
                RSL_serving = RSL_alpha
                call_Sector_Active = caller_Sector[0]
                len_i = len(i)
                if(len_i == 4):
                    i.append(caller_Sector[0])
                    new_Call_Flag = 'Y'
                    RSL_other = RSL_beta
                else:
                    new_Call_Flag = 'N'
                    if(i[4] != caller_Sector[0]):
                        # Serving Sector is not the Sector with Maximum RSL:
                        # Could be one of the TWO Cases
                        # 1) Handoff Situation
                        # 2) No Channel available in HIGHER RSL Sector
                        #        -In this case, continue serving for this sector
                        RSL_other = RSL_beta
                        if(RSL_other >= mobile_Rx_Threshold_dBm):
                                i[4] = caller_Sector[0]
                                handOff_Flag = 'Y'
                                        

            elif(RSL_alpha < RSL_beta):
                RSL_serving = RSL_beta
                call_Sector_Active = caller_Sector[1]
                len_i = len(i)
                if(len_i == 4):
                    i.append(caller_Sector[1])
                    new_Call_Flag = 'Y'
                    RSL_other = RSL_alpha
                else:
                    new_Call_Flag = 'N'
                    if(i[4] != caller_Sector[1]):
                        # Serving Sector is not the Sector with Maximum RSL:
                        # Could be one of the TWO Cases
                        # 1) Handoff Situation
                        # 2) No Channel available in HIGHER RSL Sector
                        #        -In this case, continue serving for this sector
                        RSL_other = RSL_alpha
                        if(RSL_other >= mobile_Rx_Threshold_dBm):
                                i[4] = caller_Sector[1]
                                handOff_Flag = 'Y'
                                        
            else:
                RSL_serving = RSL_alpha
                new_Call_Flag = 'N'
                # If already contains a serving sector, let it be. Else update.
                if(len(i) == 4):
                    new_Call_Flag = 'Y'
                    if(vehicle_Direction == 'North'):
                        call_Sector_Active = caller_Sector[0]
                        i.append(caller_Sector[0])
                    else:
                        call_Sector_Active = caller_Sector[1]
                        i.append(caller_Sector[1])

            # HANDOFF

            if(handOff_Flag == 'Y'):
                #if(RSL_other > (RSL_serving + handoff_Margin_dB)):
                # UNDERSTAND THIS CHANGE IF WORKS
                if(RSL_serving > (RSL_other + handoff_Margin_dB)):
                    #print("TEST HANDOFF")
                    changed_Sector = i[4]
                    if(changed_Sector == 'alpha'):
                        len_alpha = len(free_Channel_List_alpha)
                        if(len_alpha > 0):
                            # SUCCESSFUL HANDOFF
                            #print("SUCCESSFUL HANDOFF")
                            prev_Channel = i[5]
                            i[5] = free_Channel_List_alpha[0]
                            free_Channel_alpha = free_Channel_List_alpha[0]
                            # ALLOCATE CHANNEL IN NEW SECTOR
                            busy_Channel_List_alpha.append(free_Channel_alpha)
                            free_Channel_List_alpha.remove(free_Channel_alpha)
                            # FREE CHANNEL FROM OLD SECTOR
                            free_Channel_List_beta.append(prev_Channel)
                            busy_Channel_List_beta.remove(prev_Channel)
                            successful_HandOffs_Hour_beta = successful_HandOffs_Hour_beta + 1
                        else:
                            # The Call will continue as usual on the previous sector
                            i[4] = 'beta'
                            # HANDOFF FAILURE. CALL CONTINUES ON PREVIOUS SECTOR AS USUAL
                            #print("HANDOFF FAILURE. CALL CONTINUES ON PREVIOUS SECTOR AS USUAL")
                            failed_HandOffs_Hour_beta = failed_HandOffs_Hour_beta + 1
                    elif(changed_Sector == 'beta'):
                        len_beta = len(free_Channel_List_beta)
                        if(len_beta > 0):
                            # SUCCESSFUL HANDOFF
                            #print("SUCCESSFUL HANDOFF")
                            prev_Channel = i[5]
                            i[5] = free_Channel_List_beta[0]
                            free_Channel_beta = free_Channel_List_beta[0]
                            # ALLOCATE CHANNEL IN NEW SECTOR
                            busy_Channel_List_beta.append(free_Channel_beta)
                            free_Channel_List_beta.remove(free_Channel_beta)
                            # FREE CHANNEL FROM OLD SECTOR
                            free_Channel_List_alpha.append(prev_Channel)
                            busy_Channel_List_alpha.remove(prev_Channel)
                            successful_HandOffs_Hour_alpha = successful_HandOffs_Hour_alpha + 1
                        else:
                            # The Call will continue as usual on the previous sector
                            i[4] = 'alpha'
                            # HANDOFF FAILURE. CALL CONTINUES ON PREVIOUS SECTOR AS USUAL
                            #print("HANDOFF FAILURE. CALL CONTINUES ON PREVIOUS SECTOR AS USUAL")
                            failed_HandOffs_Hour_alpha = failed_HandOffs_Hour_alpha + 1
                else:
                    changed_Sector = i[4]
                    # NO POTENTIAL HANDOFF
                    if(changed_Sector == 'alpha'):
                        i[4] = 'beta'
                    if(changed_Sector == 'beta'):
                        i[4] = 'alpha'

            # COMPARING RSL SERVER WITH RSL THRESHOLD
            # If new Call Request Call will be connected and issued a Random CALL DURATION
            # If continuing Call and NOT HANDOFF, Call will proceed as usual
            # If continuing Call and HANDOFF, (FIGURE OUT LATER)
            # If RSL SERVER < RSL THRESHOLD, CALL WILL DISCONNECT IN ALL SCENARIOS

            #print("RSL SERVING = " + str(RSL_serving) + "\nRSL THRESHOLD = " + str(mobile_Rx_Threshold_dBm))
            if (RSL_serving >= mobile_Rx_Threshold_dBm):
                # Check if a channel is available on that sector
                # Proceed to connect call

                # Allotting Channels
                call_Active = 'N'

                # IF THIS IS A NEWLY ESTABLISHED CALL IN THIS LOOP
                if(len(i) < 6):
                    if (call_Sector_Active == 'alpha'):
                        if(len(free_Channel_List_alpha) > 0):
                            free_Channel_alpha = free_Channel_List_alpha[0]
                            # The randomly selected channel is free, so can be utilized
                            # Allocate this channel and establish a call
                            i.append(free_Channel_alpha)
                            busy_Channel_List_alpha.append(free_Channel_alpha)
                            free_Channel_List_alpha.remove(free_Channel_alpha)
                            call_Active = 'Y'
                            # RECORD AS Active Call
                            #print("Call established. ACTIVE CALL.")
                            call_Established_Hour_alpha = call_Established_Hour_alpha + 1

                            # CALL DURATION INSERTION RANDOMLY FOR THE NEW CALL
                            # Present Caller Profile Format
                            # [[Caller Number, Location, Direction, Distance from Antenna, Caller Sector, Channel, Call Duration]
                            active_Call_Duration = np.random.exponential(call_Duration_mins*60)
                            #print("Active call duration = " + str(active_Call_Duration))
                            i.append(active_Call_Duration)

                        else:
                            # No channel available
                            # RECORD AS Dropped Call Due To CAPACITY OF THE ORIGINAL SECTOR ONLY
                            #print("Dropped Call Due To CAPACITY OF THE ORIGINAL SECTOR ONLY")
                            blocked_Calls_Capacity_Hour_alpha = blocked_Calls_Capacity_Hour_alpha + 1
                            temp = i[0]
                            del i[:]
                            i.append(temp)

                    elif (call_Sector_Active == 'beta'):
                        if(len(free_Channel_List_beta) > 0):
                            free_Channel_beta = free_Channel_List_beta[0]
                            # The randomly selected channel is free, so can be utilized
                            # Allocate this channel and establish a call
                            i.append(free_Channel_beta)
                            busy_Channel_List_beta.append(free_Channel_beta)
                            free_Channel_List_beta.remove(free_Channel_beta)
                            call_Active = 'Y'
                            # RECORD AS Active Call
                            #print("Call established. ACTIVE CALL.")
                            call_Established_Hour_beta = call_Established_Hour_beta + 1

                            # CALL DURATION INSERTION RANDOMLY FOR THE NEW CALL
                            # Present Caller Profile Format
                            # [[Caller Number, Location, Direction, Distance from Antenna, Caller Sector, Channel, Call Duration]
                            active_Call_Duration = np.random.exponential(call_Duration_mins*60)
                            #print("Active call duration = " + str(active_Call_Duration))
                            i.append(active_Call_Duration)
                                    
                        else:
                            # No channel available
                            # RECORD AS Dropped Call Due To CAPACITY OF THE ORIGINAL SECTOR ONLY
                            #print("Dropped Call Due To CAPACITY OF THE ORIGINAL SECTOR ONLY")
                            blocked_Calls_Capacity_Hour_beta = blocked_Calls_Capacity_Hour_beta + 1
                            temp = i[0]
                            del i[:]
                            i.append(temp)
                                
            else:
                # Call dropped
                # Remove Sector Info
                i.pop(4)
                if(new_Call_Flag == 'N'):
                    i.pop(5)
                    if(i[4] == 'alpha'):
                        busy_Channel_List_alpha.remove(i[4])
                        free_Channel_List_alpha.append(i[4])
                        i.pop(4)
                        # RECORD AS DROPPED CALL DUE TO SIGNAL STRENGTH FOR THAT SECTOR
                        #print("DROPPED CALL DUE TO SIGNAL STRENGTH FOR THAT SECTOR")
                        dropped_Calls_Hour_alpha = dropped_Calls_Hour_alpha + 1
                    elif(i[4] == 'beta'):
                        busy_Channel_List_beta.remove(i[4])
                        free_Channel_List_beta.append(i[4])
                        i.pop(4)
                        # RECORD AS DROPPED CALL DUE TO SIGNAL STRENGTH FOR THAT SECTOR
                        #print("DROPPED CALL DUE TO SIGNAL STRENGTH FOR THAT SECTOR")
                        dropped_Calls_Hour_beta = dropped_Calls_Hour_beta + 1
                # CHANGE 1
                temp = i[0]
                del i[:]
                i.append(temp)

            # CALL DURATION DECREMENTATION
            if(len(i) == 7):
                # Decrement call duration left by 1 second
                i[6] = i[6] - 1
                temp_2 = i[6]
                if(temp_2 < 1):
                    # CALL COMPLETED SUCCESSFULLY
                    # Reset all the necessary parameters (FREE THE USER)
                    # FREE CHANNEL
                    active_Sector = i[4]
                    channel_Pres_1 = i[5]
                    if(active_Sector == 'alpha'):
                        busy_Channel_List_alpha.remove(channel_Pres_1)
                        free_Channel_List_alpha.append(channel_Pres_1)
                        #print("CALL COMPLETED SUCCESSFULLY")
                        successful_Calls_Hour_alpha = successful_Calls_Hour_alpha + 1
                    elif(active_Sector == 'beta'):
                        busy_Channel_List_beta.remove(channel_Pres_1)
                        free_Channel_List_beta.append(channel_Pres_1)
                        #print("CALL COMPLETED SUCCESSFULLY")
                        successful_Calls_Hour_beta = successful_Calls_Hour_beta + 1
                    temp = i[0]
                    del i[:]
                    i.append(temp)

            # UPDATE LOCATION
            if (len(i) > 2):
                caller_Dir = i[2]
                # IF MOVING SOUTH:
                if (caller_Dir == 'South'):
                    caller_Loc_Prev = i[1]
                    i[1] = caller_Loc_Prev + user_Speed_mps
                    caller_Loc = i[1]
                    if(caller_Loc >= road_Length_m):
                        length_i = len(i)
                        # USER MOVED OUT OF ROAD
                        if (length_i == 7):
                            # CALL COMPLETED SUCCESSFULLY
                            #print("CALL COMPLETED SUCCESSFULLY")
                            # FREE CHANNEL
                            active_Sector = i[4]
                            channel_Pres_2 = i[5]
                            if(active_Sector == 'alpha'):
                                busy_Channel_List_alpha.remove(channel_Pres_2)
                                free_Channel_List_alpha.append(channel_Pres_2)
                                successful_Calls_Hour_alpha = successful_Calls_Hour_alpha + 1
                            elif(active_Sector == 'beta'):
                                busy_Channel_List_beta.remove(channel_Pres_2)
                                free_Channel_List_beta.append(channel_Pres_2)
                                successful_Calls_Hour_beta = successful_Calls_Hour_beta + 1
                        temp1 = i[0]
                        del i[:]
                        i.append(temp1)

                # IF MOVING NORTH:
                if (caller_Dir == 'North'):
                    caller_Loc_Prev = i[1]
                    i[1] = caller_Loc_Prev - user_Speed_mps
                    caller_Loc = i[1]
                    if(caller_Loc <= 0):
                        length_i = len(i)
                        # USER MOVED OUT OF ROAD
                        if (length_i == 7):
                            # CALL COMPLETED SUCCESSFULLY
                            #print("CALL COMPLETED SUCCESSFULLY")
                            # FREE CHANNEL
                            active_Sector = i[4]
                            channel_Pres_3 = i[5]
                            if(active_Sector == 'alpha'):
                                busy_Channel_List_alpha.remove(channel_Pres_3)
                                free_Channel_List_alpha.append(channel_Pres_3)
                                successful_Calls_Hour_alpha = successful_Calls_Hour_alpha + 1
                            elif(active_Sector == 'beta'):
                                busy_Channel_List_beta.remove(channel_Pres_3)
                                free_Channel_List_beta.append(channel_Pres_3)
                                successful_Calls_Hour_beta = successful_Calls_Hour_beta + 1
                        temp2 = i[0]
                        del i[:]
                        i.append(temp2)

            # SET BACK DEFAULT PARAMETERS
            user_Calls = 'N'
            new_Call_Flag = 'N'

    # REPORT FOR BASESTATION EACH HOUR
    # 1. NO. OF CHANNELS CURRENTLY IN USE
    # 2. NO. OF CALL ATTEMPTS
    # 3. NO. OF SUCCESSFUL CALLS
    # 4. NO. OF SUCCESSFUL HANDOFFS
    # 5. NO. OF NUMBER OF HANDOFF FAILURES INTO AND OUT OF EACH SECTOR
    # 6. NO. OF CALL DROPS DUE TO LOW SIGNAL STRENGTH
    # 7. NO. OF BLOCKS DUE TO CAPACITY
    # 8. ANY OTHER INFORMATION
    if (t%3600 == 0):
        # An hour complete
        hour_Count = hour_Count + 1
        # 1.
        in_Use_Channels_alpha = len(busy_Channel_List_alpha)
        in_Use_Channels_beta = len(busy_Channel_List_beta)
        print("NO. OF CHANNELS CURRENTLY IN USE IN ALPHA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(in_Use_Channels_alpha))
        print("NO. OF CHANNELS CURRENTLY IN USE IN BETA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(in_Use_Channels_beta))

        # 2.
        print("\nNO. OF CALL ATTEMPTS AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(call_Attempts_Hour) + '\n')
        total_Call_Attempts_Hour = total_Call_Attempts_Hour + call_Attempts_Hour
        call_Attempts_Hour = 0
        # 3.
        print("NO. OF SUCCESSFUL CALLS IN ALPHA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(successful_Calls_Hour_alpha))
        print("NO. OF SUCCESSFUL CALLS IN BETA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(successful_Calls_Hour_beta))
        total_Successful_Calls_Hour_alpha = total_Successful_Calls_Hour_alpha + successful_Calls_Hour_alpha
        total_Successful_Calls_Hour_beta = total_Successful_Calls_Hour_beta + successful_Calls_Hour_beta
        successful_Calls_Hour_alpha = 0
        successful_Calls_Hour_beta = 0

        # 4.
        print("NO. OF SUCCESSFUL HANDOFFS IN ALPHA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(successful_HandOffs_Hour_alpha))
        print("NO. OF SUCCESSFUL HANDOFFS IN BETA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(successful_HandOffs_Hour_beta))
        total_Successful_HandOffs_Hour_alpha = total_Successful_HandOffs_Hour_alpha + successful_HandOffs_Hour_alpha
        total_Successful_HandOffs_Hour_beta = total_Successful_HandOffs_Hour_beta + successful_HandOffs_Hour_beta
        successful_HandOffs_Hour_alpha = 0
        successful_HandOffs_Hour_beta = 0

        # 5.
        print("NO. OF NUMBER OF HANDOFF FAILURES INTO AND OUT OF EACH SECTOR IN ALPHA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(failed_HandOffs_Hour_alpha))
        print("NO. OF NUMBER OF HANDOFF FAILURES INTO AND OUT OF EACH SECTOR IN BETA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(failed_HandOffs_Hour_beta))
        total_Failed_HandOffs_Hour_alpha = total_Failed_HandOffs_Hour_alpha + failed_HandOffs_Hour_alpha
        total_Failed_HandOffs_Hour_beta = total_Failed_HandOffs_Hour_beta + failed_HandOffs_Hour_beta
        failed_HandOffs_Hour_alpha = 0
        failed_HandOffs_Hour_beta = 0

        # 6.
        print("NO. OF CALL DROPS DUE TO LOW SIGNAL STRENGTH IN ALPHA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(dropped_Calls_Hour_alpha))
        print("NO. OF CALL DROPS DUE TO LOW SIGNAL STRENGTH IN BETA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(dropped_Calls_Hour_beta))
        total_Dropped_Calls_Hour_alpha = total_Dropped_Calls_Hour_alpha + dropped_Calls_Hour_alpha
        total_Dropped_Calls_Hour_beta = total_Dropped_Calls_Hour_beta + dropped_Calls_Hour_beta
        dropped_Calls_Hour_alpha = 0
        dropped_Calls_Hour_beta = 0
        
        # 7.
        print("NO. OF BLOCKS DUE TO CAPACITY IN ALPHA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(blocked_Calls_Capacity_Hour_alpha))
        print("NO. OF BLOCKS DUE TO CAPACITY IN BETA SECTOR AT THE END OF " + str(hour_Count) + "th HOUR = \t" + str(blocked_Calls_Capacity_Hour_beta) + "\n\n\n")
        total_Blocked_Calls_Capacity_Hour_alpha = total_Blocked_Calls_Capacity_Hour_alpha + blocked_Calls_Capacity_Hour_alpha
        total_Blocked_Calls_Capacity_Hour_beta = total_Blocked_Calls_Capacity_Hour_beta + blocked_Calls_Capacity_Hour_beta
        blocked_Calls_Capacity_Hour_alpha = 0
        blocked_Calls_Capacity_Hour_beta = 0

# 1.
total_In_Use_Channels_alpha = len(busy_Channel_List_alpha)
total_In_Use_Channels_beta = len(busy_Channel_List_beta)
print("NO. OF CHANNELS CURRENTLY IN USE IN ALPHA SECTOR AT THE END OF EXECUTION = \t" + str(total_In_Use_Channels_alpha))
print("NO. OF CHANNELS CURRENTLY IN USE IN BETA SECTOR AT THE END OF EXECUTION = \t" + str(total_In_Use_Channels_beta))
print("\nNO. OF CALL ATTEMPTS THIS HOUR AT THE END OF EXECUTION = \t" + str(total_Call_Attempts_Hour) + '\n')
print("NO. OF SUCCESSFUL CALLS THIS HOUR IN ALPHA SECTOR AT THE END OF EXECUTION = \t" + str(total_Successful_Calls_Hour_alpha))
print("NO. OF SUCCESSFUL CALLS THIS HOUR IN BETA SECTOR AT THE END OF EXECUTION = \t" + str(total_Successful_Calls_Hour_beta))
print("NO. OF SUCCESSFUL HANDOFFS THIS HOUR IN ALPHA SECTOR AT THE END OF EXECUTION = \t" + str(total_Successful_HandOffs_Hour_alpha))
print("NO. OF SUCCESSFUL HANDOFFS THIS HOUR IN BETA SECTOR AT THE END OF EXECUTION = \t" + str(total_Successful_HandOffs_Hour_beta))
print("NO. OF NUMBER OF HANDOFF FAILURES INTO AND OUT OF EACH SECTOR IN ALPHA SECTOR AT THE END OF EXECUTION = \t" + str(total_Failed_HandOffs_Hour_alpha))
print("NO. OF NUMBER OF HANDOFF FAILURES INTO AND OUT OF EACH SECTOR IN BETA SECTOR AT THE END OF EXECUTION = \t" + str(total_Failed_HandOffs_Hour_beta))
print("NO. OF CALL DROPS DUE TO LOW SIGNAL STRENGTH IN ALPHA SECTOR AT THE END OF EXECUTION = \t" + str(total_Dropped_Calls_Hour_alpha))
print("NO. OF CALL DROPS DUE TO LOW SIGNAL STRENGTH IN BETA SECTOR AT THE END OF EXECUTION = \t" + str(total_Dropped_Calls_Hour_beta))
print("NO. OF BLOCKS DUE TO CAPACITY IN ALPHA SECTOR AT THE END OF EXECUTION = \t" + str(total_Blocked_Calls_Capacity_Hour_alpha))
print("NO. OF BLOCKS DUE TO CAPACITY IN BETA SECTOR AT THE END OF EXECUTION = \t" + str(total_Blocked_Calls_Capacity_Hour_beta))

# PERCENTAGE OF CALL ATTEMPTS THAT HAVE A PROBLEM:
percent_Problem = ((total_Dropped_Calls_Hour_alpha + total_Dropped_Calls_Hour_beta \
                    + total_Blocked_Calls_Capacity_Hour_alpha + total_Blocked_Calls_Capacity_Hour_beta)/total_Call_Attempts_Hour)*100
print("PERCENTAGE OF CALL ATTEMPTS THAT HAVE A PROBLEM = \t" + str(percent_Problem))


# END OF CODE
