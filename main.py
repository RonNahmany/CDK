from constructs import Construct
from cdktf import App, NamedRemoteWorkspace, TerraformStack, TerraformOutput, RemoteBackend, FileProvisioner, \
    LocalExecProvisioner, RemoteExecProvisioner
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.security_group import SecurityGroup, SecurityGroupIngress, SecurityGroupEgress, \
    SecurityGroupConfig
from cdktf_cdktf_provider_aws.subnet import Subnet
from cdktf_cdktf_provider_aws.internet_gateway import InternetGateway
from cdktf_cdktf_provider_aws.route_table import RouteTable
from cdktf_cdktf_provider_aws.route import Route
from cdktf_cdktf_provider_aws.route_table_association import RouteTableAssociation
from cdktf_cdktf_provider_aws.key_pair import KeyPair
from Credencials import Cred
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import params
from cdktf import SSHProvisionerConnection
import install_docker


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, "AWS", region=params.get_region_from_CN(),
                    secret_key=Cred.Secret.value,
                    access_key=Cred.Access.value)

        vpc = Vpc(self, "Work_VPC",
                  cidr_block=Cred.max_subnet.value,
                  tags={"Name": "Work_VPC"},
                  enable_dns_hostnames=True,
                  enable_dns_support=True,

                  )
        subnet = Subnet(self, "Public_Subnet",
                        vpc_id=vpc.id,
                        cidr_block="10.0.5.0/24",
                        map_public_ip_on_launch=True,
                        availability_zone=params.get_azs(),
                        tags={"Name": "Public_Subnet_Main"},

                        )
        internet_gw = InternetGateway(self, "IGW ", vpc_id=vpc.id, tags={"Name": "IGW"})
        route_table = RouteTable(self, "IGW_route", vpc_id=vpc.id, tags={"Name": "IGW_route"})
        route = Route(self, "public_route", route_table_id=route_table.id, destination_cidr_block="0.0.0.0/0",
                      gateway_id=internet_gw.id)
        rta = RouteTableAssociation(self, "RTA", subnet_id=subnet.id, route_table_id=route_table.id)

        sec_group = SecurityGroup(self, "mySG",
                                  name="Full unlimited acess",
                                  vpc_id=vpc.id,
                                  ingress=[{
                                      "fromPort": int(0),
                                      "toPort": int(0),
                                      "protocol": "-1",
                                      "description": "Inbound rule Access",
                                      "cidrBlocks": ["0.0.0.0/0"]

                                  }],
                                  egress=[{
                                      "fromPort": int(0),
                                      "toPort": int(0),
                                      "protocol": "-1",
                                      "description": "outbound rule Access",
                                      "cidrBlocks": ["0.0.0.0/0"]

                                  }]
                                  )

        #Create Key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Serialize the private key to PEM format
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # Use a password if desired
        )
        pem_private_key_string = pem_private_key.decode('utf-8')

        #Save the private key to a .pem file
        with open("private_key.pem", "wb") as private_file:
            private_file.write(pem_private_key)

        # Derive the public key from the private key
        public_key = private_key.public_key()
        ssh_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        ).decode("utf-8")

        key = KeyPair(self, "tf_key", key_name="Public_Key", public_key=ssh_public_key)

        instance = Instance(self, "application",
                            ami="ami-0770a5f5dffd22cb3",
                            instance_type="t3.micro",
                            vpc_security_group_ids=[sec_group.id],
                            tags={"Name": "DockerApplication"},
                            subnet_id=subnet.id,
                            security_groups=[sec_group.id],
                            key_name=key.id,
                            user_data=install_docker.InstallDocker.script.value

                            )
        # print(install_docker.InstallDocker.script.value)  # Prints the script to the console

        # ssh = SSHProvisionerConnection(type="ssh",
        #                                host=instance.public_dns,
        #                                host_key=instance,
        #                                user="ec2-user",
        #                                script_path="./install_docker.py"
        #                                )
        #
        # provision = RemoteExecProvisioner(type="ssh",
        #                                   connection=ssh,
        #                                   script="./install_docker.py",
        #                                   inline=["python3 ./install_docker.py"]
        #                                   )
        #
        #
        # TerraformOutput(self, "sshsettings",
        #                 value=[provision.script, provision.connection]
        #                 )
        TerraformOutput(self, "user_data",
                        value=[instance.user_data]
                        )


app = App()
stack = MyStack(app, "terraform_Lunch_Config")

app.synth()
