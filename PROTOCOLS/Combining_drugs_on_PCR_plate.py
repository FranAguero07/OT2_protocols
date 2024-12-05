# # SUMMARY
# This protocol requires manually placing the compounds in the first well of the first row (A2) and first 
# column (B1) of the PCR plate (at least 80uL). It also requires preparing an eppendorf with DMSO in well 
# A1 of the tuberack (1 mL).
# When running the program, it will first start by putting DMSO in the first row and column, except for the
# wells where we put the compounds manually (it will move 50 uL from eppendorf A1 of the tuberack to well
# A3 of the PCR plate, then from eppendorf A1 to A4 from the PCR plate and so on; then it will fill the
# first column aspirating again from the eppendorf of A1 and moving it to C1, D1, and so on until it reaches
# G1). Then it will make serial dilutions of the compounds in the first row (from A2 to A9) and first column
# (from B1 to F1), moving 50 uL. Finally it will make the combinations between the rows and columns; will
# first distribute the content of column 1 along the rows (i.e. from B1 to B10, from B1 to B9,...from B1 to
# B2; and then from C1 to c10, C1 to C9,...) , and then it will distribute the content of the first row along
# each column (from A2 ->G2, A2 ->F2,..., A2 -> B2; A3 ->G3, A3 -> F3 and so on)

# # LABWARE NEEDED for running this protocol
# - PCR full skirt plate: nest_96_wellplate_100ul_pcr_full_skirt
# - Reservoir: opentrons_24_tuberack_nest_1.5ml_snapcap
# - Tipracks p300: opentrons_96_tiprack_300ul
# - Tipracks p20: opentrons_96_tiprack_20ul
# - P300 pipette: p300_single_gen2 on left
# - P20 pipette: p20_single_gen2 on right

# This protocol uses different coordinates for each labware. If you want to use the default coordinates, delete the line "labware.set_offset()" for each one.



#import opentrons.simulate
#protocol = opentrons.simulate.get_protocol_api('2.11')
import opentrons.execute
protocol = opentrons.execute.get_protocol_api('2.11')
metadata = {
    "apiLevel": "2.11",
    "protocolName": "Combining compounds",
    "description": """Protocol for combining different compounds on a PCR plate""",
    "author": "Aguero Franco Agustin, Didier Garnham Mercedes"
    }
protocol.home()


# LABWARE INPUTS

# Plates and tips
#          (PCR PLATE)
pcr_plate_position=int(input("PCR plate position:"))
plate_pcr = protocol.load_labware("nest_96_wellplate_100ul_pcr_full_skirt", pcr_plate_position)
plate_pcr.set_offset(x=0.00, y=2.00, z=0.00)
#          (RESERVOIR)
reservoir_position=int(input("Reservoir position:"))
reservoir = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", reservoir_position)
reservoir.set_offset(x=0.00, y=2.00, z=2.00)
#          (TIP RACKS) 
p300_tips=int(input("Amount of tipracks for P300: "))
p300_tips_list=[]
for i in range (1, p300_tips+1):
    print("For the P300 tiprack n° ", i)
    position_tips_i=int(input("Position: "))
    tips_i = protocol.load_labware("opentrons_96_tiprack_300ul", position_tips_i)
    tips_i.set_offset(x=0.00, y=1.50, z=0.00)
    p300_tips_list.append(tips_i)
    i+=1
p20_tips=int(input("Amount of tipracks for P20: "))
p20_tips_list=[]
for j in range (1, p20_tips+1):
    print("For the P20 tiprack n° ", j)
    position_tips_j=int(input("Position: "))
    tips_j = protocol.load_labware("opentrons_96_tiprack_20ul", position_tips_j)
    tips_j.set_offset(x=0.00, y=1.50, z=0.00)
    p20_tips_list.append(tips_j)
    j+=1
#Pipettes 
p300_pipette = protocol.load_instrument("p300_single_gen2", "left", tip_racks= p300_tips_list)
p20_pipette = protocol.load_instrument("p20_single_gen2", "right", tip_racks= p20_tips_list)



# PROTOCOLS

