#TESTEAR ANTES DE USAR!!!!!!! FALTA REVISAR!!!!
from opentrons import protocol_api
#import json
metadata = {
    "apiLevel": "2.11",
    "protocolName": "Parasite Lysis",
    "description": "Protocol for lysing parasites in a 96-well plate",
    "author": "Aguero Franco Agustin, Didier Garnham Mercedes"
}
def run(ctx: protocol_api.ProtocolContext):
    # LABWARE INPUTS
    reservoir_position = 1  # Define the deck position for the reservoir
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", reservoir_position) #sino usar ctx.load_labware()
    #reservoir.set_offset(x=0.00, y=0.00, z=0.00)
    # Plates and tipracks
    plates_positions = [2, 3]  # Define deck positions for plates
    tips_positions = [4, 5]    # Define deck positions for tipracks
    plates_list = [protocol.load_labware("nest_96_wellplate_200ul_flat", pos) for pos in plates_positions]
    tips_list = [protocol.load_labware("opentrons_96_tiprack_300ul", pos) for pos in tips_positions]
    # Pipette
    left_pipette = protocol.load_instrument("p300_single_gen2", "left", tip_racks=tips_list)

    protocol.home()
    # PROTOCOL
    def wash_tip():
        left_pipette.mix(1, 100, reservoir["A12"]) #sino probar source= reservoir["A12"]
        left_pipette.blow_out()
    _96_wells_list = []
    abc= ["B","C","D","E","F","G"]
    for i in range(2,12):
        for j in abc:
            well_j = j + str(i)
            _96_wells_list.append(well_j)
    def lysis_solution(reservoir_columns_list, plate_wells_list, amount_plates):
        for plate in range(amount_plates): #sino probar plates_list
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
    #incubate=input("Write OK after the plate was incubated for 30 minutes: ")
    #if incubate=="OK":
    #    pass
    #elif incubate=="ok":
    #    pass
    #elif incubate=="Ok":
    #    pass
    #else:
    #    print("Incubate before continuing the protocol")
    #    stop
    #confirmation_list= ["Yes","YES","yes"]
    #negation_list= ["No","NO","no"]
    #check=input("Did you check the effective lysis of the plate on microscope? (answer YES/NO) : ")
    #if check in confirmation_list:
    #    pass
    #else:
    #    print("Please, check on microscope the effective lysis of the plate")
    #for line in protocol.commands():
    #   print(line)