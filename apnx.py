import socket, ssl, json, struct, sys




def mainWithArguments():
	print "au"


def mainOptionsMenu():
	print "au"
  
if __name__== "__main__":
	print "#### Running apnx pusher ####"
	print "First parameter should be token, path push .pem"
	print sys.argv[0]
  	mainWithArguments()

#originally from: http://stackoverflow.com/questions/1052645/apple-pns-push-notification-services-sample-code

# device token returned when the iPhone application
# registers to receive alerts

deviceToken = '1909913d261daf71453b337df6497ac3a0f2fee16fe5e1a7c5f0b3e93ca317f4'

thePayLoad = {
     'aps': {
          'alert':'OMG! Push\'s works fine!',
          'sound':'k1DiveAlarm.caf',
          'badge':42,
          },
     'test_data': { 'foo': 'bar' },
     }

# Certificate issued by apple and converted to .pem format with openSSL
# Per Apple's Push Notification Guide (end of chapter 3), first export the cert in p12 format
# openssl pkcs12 -in cert.p12 -out cert.pem -nodes 
#   when prompted "Enter Import Password:" hit return
#
theCertfile = 'apns-dev-cert.pem'
# 
theHost = ( 'gateway.sandbox.push.apple.com', 2195 )

# 
data = json.dumps( thePayLoad )

# Clear out spaces in the device token and convert to hex
deviceToken = deviceToken.replace(' ','')




if sys.version_info[0] == 3:
    byteToken = bytes.fromhex( deviceToken ) # Python 3
    text = input("prompt")  # Python 3
else:
    byteToken = deviceToken.decode('hex') # Python 2
    text = raw_input("prompt")  # Python 2

print text
theFormat = '!BH32sH%ds' % len(data)
theNotification = struct.pack( theFormat, 0, 32, byteToken, len(data), data )

# Create our connection using the certfile saved locally
ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = theCertfile )
ssl_sock.connect( theHost )

# Write out our data
ssl_sock.write( theNotification )
print "successfully"

# Close the connection -- apple would prefer that we keep
# a connection open and push data as needed.
ssl_sock.close()
