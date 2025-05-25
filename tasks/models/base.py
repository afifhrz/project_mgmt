from django.db import models
from common.models.base import BaseModel
from .enums import RMU, Section, Status, RiskLevel, PtwBasedOnRiskLevel

class BaseTasks(BaseModel):
    rmu = models.CharField(max_length=10, choices=RMU.choices, default=RMU.RMU)
    taskname = models.TextField()
    section = models.CharField(max_length=10, choices=Section.choices, default=Section.FSE)
    plan_start_date = models.DateField()
    plan_end_date = models.DateField()
    break_in = models.BooleanField(default=False)
    need_contingency = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True)
    planned_work_duration = models.IntegerField()
    planned_manpower = models.IntegerField()
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    unattained_reason = models.TextField(blank=True, null=True)
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices, default=RiskLevel.LOW)
    risk_likelihood = models.IntegerField(default=0)
    risk_impact = models.IntegerField(default=0)
    priority_urgency = models.IntegerField(default=0)
    priority_impact = models.IntegerField(default=0)
    work_pack_readiness = models.BooleanField(default=True)
    ptw_based_on_risk_level = models.CharField(max_length=10, choices=PtwBasedOnRiskLevel.choices, default=PtwBasedOnRiskLevel.A)
    budgetary_planning = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budgetary_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issue_id = models.CharField(max_length=20, blank=True)
    json_data = None
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        risk_score = self.risk_likelihood * self.risk_impact
        if risk_score >= 9:
            self.risk_level = RiskLevel.HIGH
        elif risk_score == 5 or risk_score == 8 or risk_score == 9:
            self.risk_level = RiskLevel.MII
        elif risk_score == 4 or risk_score == 6:
            self.risk_level = RiskLevel.MI
        else:
            self.risk_level = RiskLevel.LOW
        
        if not self.issue_id:
            # Generate issue_id as prefix + (number of tasks in the current project + 1)
            if hasattr(self, 'sprint') and hasattr(self.sprint, 'project'):
                project = self.sprint.project
                from .models import Task  # Import here to avoid circular import
                task_count = Task.objects.filter(sprint__project=project).count()
                self.issue_id = f"{project.prefix}-{task_count + 1}"
        super().save(*args, **kwargs)