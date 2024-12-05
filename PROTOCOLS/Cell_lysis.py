# # Summary

# This protocol takes 100 uL of solution from the first column of the reservoir and puts it in well A2 of the
# first 96-well plate, then takes another 100uL from the reservoir (first column) and puts it in well A3 of 
# the 96-well plate; so on until reach well A11. At the end, mix each well 2 times from A2 to A11, and between 
# each well wash the tip in well A12 of the reservoir.
# If it is done for more than one plate, first do what was mentioned above for the first plate, and then do the
# same for the second, only this time it will take the 100 uL from column A2 of the reservoir.
# Therefore, it will be necessary to prepare manually in the reservoir a solution to wash the tips (e.g. bleach)
# in column A12 of the reservoir, and in each column you will use of the reservor (consider one column per 
# plate), you will have to put 10 mL of the lisis solution.



# # Labware needed for running this protocol:

# - Reservoir: nest_12_reservoir_15ml
# - 96 well plates: nest_96_wellplate_200ul_flat
# - Tipracks: opentrons_96_tiprack_300ul (this protocol will consider a tiprack for each plate)
# - Pipette: p300 single on left

# This protocol uses different coordinates for each labware. If you want to use the default coordinates, delete the line "labware.set_offset()" for each one.



## Protocol

import opentrons.execute
protocol = opentrons.execute.get_protocol_api('2.11')
#import opentrons.simulate
#protocol = opentrons.simulate.get_protocol_api('2.11')
metadata = {
    "apiLevel": "2.11",
    "protocolName": "Parasite lysis",
    "description": """Protocol for lysing parasites in a 96-well plate""",
    "author": "Aguero Franco Agustin, Didier Garnham Mercedes"
    }
protocol.home()

# LABWARE INPUTS

# Reservoir
reservoir_position=int(input("Reservoir position: "))
reservoir = protocol.load_labware("nest_12_reservoir_15ml", reservoir_position)
reservoir.set_offset(x=0.00, y=0.00, z=0.00)
# Plates and tipracks
plates=int(input("Number of plates: "))
tips_list=[]
plates_list=[]
for i in range (1, plates+1):
    print("For the PLATE ", i)
    #Plates
    plate_i_position=int(input("Plate position: "))
    plate_i = protocol.load_labware("nest_96_wellplate_200ul_flat", plate_i_position)
    plate_i.set_offset(x=1.00, y=2.00, z=0.00)
    plates_list.append(plate_i)
    #Tip racks
    tips_i_position=int(input("Tip rack position: "))
    tips_i = protocol.load_labware("opentrons_96_tiprack_300ul", tips_i_position)
    tips_i.set_offset(x=0.00, y=1.00, z=0.00)
    tips_list.append(tips_i)
    i+=1  
#Pipette
left_pipette = protocol.load_instrument("p300_single_gen2", "left", tip_racks= tips_list)

# METHODS

def wash_tip():
    left_pipette.mix(1, 100, reservoir["A12"])
    left_pipette.blow_out()
_96_wells_list = []
abc= ["B","C","D","E","F","G"]
for i in range(2,12):
    for j in abc:
        well_j = j + str(i)
        _96_wells_list.append(well_j)
def lysis_solution(reservoir_columns_list, plate_wells_list, amount_plates):
    for plate in range(amount_plates):
    #This function aliquots 100 ul of the lysis solution and mixes it with the plate medium
        left_pipette.pick_up_tip()
        for well_plate in plate_wells_list:
            left_pipette.aspirate(100, reservoir[reservoir_columns_list[plate]])
            left_pipette.dispense(105, plates_list[plate][well_plate])
            left_pipette.mix(2, 100, plates_list[plate][well_plate])
           
            wash_tip()
            left_pipette.drop_tip()
            left_pipette.pick_up_tip()
        left_pipette.return_tip()
plate_wells = _96_wells_list
res_columns = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8","A9","A10","A11","A12"]
lysis_solution(res_columns, plate_wells, plates)
protocol.home()
incubate=input("Write OK after the plate was incubated for 30 minutes: ")
if incubate=="OK":
    pass
elif incubate=="ok":
    pass
elif incubate=="Ok":
    pass
else:
    print("Incubate before continuing the protocol")
    stop
confirmation_list= ["Yes","YES","yes"]
negation_list= ["No","NO","no"]
check=input("Did you check the effective lysis of the plate on microscope? (answer YES/NO) : ")
if check in confirmation_list:
    pass
else:
    print("Please, check on microscope the effective lysis of the plate")

#for line in protocol.commands():
 #   print(line)