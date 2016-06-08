###############################
#      FUNCTION MODULES       #
###############################

# Imports

import random as random
import numpy as np
import math as math

# 1. IMPORTING ANTENNA DISCRIMINATOR VALUES CORRESPONDING TO ANGLES TO BORESIGHT

antenna_File = open('antenna_pattern.txt', 'r')
print(antenna_File)
ant_Pattern_List = [line.split('\t') for line in antenna_File.readlines()]
ant_Pattern_List_copy = []

for indx_1 in ant_Pattern_List:
    outer_List = []
    for indx_2 in indx_1:
        outer_List.append(float(indx_2))
    ant_Pattern_List_copy.append(outer_List)

def antenna_Discrimination(angle):
    for indx_1 in ant_Pattern_List_copy:
        if ( angle >= indx_1[0] and angle < (indx_1[0] + 1)):
            return indx_1[1]


# 2. ASSIGNING RANDOM LOCATION AND DIRECTION TO A USER TRYING TO MAKE A CALL
#    AND CALCULATING ITS DISTANCE FROM THE ANTENNA

def location_Assign(i,road_Length_m,direction,perp_Distance_m):
    location = random.uniform(0, road_Length_m)
    #print("Random Location = " + str(location))
    rndm_Toss_2 = random.random()
    if(rndm_Toss_2 <= 0.5):
        vehicle_Direction = direction[0]
    else:
        vehicle_Direction = direction[1]
    i.append(location)
    i.append(vehicle_Direction)


    # Calculate Distance from the antenna
    location = i[1]
    if(location == road_Length_m/2):
        distance_From_Antenna_m = perp_Distance_m
    elif(location < road_Length_m/2):
        distance_From_Antenna_m = math.sqrt(math.pow(((road_Length_m/2) - location),2) + math.pow(perp_Distance_m,2))
    else:
        distance_From_Antenna_m = math.sqrt(math.pow((location - (road_Length_m/2)),2) + math.pow(perp_Distance_m,2))

    i.append(distance_From_Antenna_m)

    return(i)

    '''print statements'''
    #print('\n\n\n')
    #print("Location from road : " + str(location) + "\nVehicle direction:" + str(vehicle_Direction) + "\nDiagonal Distance:" + str(distance_From_Antenna_m))
    #print('\n\n\n')

# 3. CALCULATING FADING LOSS

def fading_Calc():
    # nr.normal of real and imag, then taking absolute, we get linear values, converting them to dB and finding the second minimum one

    real_Part = np.random.normal(0,1,10)
    imag_Part = np.random.normal(0,1,10)
    gaussian_Dist = real_Part + (imag_Part*(1j))

    Rayleigh_Values = np.absolute(gaussian_Dist)
    '''Rayleigh_Values_dB = []
    for indx_2 in Rayleigh_Values:
        Rayleigh_Values_dB.append(10*math.log10(indx_2))'''

    '''print statements'''
    #print("Rayleigh Values : " + str(Rayleigh_Values))
    
    fading_Value_dB = np.partition(Rayleigh_Values,1)[1]

    return (fading_Value_dB)


# 4. CALCULATING PROPAGATION LOSS

def propagation_Loss(alpha_Freq_MHz, beta_Freq_MHz, mobile_Height_m, bstn_Ant_Height_m, distance_From_Antenna_m):
    # For antenna alpha
    '''Look up units once online'''

    a_hm_alpha = (((1.1 * math.log10(alpha_Freq_MHz)) - 0.7) * mobile_Height_m) - ((1.56 * math.log10(alpha_Freq_MHz)) - 0.8)
    propagation_Loss_dB_alpha = 69.55 + (26.16 * math.log10(alpha_Freq_MHz)) - (13.82 * math.log10(bstn_Ant_Height_m))\
                        + ((44.9 - (6.55 * math.log10(bstn_Ant_Height_m))) * math.log10(distance_From_Antenna_m/1000)) - a_hm_alpha

    # For antenna beta

    a_hm_beta = (((1.1 * math.log10(beta_Freq_MHz)) - 0.7) * mobile_Height_m) - ((1.56 * math.log10(beta_Freq_MHz)) - 0.8)
    propagation_Loss_dB_beta = 69.55 + (26.16 * math.log10(beta_Freq_MHz)) - (13.82 * math.log10(bstn_Ant_Height_m))\
                        + ((44.9 - (6.55 * math.log10(bstn_Ant_Height_m))) * math.log10(distance_From_Antenna_m/1000)) - a_hm_beta

    '''print statements'''
    #print("      Propagation loss alpha antenna : " + str(propagation_Loss_dB_alpha))
    #print("      Propagation loss beta antenna : " + str(propagation_Loss_dB_beta))

    return((propagation_Loss_dB_alpha, propagation_Loss_dB_beta))

# 5. CALCULATING EIRP

def EIRP_Calc_alpha(Tx_Power_dBm, line_Loss_dB, ant_Gain_boresight_dBi, location, road_Length_m, perp_Distance_m):
    ''' Check dB or dBm stuff online'''
            
    EIRP_boresight = Tx_Power_dBm - line_Loss_dB + ant_Gain_boresight_dBi


    # Calculating the vector values for the mobile at Current Location
    if( location == road_Length_m/2):
        Caller_yCoord = 0
    elif( location < road_Length_m/2):
        Caller_yCoord = road_Length_m/2 - location
    else:
        Caller_yCoord = -(location - road_Length_m/2)

    vector_Caller = np.array([perp_Distance_m, Caller_yCoord])
    absolute_Caller = np.linalg.norm(vector_Caller)

    # BORESIGHT ANGLE FOR ALPHA SECTOR

    vector_alpha = np.array([0,1])
    absolute_alpha = np.linalg.norm(vector_alpha)
    dot_Product_alpha = np.dot(vector_alpha,vector_Caller)
    angle_Theta_alpha_rad = np.arccos(dot_Product_alpha/(absolute_alpha*absolute_Caller))

    # Converting from Radians to Degrees
    angle_Theta_alpha_deg = math.degrees(angle_Theta_alpha_rad)

    # BORESIGHT ANGLE FOR BETA SECTOR

    vector_beta = np.array([math.sqrt(3)/2, -1/2])
    absolute_beta = np.linalg.norm(vector_beta)
    dot_Product_beta = np.dot(vector_beta,vector_Caller)
    angle_Theta_beta_rad = np.arccos(dot_Product_beta/(absolute_beta*absolute_Caller))

    # Converting from Radians to Degrees
    angle_Theta_beta_deg = math.degrees(angle_Theta_beta_rad)

    return ((EIRP_boresight, angle_Theta_alpha_deg, angle_Theta_beta_deg))
