import Encoder
import Decoder

coded = Encoder.main("yepwhite", "Hi Friends, it's your friendly neighborhood Fire Chief, Pathfinder!")
print(coded)
decoded = Decoder.main("bonk",coded)
print(decoded)