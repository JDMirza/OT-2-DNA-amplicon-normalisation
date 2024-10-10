from opentrons import protocol_api
# metadata
metadata = {'protocolName': 'Variable dilution input','description':'dictionary test for volume' ,'author': 'JM','description': 'Amplicon Dilution',
    'apiLevel': '2.10'}
def run(protocol: protocol_api.ProtocolContext):
    # labware and pipettes
    dil1 = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '8', 'Dilution Pool 1')
    dil2 = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '9', 'Dilution Pool 2')
    pool1 = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '5', 'Pool 1')
    pool2 = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '6', 'Pool 2')
    combdil = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep', '3', 'Combined diluted pools')

    trough = protocol.load_labware('agilent_1_reservoir_290ml', '7', 'trough')
    
    tiprack = protocol.load_labware('opentrons_96_filtertiprack_200ul', '10', '200 tips')
    smalltiprack = protocol.load_labware('opentrons_96_filtertiprack_20ul', '1' , '20 tips')
    wastesmalltiprack = protocol.load_labware('opentrons_96_filtertiprack_20ul', '11', '20 waste')

    left = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack])
    right = protocol.load_instrument('p20_multi_gen2', 'right', tip_racks=[smalltiprack])

    # commands
    # Transfer water from trough to wells without removing tips
    left.pick_up_tip(tiprack['H1'])

    wells = ["A1","B1","C1","D1","E1","F1","G1","H1","A2","B2","C2","D2","E2","F2","G2","H2","A3","B3","C3","D3","E3","F3","G3","H3","A4","B4","C4","D4","E4","F4","G4","H4","A5","B5","C5","D5","E5","F5","G5","H5","A6","B6","C6","D6","E6","F6","G6","H6","A7","B7","C7","D7","E7","F7","G7","H7","A8","B8","C8","D8","E8","F8","G8","H8","A9","B9","C9","D9","E9","F9","G9","H9","A10","B10","C10","D10","E10","F10","G10","H10","A11","B11","C11","D11","E11","F11","G11","H11","A12","B12","C12","D12","E12","F12","G12","H12"]
      
    #Dictionary of volumes generated for dilution to replace with Qubit output from excel sheet 
    volume1 = [10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    volume2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    dict1 = {well:float(volume1[index]) for index, well in enumerate(wells)}

    dict2 = {well:float(volume2[index]) for index, well in enumerate(wells)}
    
    for well, volume1 in dict1.items():
        if volume1 == 0:
            protocol.comment('Transfer volume for ' + well + ' is zero, skipping')
            continue
        left.aspirate(volume1, trough['A1'])
        left.dispense(volume1, dil1[well])

    for well, volume2 in dict2.items():
        if volume2 == 0:
            protocol.comment('Transfer volume for ' + well + ' is zero, skipping')
            continue
        left.aspirate(volume2, trough['A1'])
        left.dispense(volume2, dil2[well])    

    left.drop_tip(tiprack['H1'])

    right.speed.aspirate = 20
    right.speed.dispense = 20
    
    wells = ["A1", "A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12"]
    for well in wells:
        right.pick_up_tip(smalltiprack[well])
        right.aspirate(5, pool1[well])
        right.dispense(5, dil1[well])
        right.mix(2,8)
        right.drop_tip(wastesmalltiprack[well])          
    
    protocol.pause("Change tips at position 1 and 11")

    for well in wells:
        right.pick_up_tip(smalltiprack[well])
        right.aspirate(5, pool2[well])
        right.dispense(5, dil2[well])
        right.mix(2,8)
        right.drop_tip(wastesmalltiprack[well])          
    
    protocol.pause("Change tips at position 1 and 11")
    
    for well in wells:
        right.pick_up_tip(smalltiprack[well])
        right.aspirate(5, dil1[well])
        right.aspirate(5, dil2[well])
        right.dispense(10, combdil[well])
        right.mix(2,8)
        right.drop_tip(wastesmalltiprack[well])  