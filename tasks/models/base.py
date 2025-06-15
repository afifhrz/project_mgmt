from django.db import models
from common.models.base import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
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
    unattained_reason = models.TextField(default="", null=True)
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices, default=RiskLevel.LOW)
    risk_likelihood = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    risk_impact = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
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
    
    def calculate_risk_score(self):
        try:
            # Convert to int if strings are passed, handle None values
            likelihood = int(self.risk_likelihood or 0)
            impact = int(self.risk_impact or 0)
            return likelihood * impact
        except (ValueError, TypeError):
            # If conversion fails, return 0 as fallback
            return 0
        
    def save(self, *args, **kwargs):
        risk_score = self.calculate_risk_score()
        if risk_score >= 9:
            self.risk_level = RiskLevel.HIGH
        elif risk_score == 5 or risk_score == 8 or risk_score == 9:
            self.risk_level = RiskLevel.MII
        elif risk_score == 4 or risk_score == 6:
            self.risk_level = RiskLevel.MI
        else:
            self.risk_level = RiskLevel.LOW
        
        if self.issue_id == "":
            # If issue_id is empty, generate it based on the project prefix and task count
            # Generate issue_id as prefix + (number of tasks in the current project + 1)
            if hasattr(self, 'seven_days') and hasattr(self.seven_days, 'project'):
                project = self.seven_days.project
                from .models import Task  # Import here to avoid circular import
                task_count = Task.objects.filter(seven_days__project=project).count()
                self.issue_id = f"{project.prefix}-{task_count + 1}"
        super().save(*args, **kwargs)