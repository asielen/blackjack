# X TF TF TF
# Number of decks
# Dealer Hit or stand on 17 (False for stand)
# Double after split? True or False
# Surrender True or False.. always false for now
basic = {
    "1-False-True-False":
       {'7XT': ['hit'], '13SX9': ['hit'], '8,8X4': ['split'], '5X9': ['hit'], '17XQ': ['stand'], '16X3': ['stand'], '7X7': ['hit'], 'A,AX5': ['split'], '4,4XJ': ['hit'], 'A,AXJ': ['split'], '6X4': ['hit'], '17SXA': ['hit'], '17XT': ['stand'], '8X8': ['hit'], '3,3XK': ['hit'], '6X6': ['hit'], '19XA': ['stand'], '18X9': ['stand'], '13XA': ['hit'], '14X3': ['stand'], '7X3': ['hit'], '11XJ': ['doub', 'hit'], '8X2': ['hit'], '15X6': ['stand'], '6,6X8': ['hit'], '17SXK': ['hit'], '17SXJ': ['hit'], '17X5': ['stand'], '4,4XA': ['hit'], 'A,AX7': ['split'], '7,7X3': ['split'], '6,6X5': ['split'], '13SXT': ['hit'], '2,2X9': ['hit'], '5X6': ['hit'], '11X3': ['doub', 'hit'], '18SX4': ['doub', 'split'], '9XQ': ['hit'], '6,6XA': ['hit'], '21X4': ['stand'], '20SXK': ['stand'], '8,8XQ': ['split'], '20XA': ['stand'], '6X9': ['hit'], '19SX2': ['stand'], '15X2': ['stand'], '17XK': ['stand'], '3,3X4': ['split'], '14XK': ['hit'], '6,6XT': ['hit'], '19SX5': ['stand'], '10X5': ['doub', 'hit'], '7X8': ['hit'], '10X3': ['doub', 'hit'], '5X8': ['hit'], '7X4': ['hit'], '19X9': ['stand'], '6,6X7': ['hit'], '2,2X8': ['hit'], '5XJ': ['hit'], '8,8X6': ['split'], '21SXJ': ['stand'], '16SXQ': ['hit'], '20SXJ': ['stand'], '18SXA': ['hit'], '2,2XT': ['hit'], '8XK': ['hit'], '4,4XQ': ['hit'], '13X7': ['hit'], '17XJ': ['stand'], '16SX3': ['hit'], '15SX6': ['doub', 'hit'], '7,7X4': ['split'], '10X6': ['doub', 'hit'], '12X4': ['stand'], '18XQ': ['stand'], '18SXJ': ['hit'], '14X4': ['stand'], '14X5': ['stand'], '21XT': ['stand'], '20SX8': ['stand'], '13SX7': ['hit'], '19X6': ['stand'], '20XQ': ['stand'], '19X8': ['stand'], '17X2': ['stand'], '18X8': ['stand'], '15X5': ['stand'], '15XT': ['hit'], '10X9': ['doub', 'hit'], '13X3': ['stand'], '9X6': ['doub', 'hit'], '9,9X9': ['split'], '15SXK': ['hit'], '6XT': ['hit'], '13X6': ['stand'], '4,4X8': ['hit'], '6,6XK': ['hit'], '13SX6': ['doub', 'hit'], 'A,AX8': ['split'], 'T,TX7': ['stand'], '6,6X9': ['hit'], '19SX7': ['stand'], '2,2X2': ['hit'], '16XT': ['hit'], '5X2': ['hit'], '14XQ': ['hit'], '9X5': ['doub', 'hit'], '14SX9': ['hit'], '7,7XJ': ['hit'], '10XT': ['hit'], '17X6': ['stand'], '9,9X4': ['split'], '7XQ': ['hit'], '15SXJ': ['hit'], '20SXA': ['stand'], '12X3': ['hit'], '2,2XA': ['hit'], '10X8': ['doub', 'hit'], '3,3X9': ['hit'], '14SX8': ['hit'], '5,5X2': ['doub', 'hit'], '2,2X3': ['hit'], '15SX8': ['hit'], '13X9': ['hit'], '9,9X3': ['split'], '16SXT': ['hit'], '9,9XA': ['stand'], 'A,AXQ': ['split'], '21SX3': ['stand'], '19SX8': ['stand'], '15SXT': ['hit'], '19SX3': ['stand'], '8XA': ['hit'], '8,8X7': ['split'], '15XQ': ['hit'], '2,2XK': ['hit'], '21X3': ['stand'], '16SX5': ['doub', 'hit'], '21SX6': ['stand'], '17X3': ['stand'], 'A,AXA': ['split'], '9,9XQ': ['stand'], '6XA': ['hit'], '15SX2': ['hit'], '2,2X7': ['split'], '19X2': ['stand'], '8,8X3': ['split'], '16X8': ['hit'], '21SXQ': ['stand'], '13SXQ': ['hit'], '18SXT': ['hit'], '12X5': ['stand'], '6XJ': ['hit'], '16SX2': ['hit'], '16X9': ['hit'], '5X7': ['hit'], '11XT': ['doub', 'hit'], '19XK': ['stand'], '9,9X6': ['split'], '11XK': ['doub', 'hit'], '8X7': ['hit'], '8,8XT': ['split'], '12XT': ['hit'], '9X8': ['hit'], '20X3': ['stand'], '2,2XJ': ['hit'], '13SX5': ['doub', 'hit'], 'T,TXQ': ['stand'], '2,2X4': ['split'], '8,8X5': ['split'], '5X4': ['hit'], '17X8': ['stand'], '13SX3': ['hit'], 'T,TXA': ['stand'], '15SX5': ['doub', 'hit'], '21SX7': ['stand'], '8XQ': ['hit'], '14XA': ['hit'], '19XQ': ['stand'], '17X4': ['stand'], '7,7X7': ['split'], '17SX3': ['doub', 'hit'], '20SX3': ['stand'], 'T,TXT': ['stand'], '3,3X2': ['hit'], '11XA': ['hit'], '9XT': ['hit'], '5X3': ['hit'], '14SX3': ['hit'], '3,3X5': ['split'], '19SXT': ['stand'], '4,4X3': ['hit'], '20XJ': ['stand'], '15SX4': ['doub', 'hit'], '19X5': ['stand'], '14X7': ['hit'], '16SX6': ['doub', 'hit'], '6XQ': ['hit'], '8,8XJ': ['split'], '21X9': ['stand'], '20X2': ['stand'], '16X6': ['stand'], '9,9XK': ['stand'], '16SXK': ['hit'], '15SX9': ['hit'], '4,4X4': ['hit'], '11X9': ['doub', 'hit'], '14SX5': ['doub', 'hit'], '5,5X9': ['doub', 'hit'], '21SXK': ['stand'], '15SX7': ['hit'], '16XJ': ['hit'], '20XT': ['stand'], 'A,AXK': ['split'], '18SX5': ['doub', 'split'], '14SXK': ['hit'], '6X2': ['hit'], '18SX7': ['stand'], '14SXT': ['hit'], '20SXT': ['stand'], '21X8': ['stand'], '4,4X5': ['hit'], '7X5': ['hit'], '17SX9': ['hit'], '13X2': ['stand'], '3,3X7': ['split'], '3,3X3': ['hit'], '19SXJ': ['stand'], '19X3': ['stand'], '8X9': ['hit'], '11X6': ['doub', 'hit'], '8X4': ['hit'], 'A,AX2': ['split'], '4,4XK': ['hit'], '9X9': ['hit'], 'T,TX9': ['stand'], '12XQ': ['hit'], '7X6': ['hit'], '20SX5': ['stand'], '21SXA': ['stand'], '13XJ': ['hit'], '14X8': ['hit'], 'A,AX3': ['split'], '10XQ': ['hit'], '16SX9': ['hit'], 'T,TX8': ['stand'], '5,5XA': ['hit'], '18SX9': ['hit'], '21X2': ['stand'], '7XK': ['hit'], '5,5X8': ['doub', 'hit'], '7XA': ['hit'], '6XK': ['hit'], '8,8X9': ['split'], '21X6': ['stand'], '18XA': ['stand'], '9X2': ['hit'], '7,7X8': ['hit'], '13SXK': ['hit'], '5,5XJ': ['hit'], '5,5X3': ['doub', 'hit'], '13XQ': ['hit'], '20X5': ['stand'], '5,5XK': ['hit'], '6,6X4': ['split'], '18X2': ['stand'], '17SX4': ['doub', 'hit'], '13X5': ['stand'], '20SX2': ['stand'], '8,8XK': ['split'], '6X7': ['hit'], '7,7XT': ['hit'], '8X3': ['hit'], '5XA': ['hit'], '9,9X2': ['split'], '5XK': ['hit'], '9,9X5': ['split'], '13XK': ['hit'], '18X4': ['stand'], '10X4': ['doub', 'hit'], '10X7': ['doub', 'hit'], '16X4': ['stand'], '7,7XA': ['hit'], 'T,TXK': ['stand'], '17SXQ': ['hit'], '16XA': ['hit'], '18SX2': ['stand'], '17SX7': ['hit'], '14X9': ['hit'], '20X7': ['stand'], '15SXQ': ['hit'], '7,7X5': ['split'], '18SXQ': ['hit'], '18SX8': ['stand'], '15XK': ['hit'], '15X4': ['stand'], '18XJ': ['stand'], '21X5': ['stand'], '10X2': ['doub', 'hit'], '3,3XJ': ['hit'], '18X3': ['stand'], '16SX7': ['hit'], '6X5': ['hit'], '14X6': ['stand'], '7,7X2': ['split'], '14XJ': ['hit'], '17SX8': ['hit'], '21SX4': ['stand'], '8XJ': ['hit'], '18XT': ['stand'], '8X5': ['hit'], '16SXA': ['hit'], '20XK': ['stand'], 'T,TX5': ['stand'], '10XJ': ['hit'], '19X7': ['stand'], '16SXJ': ['hit'], '18X5': ['stand'], '19SX9': ['stand'], '8XT': ['hit'], '2,2X5': ['split'], '5,5X5': ['doub', 'hit'], '16XQ': ['hit'], '14SX7': ['hit'], '19SX4': ['stand'], '11XQ': ['doub', 'hit'], '9,9XT': ['stand'], '16XK': ['hit'], '12X2': ['hit'], 'T,TX3': ['stand'], '12X6': ['stand'], '21X7': ['stand'], '20X4': ['stand'], '19X4': ['stand'], '18SXK': ['hit'], '21SX8': ['stand'], '9XA': ['hit'], 'A,AX9': ['split'], '15X8': ['hit'], '7,7X9': ['hit'], '18X6': ['stand'], '12X9': ['hit'], '9,9X8': ['split'], '15SX3': ['hit'], '9X7': ['hit'], '15XA': ['hit'], '11X7': ['doub', 'hit'], '6,6XQ': ['hit'], '12X7': ['hit'], 'T,TX4': ['stand'], '21XK': ['stand'], '6,6X3': ['split'], 'A,AX4': ['split'], '16X5': ['stand'], '11X4': ['doub', 'hit'], '12X8': ['hit'], '4,4X9': ['hit'], '5,5XT': ['hit'], '5,5X4': ['doub', 'hit'], '21SXT': ['stand'], '10XA': ['hit'], '15XJ': ['hit'], '8X6': ['hit'], '9,9XJ': ['stand'], '20SX9': ['stand'], '16X7': ['hit'], '14SX6': ['doub', 'hit'], '21XA': ['stand'], '14SXA': ['hit'], '17SX2': ['hit'], '5,5X6': ['doub', 'hit'], '21SX2': ['stand'], '6X8': ['hit'], '7X9': ['hit'], '4,4X7': ['hit'], '9,9X7': ['stand'], '10XK': ['hit'], '18X7': ['stand'], '5X5': ['hit'], '4,4X2': ['hit'], '2,2X6': ['split'], '8,8X2': ['split'], '3,3X6': ['split'], '16SX8': ['hit'], '17SX6': ['doub', 'hit'], '9XJ': ['hit'], '19SXQ': ['stand'], '12XK': ['hit'], '4,4XT': ['hit'], '21XJ': ['stand'], '6X3': ['hit'], '4,4X6': ['hit'], '15X7': ['hit'], '9X3': ['doub', 'hit'], 'A,AX6': ['split'], '20SXQ': ['stand'], 'A,AXT': ['split'], '19SXA': ['stand'], '13X4': ['stand'], '21XQ': ['stand'], '2,2XQ': ['hit'], '15X9': ['hit'], '20X8': ['stand'], '12XA': ['hit'], '14SX2': ['hit'], '13XT': ['hit'], 'T,TX6': ['stand'], '6,6X2': ['hit'], '14SX4': ['hit'], '3,3XQ': ['hit'], '5,5X7': ['doub', 'hit'], '21SX9': ['stand'], '15X3': ['stand'], '7X2': ['hit'], '16X2': ['stand'], '11X8': ['doub', 'hit'], '7,7XK': ['hit'], '19XJ': ['stand'], '14X2': ['stand'], '14SXJ': ['hit'], '13SX2': ['hit'], '9XK': ['hit'], '9X4': ['doub', 'hit'], '14SXQ': ['hit'], '5,5XQ': ['hit'], '3,3XA': ['hit'], '18SX6': ['doub', 'split'], '11X5': ['doub', 'hit'], '3,3X8': ['hit'], '13SXJ': ['hit'], '17XA': ['stand'], '13SX8': ['hit'], '5XQ': ['hit'], '7,7X6': ['split'], '16SX4': ['doub', 'hit'], '5XT': ['hit'], '15SXA': ['hit'], '17X7': ['stand'], '8,8XA': ['split'], 'T,TXJ': ['stand'], '7,7XQ': ['hit'], '21SX5': ['stand'], '13SX4': ['hit'], '6,6X6': ['split'], '20X6': ['stand'], '8,8X8': ['split'], 'T,TX2': ['stand'], '17SX5': ['doub', 'hit'], '20SX6': ['stand'], '20SX7': ['stand'], '6,6XJ': ['hit'], '7XJ': ['hit'], '17X9': ['stand'], '13SXA': ['hit'], '20SX4': ['stand'], '19XT': ['stand'], '18SX3': ['doub', 'split'], '13X8': ['hit'], '12XJ': ['hit'], '19SX6': ['stand'], '19SXK': ['stand'], '11X2': ['doub', 'hit'], '14XT': ['hit'], '18XK': ['stand'], '17SXT': ['hit'], '3,3XT': ['hit'], '20X9': ['stand']},
    "1-True-True-False":
       None,
    "1-True-False-False":
       None,
    "1-False-False-False":
       None,
    "2-False-True-False":
       None,
    "2-True-True-False":
       None,
    "2-True-False-False":
        None,
    "2-False-False-False":
        None,
    "4-False-True-False":
       None,
    "4-True-True-False":
        None,
    "4-True-False-False":
        None,
    "4-False-False-False":
       None
}
