from typing import List, Optional
from pydantic import BaseModel

class PortsSchema(BaseModel):
    cport: str
    hport: Optional[str]
    proto: str

class VolumesSchema(BaseModel):
    container: str
    bind: str

class EnvSchema(BaseModel):
    label: str
    default: str
    name: Optional[str]
    description: Optional[str]

class SysctlsSchema(BaseModel):
    name: str
    value: str

class DeployForm(BaseModel):
    name: str
    image: str
    restart_policy: str
    notes: Optional[str]
    ports: Optional[List[PortsSchema]]
    volumes: Optional[List[VolumesSchema]]
    env: Optional[List[EnvSchema]]
    sysctls: Optional[List[SysctlsSchema]]
    cap_add: Optional[List[str]]
# LOGS #
class DeployLogs(BaseModel):
    logs: str
class AppLogs(BaseModel):
    logs: str

# Processes #
class Processes(BaseModel):
    Processes: List[List[str]]
    Titles: List[str]