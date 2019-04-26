import socket, ssl, json, struct, sys
from datetime import datetime


## Constants never change
fcmUrl = 'https://fcm.googleapis.com/fcm/send'
fcmContentType = 'Content-Type: application/json'

apnsSandBoxHostSSL = ( 'gateway.sandbox.push.apple.com', 2195 )
apnsProductionHostSSL = ( 'gateway.push.apple.com', 2195)

apnsSandBoxHostTLS = ( 'api.development.push.apple.com', 443 )
apnsProductionHostTLS = ( 'api.push.apple.com', 443)

def showAllInfo():
    print '-h to show help'


def mainWithArguments():
	print 'au'


def mainOptionsMenu():
	print 'au'
  
if __name__== "__main__":
	print "#### Running apnx pusher ####"
	print sys.argv[0]
        showAllInfo()
        mainWithArguments()

#originally from: http://stackoverflow.com/questions/1052645/apple-pns-push-notification-services-sample-code

# device token returned when the iPhone application
# registers to receive alerts

deviceToken = '5a72a0d392dd18d09c6bc729e1aec1ed1f62862b1d17d8a2a7a435b81d4d8aa9'

thePayLoad = {
     'aps': {
         'alert':'OMG! Push\'s works fine! with date: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
data = json.dumps( thePayLoad )

# Clear out spaces in the device token and convert to hex
deviceToken = deviceToken.replace(' ','')


if sys.version_info[0] == 3:
    byteToken = bytes.fromhex( deviceToken ) # Python 3
    text = input("Choose and option:")  # Python 3
else:
    byteToken = deviceToken.decode('hex') # Python 2
    text = raw_input("Choose and option:")  # Python 2

theFormat = '!BH32sH%ds' % len(data)
theNotification = struct.pack( theFormat, 0, 32, byteToken, len(data), data )

# Create our connection using the certfile saved locally
ssl_sock = ssl.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), certfile = theCertfile )
ssl_sock.connect( apnsSandBoxHostSSL )

# Write out our data
ssl_sock.write( theNotification )
print "successfully"

# Close the connection -- apple would prefer that we keep
# a connection open and push data as needed.
ssl_sock.close()
