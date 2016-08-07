import sys
import wave

for arg in sys.argv[1:]:
    with open(arg, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(arg+'.wav', 'wb') as wavfile:
        wavfile.setparams((2, 2, 44100, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)

#
# # pcm_data = audiotools.open("file.wav").to_pcm()
# outfile = open("output.pcm","wb")
# transfer_framelist_data(pcm_data,outfile)
# pcm_data.close()
# outfile.close()