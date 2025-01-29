from opentrons import protocol_api

metadata = {
    "apiLevel": "2.11",
    "protocolName": "Simple Pipetting Protocol",
    "description": "A simple example of pipetting and printing actions",
    "author": "Franco Agustín Agüero"
}

def run(ctx: protocol_api.ProtocolContext):
    # Cargar labware
    tiprack = ctx.load_labware("opentrons_96_tiprack_300ul", 1)
    plate = ctx.load_labware("nest_96_wellplate_200ul_flat", 2)
    
    # Cargar pipeta
    pipette = ctx.load_instrument("p300_single_gen2", "left", tip_racks=[tiprack])

    # Realizar pipeteo 
    for well in plate.wells():
        pipette.pick_up_tip()
        pipette.aspirate(100, well)
        pipette.dispense(100, well)
        pipette.blow_out()
        pipette.drop_tip()

    # Imprimir todos los comandos generados
    for line in ctx.commands():
        print(line)