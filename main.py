from constructs import Construct
from cdktf import App, NamedRemoteWorkspace, TerraformStack, TerraformOutput, RemoteBackend
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.security_group import SecurityGroup
from cdktf_cdktf_provider_aws.subnet import Subnet
from Credencials import Cred


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, "AWS", region="us-west-1",
                    secret_key=Cred.Secret.value,
                    access_key=Cred.Access.value)

        vpc = Vpc(self, "myVpc",
                  cidr_block="10.0.0.0/16",
                  instance_tenancy="default",
                  tags={"Name": "MYvcpProject"},
                  enable_dns_hostnames=True,
                  enable_dns_support=True,

                  )
        subnet = Subnet(self,"mySubnet",
                        vpc_id=vpc.id,
                        cidr_block="10.0.1.0/24",
                        map_public_ip_on_launch=True,
                        tags={"Name": "MySubnet"}

                        )
        sec_group = SecurityGroup(self, "mySG", name="allow access", vpc_id=vpc.id)

        instance = Instance(self, "compute",
                            ami="ami-01456a894f71116f2",
                            instance_type="t2.micro",
                            vpc_security_group_ids=[sec_group.id],
                            tags={"Name": "MyInstance"},
                            subnet_id=subnet.id
                            )

        # TerraformOutput(self, "public_ip",
        #                 value=instance.public_ip,
        #                 )


app = App()
stack = MyStack(app, "aws_instance")

app.synth()
