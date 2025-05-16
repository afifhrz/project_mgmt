from django.db import models

class Status(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    PROGRESS = 'PROGRESS', 'On Progress'
    PENDING = 'PENDING', 'Pending'
    DONE = 'DONE', 'Done'
    CANCELLED = 'CANCELLED', 'Cancelled'
    REOPEN = 'REOPEN', 'Reopen'
    
class RMU(models.TextChoices):
    RMU = 'RMU', 'RMU'
    SSBE = 'SSBE', 'SSB E'
    
class Section(models.TextChoices):
    FSE = 'FSE', 'FSE'
    CMO = 'CMO', 'CMO'
    HSE = 'HSE', 'HSE'
    OHS = 'OHS', 'OHS'
    PAR = 'PAR', 'PAR'
    PDON = 'PDON', 'PDON'
    PRD = 'PRD', 'PRD'
    PROE = 'PROE', 'PROE'
    RELATION = 'RELATION', 'RELATION'
    RMA = 'RMA', 'RMA'
    WMN = 'WMN', 'WMN'
    ENG = 'ENG', 'ENG'
    ISCSD = 'ISCSD', 'ISCSD'
    SEC = 'SEC', 'SEC'
    MAI = 'MAI', 'MAI'

class RiskLevel(models.TextChoices):
    LOW = 'L', 'L'
    MI = 'MI', 'M-I'
    MII = 'MII', 'M-II'
    HIGH = 'H', 'H'
    CRITICAL = 'C', 'C'
    
class PtwBasedOnRiskLevel(models.TextChoices):
    A = 'A', 'A'
    B = 'B', 'B'