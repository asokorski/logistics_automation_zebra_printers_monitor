from pysnmp.hlapi.v1arch.asyncio import *
from pysnmp_sync_adapter import get_cmd_sync, create_transport


printer_ip = '10.55.154.116'
community = CommunityData('public', mpModel=1)  #SNMPv2c
transport = create_transport(UdpTransportTarget, (printer_ip, 161), timeout=2)

oids = [
    ObjectType(ObjectIdentity('1.3.6.1.4.1.10642.200.19.7.0')),
    ObjectType(ObjectIdentity('1.3.6.1.4.1.10642.200.19.8.0')),
    ObjectType(ObjectIdentity('1.3.6.1.4.1.10642.200.19.20.0')),
]

# Performing SNMP GET
errorInd, errorStatus, errorIndex, varBinds = get_cmd_sync(
    SnmpDispatcher(), community, transport, *oids
)

# Results
if errorInd or errorStatus:
    print("Error:", errorInd or errorStatus.prettyPrint())
else:
    for varBind in varBinds:
        name, val = varBind
        print(f"{name.prettyPrint()} = {val.prettyPrint()}")
