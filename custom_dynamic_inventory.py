# Use python script to build your custom inventory from dynamic inventory(from  ec2.py,extract EC2s based on taggings) you get from ansible cli
#!/bin/python   #python is alraedy installed in servers,thats why we use python interpreter.check which python, which bash
import sys  #import sys module to exit, it lets us access system-specific parameters ans functions
import json # we get facts(list of IPs,ASG..etc) in json format,we need to print in json format because ansible understands json.

try:
   import boto3 #in case of dependency issue when boto3 installed we need to catch exception
except ImportError:  
   print("Please install boto3 using pip install boto3 and try again")
   sys.exit(1)    # 0 is usually success,1 error,  2 another error
except Exception as e:
   print(e)
   sys.exit(2)
# we make fuction below "get_hosts()" to reuse it.
def get_hosts(all_ec2s,f_value):   # it has 2 parameters 1.all_ec2s 2.filter  values(filters tags)
   custom_filter={"Name":"tag:Environment", "Values":[f_value]}
   hosts=[]  #loop through all instances which has (web or db) tags and add private IPs of these instances to this hosts list
   for instance in all_ec2s.instances.filter(Filters=[custom_filter]):
    hosts.append(instance.private_ip_address)
   return hosts

# main function which will poll all ec2 resources from us-east-1
def main():
   all_ec2s=boto3.resource("ec2","us-east-1") # (no session here ? access key,secret key,session token,enable users activa..etc we all get these from IAM role that
   db_group=get_hosts(all_ec2s,"db")  #func gets all ec2 having db tag from us-east-1.       #  we previosly attached.we assume IAM role automatically  assigns sts in the backend.
   web_group=get_hosts(all_ec2s,"web") #func gets all ec2 having web tag from us-east-1.
#    print(web_group)
   all_groups= { 'db': db_group,
                  'web': web_group
               }
   print(json.dumps(all_groups)) #json.dumps() function converts a python object into a json string.

if __name__=="__main__":  #import script in a different python script ??not clr
   main()