# CTC - Deploy and manage AWS Control Tower Controls (sometimes called guardrails) using CDK and infrastructure as code



- [Goal](#goal)
- [Overview](#overview)
- [Setup](#setup)
  - [Requirements](#requirements)
  - [Controls Configuration File](#controls-configuration-file)
  - [Control Behavior And Guidance](#control-behavior-and-guidance)
- [Deployment](#deployment)
- [Useful Commands](#useful-commands)



## Goal

This pattern describes how to use AWS Control Tower Controls, AWS Cloud Development Kit (CDK) and infrastructure as code (IaC) to implement and administer preventive, detective and proactive security on the Amazon Web Services (AWS) Cloud, for example, you can use controls to help ensure that security logs and necessary cross-account access permissions are created, and not altered.

This IaC artifact (CTC or ControlTowerControls) is a collection of reusable resources that accelerate the delivery of preventive, detective and proactive security controls (sometimes called guardrails) on the AWS Cloud and helps with faster deployment to production. It is used to implement the foundational structure of an organization by following AWS Control Tower best practices.

CTC implements a deployment process throughout IaC deployment by using AWS services such AWS Cloud Development Kit and Cloudformation.

AWS CDK and CloudFormation services act as the IaC layer to provide reproducible and fast deployments with easy operations and administration.

A control is a high-level rule that provides ongoing governance for your overall AWS environment. It's expressed in plain language. AWS Control Tower implements preventive, detective, and proactive controls that help you govern your resources and monitor compliance across groups of AWS accounts.

A control applies to an entire organizational unit (OU), and every AWS account within the OU is affected by the control. Therefore, when users perform work in any AWS account in your landing zone, they're always subject to the controls that are governing their account's OU.

## Overview

The solution consists of the following:
- A **set of Control Tower controls** to be deployed in the Control Tower master account with the desired controls to be deploy in the Lanzing Zone.

![Architecture](img/ctc-architecture.png)


## Setup

### Requirements
To deploy this solution, you need


| Name | Version |
|------|---------|
| <a name="requirement_ct"></a> [AWS Control Tower](https://aws.amazon.com/controltower/) | >= 3.0 |
| <a name="requirement_python"></a> [Python](https://www.python.org/) | >= 3.9 |
| <a name="requirement_npm"></a> [npm](https://www.npmjs.com/) | >= 8.9.0 |
| <a name="requirement_gem"></a> [gem](https://rubygems.org/) | >= 3.3.11 |

The `cdk.json` file tells the CDK Toolkit how to execute the code.
The `package.json` file installs `cfn_nag` and requires `npm` and `gem` to be already installed.

Also, make sure that for deploying [proactive](https://docs.aws.amazon.com/controltower/latest/userguide/proactive-controls.html) controls you must previously apply an elective, SCP-based control with the identifier **CT.CLOUDFORMATION.PR.1** before you can activate proactive controls on an OU. See Disallow management of resource types, modules, and hooks within the AWS CloudFormation registry. If this SCP is not activated, you'll see an error message directing you to enable this control as a prerequisite, or showing it as a dependency for other proactive controls.

## Controls Configuration File
Update the configuration file `constants.py` like the following example:
```
ACCOUNT_ID = <AWS Account Identifier>
AWS_CONTROL_TOWER_REGION = <AWS Control Tower Region>
GUARDRAILS_CONFIGURATION = [
    {
        "Enable-Control": {
            "AWS-GR_ENCRYPTED_VOLUMES",
            ...
        },
        "OrganizationalUnitIds": ["<Organizational Unit Id>", "<Organizational Unit Id>"...],
    },
    {
        "Enable-Control": {
            "AWS-GR_SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED",
            ...
        },
        "OrganizationalUnitIds": ["<Organizational Unit Id>"...],
    },
]
```

The organizational unit ids should follow the pattern `^ou-[0-9a-z]{4,32}-[a-z0-9]{8,32}$`, for example, `ou-1111-11111111`.

The `control_names` are found after the `“/”` of the `API controlIdentifier` see the next example of an `API controlIdentifier`: `arn:aws:controltower:REGION::control/CONTROL_NAME`.


## Control Behavior And Guidance

[Controls are categorized according to their behavior and their guidance.](https://docs.aws.amazon.com/controltower/latest/userguide/controls.html)

[For a full list of preventive, detective and proactive available controls, see the The AWS Control Tower controls library.](https://docs.aws.amazon.com/controltower/latest/userguide/controls-reference.html)


## Deployment

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, activate the virtualenv.

```
$ source .venv/bin/activate
```

For Windows platform, activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, install the required dependencies.

```
$ ./scripts/install_deps.sh
```

Setup AWS CDK 
```
$ npx cdk bootstrap
```
Synthesize and deploy the CloudFormation template.

```
$ npx cdk synth
$ npx cdk deploy
```

## Useful Commands

 * `npx cdk ls`          list all stacks in the app
 * `npx cdk synth`       emits the synthesized CloudFormation template
 * `npx cdk deploy`      deploy this stack
 * `npx cdk destroy`     destroy this stack
 * `npx cdk diff`        compare deployed stack with current state
 * `npx cdk docs`        open CDK documentation

## Authors

Pattern created by Ivan Girardi (AWS) and Iker Reina Fuente (AWS).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.