#Add DMSO in first row
p300_pipette.pick_up_tip()
for k in range (2,10):
    p300_pipette.aspirate(50, reservoir["A1"])
    p300_pipette.touch_tip(v_offset=-3)
    p300_pipette.dispense(50, plate_pcr.rows()[0][k], rate= 0.5)
    p300_pipette.blow_out(plate_pcr.rows()[0][k])
    p300_pipette.touch_tip(plate_pcr.rows()[0][k])
#p300_pipette.drop_tip()

#Add DMSO in first column
#p300_pipette.pick_up_tip()
for j in range (2,7):
    p300_pipette.aspirate(50, reservoir["A1"])
    p300_pipette.touch_tip(v_offset=-3)
    p300_pipette.dispense(50, plate_pcr.wells()[j], rate= 0.5)
    p300_pipette.blow_out(plate_pcr.wells()[j])
    p300_pipette.touch_tip(plate_pcr.wells()[j])
#p300_pipette.drop_tip()

#Add 10 uL DMSO in column 11
#p300_pipette.pick_up_tip()
for j in range (80,87):
    p300_pipette.aspirate(10, reservoir["A1"])
    p300_pipette.touch_tip(v_offset=-3)
    p300_pipette.dispense(10, plate_pcr.wells()[j], rate= 0.5)
    p300_pipette.blow_out(plate_pcr.wells()[j])
    p300_pipette.touch_tip(plate_pcr.wells()[j])
p300_pipette.drop_tip()

#Drug dilution on first column, B1 to F1 (G1 has no compound)
p300_pipette.pick_up_tip()
for i in range (1, 5):
    p300_pipette.aspirate(25, plate_pcr.columns()[0][i])
    p300_pipette.dispense(25,  plate_pcr.columns()[0][i+1], rate= 0.5)
    p300_pipette.mix(10, 60)
    p300_pipette.blow_out()
    p300_pipette.touch_tip()
p300_pipette.aspirate(25,plate_pcr.columns()[0][5])
p300_pipette.dispense(25,plate_pcr.columns()[0][7], rate= 0.5)
p300_pipette.blow_out()
p300_pipette.touch_tip()
p300_pipette.drop_tip()

#Drug dilution on first row, A2 to A9 (A11 has no compound)
p300_pipette.pick_up_tip()
for i in range (1, 9):
    p300_pipette.aspirate(25, plate_pcr.columns()[i][0])
    p300_pipette.dispense(25,  plate_pcr.columns()[i+1][0], rate= 0.5)
    p300_pipette.mix(10, 60)
    p300_pipette.blow_out()
    p300_pipette.touch_tip()
p300_pipette.aspirate(25,plate_pcr.columns()[9][0])
p300_pipette.dispense(25,plate_pcr.columns()[11][0], rate= 0.5)
p300_pipette.blow_out()
p300_pipette.touch_tip()
p300_pipette.drop_tip()

# COMBINATIONS
# Put 5 uL in each column from right to left (takes from column B1 and distribute in columns B2 to B10)
for k in range(1,7):
    p20_pipette.pick_up_tip()
    for i in range (1,10):
        p20_pipette.aspirate(5, plate_pcr.columns()[0][k])
        p20_pipette.dispense(5, plate_pcr.columns()[10-i][k], rate= 0.5)
        p20_pipette.blow_out(plate_pcr.columns()[10-i][k])
        p20_pipette.touch_tip(plate_pcr.columns()[10-i][k], v_offset=-2)
    p20_pipette.drop_tip()

# Dilutions from down to top (takes from A2 and distribute in rows A2 to F2)
for k in range(1,10):
    p20_pipette.pick_up_tip()
    for i in range (1,7):
        p20_pipette.aspirate(5, plate_pcr.columns()[k][0])
        p20_pipette.dispense(5, plate_pcr.columns()[k][7-i], rate= 0.5)
        p20_pipette.mix(5, 10)
        p20_pipette.dispense(20, plate_pcr.columns()[k][7-i], rate= 0.5)
        p20_pipette.blow_out(plate_pcr.columns()[k][7-i])
        p20_pipette.touch_tip(plate_pcr.columns()[k][7-i], v_offset=-2)
    p20_pipette.drop_tip()

protocol.home()

#for line in protocol.commands():
#    print(line)