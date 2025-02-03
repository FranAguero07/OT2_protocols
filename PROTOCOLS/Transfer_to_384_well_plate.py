from opentrons import protocol_api
metadata = {
    "apiLevel": "2.11",
    "protocolName": "Transfer from 96 to 384 well plate",
    "description": """Protocol for moving liquids and substratums to a 384 well plate""",
    "author": "Salas Sarduy Emir, Didier Garnham Mercedes, Aguero Franco Agustin"
    }

def run(ctx: protocol_api.ProtocolContext):
    ctx.home()
    plates=1                     #Write the amount of plates you want to transfer
    first_384_column= 1          #Write the 384 well plate column from where you want to start using 
    _384_wells_list = []
    abc= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P"]
    for i in range(first_384_column,25):
        for j in abc:
            well_j = j + str(i)
            _384_wells_list.append(well_j)

    tips_list=[]
    tips_p20_list=[]
    plates_list=[]
    if plates==1:
        plate_384 = ctx.load_labware("corning_384_wellplate_112ul_flat", 1)
        plate_384.set_offset(x=0.50, y=1.50, z=3.00)
        
        #PLATES
        plate_1 = ctx.load_labware("nest_96_wellplate_200ul_flat", 2)
        plate_1.set_offset(x=1.00, y=2.00, z=0.00)
        plates_list.append(plate_1)
        #TIP RACKS
        tips_1 = ctx.load_labware("opentrons_96_tiprack_300ul", 3)
        tips_1.set_offset(x=0.00, y=1.00, z=0.00)
        tips_list.append(tips_1)
        #Reservoir
        reservoir = ctx.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", 4)
        reservoir.set_offset(x=0.00, y=1.00, z=0.00)
        #Pipette
        p300_pipette = ctx.load_instrument("p300_single_gen2", "left", tip_racks= tips_list)

        # LABWARE NEEDED for adding substratum
        #Pipette and tips
        tips_p20= ctx.load_labware("opentrons_96_tiprack_20ul", 5)
        tips_p20.set_offset(x=0.00, y=1.00, z=0.00)
        tips_p20_list.append(tips_p20)
        p20_single_pipette = ctx.load_instrument("p20_single_gen2","right", tip_racks=tips_p20_list)

    # PROTOCOL for moving solution from 96 to 384 well plate 
    _384_wells= _384_wells_list
    i=0
    k=9
    for plate in plates_list: 
        while k<86:
            for j in range(k, k+6):
                p300_pipette.pick_up_tip()
                p300_pipette.mix(5, 100, plate.wells()[k])
                p300_pipette.aspirate(90, plate.wells()[k])
                p300_pipette.dispense(90, plate_384[_384_wells[i]])
                p300_pipette.drop_tip()
                i+=1
                k+=1
            k+=2

    # PROTOCOL for adding substratum
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

    ctx.home()

    for line in ctx.commands():
        print(line)