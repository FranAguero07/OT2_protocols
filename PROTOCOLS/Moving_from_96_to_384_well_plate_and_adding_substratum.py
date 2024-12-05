# # Summary

# This protocol first moves solutions from a 96-well plate to a 384-well plate, mixing 5 times in each step. 
# For this it takes 90 uL of B2 (96 wells) and moves it to A1 (384 wells), then takes 90 uL of C2 (96 wells) 
# and moves it to B1 (384 wells), then from D2 (96 wells) to C1 (384 wells); and so on until moving the entire
#  96 wells plate. The order of passage on the 96 wells plate will be from B2 to G2, B3 to G3,...,B12 to G12
# (NOT considering row A or H, nor column 1 of the 96 wells plate).
# The protocol also allows you to put substrate in the 384 plate. It will start by putting 10 uL in the 
# position of all the controls, and then it will continue putting 10 uL in the other wells, going in the order 
# A1, B1, C1 and so on. The substrate will always be taken from the eppendorf located in position A1.
# So it is necessary to manually place the eppendorf with the substrate in position A1 of the tuberack. It is 
# supposed to use at least 600 uL of substrate (10uL * 60 wells)



# # Labware needed for running this protocol:

# For moving liquids from 96 well plates to 384 well plate
# - 384 well plate: corning_384_wellplate_112ul_flat
# - 96 well plate: nest_96_wellplate_200ul_flat
# - tipracks: opentrons_96_tiprack_300ul (this protocol requires at least a tiprack for each 96 well plate used)
# - pipette: p300_single_gen2 on left
# For moving substratum to 384 well plate
# - reservoir: opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap
# - tipracks: opentrons_96_tiprack_20ul 
# - pipette: p20_single_gen2 on right (depending on the amount of wells to fill)

# This protocol uses different coordinates for each labware. If you want to use the default coordinates, delete de line "labware.set_offset()" for each one.



##Protocol

#import opentrons.simulate
#protocol = opentrons.simulate.get_protocol_api('2.11')
import opentrons.execute
protocol = opentrons.execute.get_protocol_api('2.11')
metadata = {
    "apiLevel": "2.11",
    "protocolName": "Moving liquids and substrats",
    "description": """Protocol for moving liquids and substratums to a 384 well plate""",
    "author": "Aguero Franco Agustin, Didier Garnham Mercedes"
    }
protocol.home()

_384_plate_position=int(input("384 well plate position:"))
plate_384 = protocol.load_labware("corning_384_wellplate_112ul_flat", _384_plate_position)
plate_384.set_offset(x=0.50, y=1.50, z=3.00)
print("Is the 384 well plate used? (answer YES or NO)")
answer=  input()
confirmation_list= ["Yes","YES","yes"]
negation_list= ["No","NO","no"]
if answer in confirmation_list:
    first_384_column= int(input("From the 384 well plate, from which column do you want to star?: "))
    _384_wells_list = []
    abc= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"]
    for i in range(first_384_column,25):
        for j in abc:
            well_j = j + str(i)
            _384_wells_list.append(well_j)
    
elif answer in negation_list:
    _384_wells_list = []
    abc= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"]
    for i in range(1,25):
        for j in abc:
            well_j = j + str(i)
            _384_wells_list.append(well_j)
#Plates and tip racks
plates=int(input("Amount of plates: "))
tips_list=[]
plates_list=[]
for i in range (1, plates+1):
    print("For the PLATE ", i)
    #PLATES
    plate_i_position=int(input("Plate position: "))
    plate_i = protocol.load_labware("nest_96_wellplate_200ul_flat", plate_i_position)
    plate_i.set_offset(x=1.00, y=2.00, z=0.00)
    plates_list.append(plate_i)
    #TIP RACKS
    tips_i_position=int(input("p300 Tip rack position: "))
    tips_i = protocol.load_labware("opentrons_96_tiprack_300ul", tips_i_position)
    tips_i.set_offset(x=0.00, y=1.00, z=0.00)
    tips_list.append(tips_i)
    i+=1
#Reservoir
reservoir_position=int(input("Reservoir position: "))
reservoir = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", reservoir_position)
reservoir.set_offset(x=0.00, y=1.00, z=0.00)
#Pipette
p300_pipette = protocol.load_instrument("p300_single_gen2", "left", tip_racks= tips_list)

#MOVING FROM 96 TO 384 WELL PLATE 
_384_wells= _384_wells_list
i=0
k=9
for plate in plates_list: 
    while k<96:
        for j in range(k, k+6):
            p300_pipette.pick_up_tip()
            p300_pipette.mix(5, 100, plate.wells()[k])
            p300_pipette.aspirate(90, plate.wells()[k])
            p300_pipette.dispense(90, plate_384[_384_wells[i]])
            p300_pipette.drop_tip()
            i+=1
            k+=1
        k+=2

# FOR ADDING SUBSTRATUM --
#Reservoir
reservoir_position=int(input("Reservoir position: "))
reservoir = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", reservoir_position)
reservoir.set_offset(x=0.00, y=1.00, z=0.00)
#Pipette and tips
tips_p20=int(input("Amount of tip racks for P20: "))
tips_p20_list=[]
for i in range (1, tips_p20+1):
    print("For the P20 tip rack n° ", i)
    tips_i_position=int(input("Position: "))
    tips_i = protocol.load_labware("opentrons_96_tiprack_20ul", tips_i_position)
    tips_i.set_offset(x=0.00, y=1.00, z=0.00)
    tips_p20_list.append(tips_i)
    i+=1
p20_single_pipette = protocol.load_instrument("p20_single_gen2","right", tip_racks=tips_p20_list)
#Passage from eppendorf with substratum (placed in A1) to 384 well plate
def substratum_to_384 (k,j):
    for i in range(k,j):
            p20_single_pipette.aspirate(15, reservoir["A1"])
            p20_single_pipette.dispense(10,plate_384[_384_wells_list[i]])
            p20_single_pipette.dispense(5, reservoir["A1"])
            i+=1
#For controls
a=1
m=54
n=60
p20_single_pipette.pick_up_tip()
while a<= plates:
    x= substratum_to_384(m,n)
    m+=60
    n+=60
    a+=1
p20_single_pipette.drop_tip()
#For the other wells
a=1
m=0
n=54
p20_single_pipette.pick_up_tip()
while a<= plates:
    x= substratum_to_384(m,n)
    m+=60
    n+=60
    a+=1
p20_single_pipette.drop_tip()

incubate_at_37=input("Write OK after the plate was incubated at 37°C for 15 minutes: ")
if incubate_at_37=="OK":
    pass
elif incubate_at_37=="ok":
    pass
elif incubate_at_37=="Ok":
    pass
else:
    print("Incubate before continuing the protocol")
    stop
protocol.home()

#for line in protocol.commands():
#    print(line)