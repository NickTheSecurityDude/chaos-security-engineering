# Chaos Security Engineering Demo

Part of practicing "assume breach" security is by implementing Chaos Engineering.  

In the event your organization suffers a breach its important to be prepared to for it and have the controls in place to mitigate it.

Not only should you have controls but you should regularly test this controls.  A good way to automate this is by using Chaos Security Engineering.

Lets take a look at the following scenario, an organization has a control which states the AWS Managed Policy: AdministratorAccess shall not be used.

When you launch the CloudFormation stack included in this repo, it will respond in two cases:
1. A new role created with the AdministratorAccess policy
1. The AdministratorAccess policy attached to an existing role

To verify this create a role and attach the AdministratorAccess policy.  You will see something like this:
![](https://i.postimg.cc/h4HDTz1t/admin-policy-attached.jpg)

Wait a few seconds, then refresh, you will see the policy was automatically removed.  Now, try attaching it to the the role (case #2), again its automatically removed.
![](https://i.postimg.cc/Bt9J0knK/admin-policy-removed.jpg)

Organizaitions often have hundreds of controls so manually testing them all on a regular basis would not be practical.  This is where Chaos Security Engineering (CSE) comes in.  You can create different "experiments" to test or simillate breaches and security violations and see how your system responds.

In the experiments folder of this repo you will see a script called "chaos-gator.py".  This script performs the following CSE experiment:
1. Looks for a role which doesn't have the AdministratorAccess policy attached
1. Try to attach the role, if it can't it will keep trying other roles
1. If it can attach the policy, it then checks to see if the policy was automatically removed

Here is a sample run:
![](https://i.postimg.cc/FHxkTgTZ/auto-remediation.jpg)

What other experiements can you think of?
