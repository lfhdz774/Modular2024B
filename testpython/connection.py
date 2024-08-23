import paramiko
k = paramiko.RSAKey.from_private_key_file("./key11.pem")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print ("connecting")
c.connect( hostname = "ec2-3-145-177-3.us-east-2.compute.amazonaws.com", username = "ubuntu", pkey = k )
print ("connected")
commands = [ "sudo useradd  test123"]
for command in commands:
    print ("Executing {}".format( command ))
    stdin , stdout, stderr = c.exec_command(command)
    print (stdout.read())
    print( "Errors")
    print (stderr.read())
c.close()