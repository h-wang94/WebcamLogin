if [ -d ~/.voiceid/gmm_db ]; then
	echo "Clearing existing GMM database!"
	rm -r ~/.voiceid/gmm_db
fi

if [ -z `which vid` ]; then
	echo "Oh! VoiceID has not been installed! Exiting!"
	exit 1
fi

# Build some voice fingerprint databases
vid -s Tommy -g alice1{,1,2,3}.wav
vid -s Heath -g heath123.wav 
vid -s Harrison -g harrison1.wav

echo "OK!"
