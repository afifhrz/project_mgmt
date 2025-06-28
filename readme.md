# Deployment Notes

## How to setup
1. `python -m virtenv virtenv`
2. activate virtual env
3. `pip install -r requirements.txt`
4. setup database
5. `python manage.py migrate`
6. run seeding `python .\manage.py loaddata auth trial-data`

## Dump Data
run this command
```
pip freeze > requirements.txt
cd seeding
python ..\manage.py dumpdata auth -o auth.json
python ..\manage.py dumpdata --exclude=auth --exclude=sessions -o trial-data.json
```

## Remove All Data
`python manage.py flush`

# Development Guides
1. Auto formatter using extension [autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8)
2. Function naming in urls follow apps naming (plural)
3. Model class name using singular
4. Templates file name follow apps naming (plural)

# App Capabilities

## Project Management

### 1. Project CRUD Operations (General Manager)
- **Create** new projects with detailed specifications
- **Read** existing project details and progress
- **Update** project information and parameters
- **Delete** projects when necessary
- Access to comprehensive project dashboard

### 2. Project Assignment Management
- General Manager can:
  - Assign Section Planners to specific projects
  - Reassign projects to different Section Planners
  - Remove Section Planners from projects

## Sprint and Task Management

### 3. 30-Day Sprint Management (Asset Planner)
- Initialize and plan 30-day sprints
- Set sprint objectives and goals
- Track sprint progress
- Define sprint deliverables

### 4. 30D Epic Task Management
- **Asset Planner responsibilities:**
  - Create 30D-level tasks
  - Define task requirements
  - Set task priorities
  - Estimate completion time
- **General Manager responsibilities:**
  - Review and approve 30D tasks
  - Monitor 30D progress

### 5. 7-Day Sprint Management (Section Planner)
- Create 7D sprint plans
- Align with 30-day sprint objectives
- Track daily progress
- Manage team workload
- Report 7D status

### 6. Task/Activity Management
- **Section Planner capabilities:**
  - Create detailed tasks and activities
  - Set deadlines and priorities
  - Track task progress
  - Update task status
- **Operations Manager responsibilities:**
  - Review and approve tasks
  - Monitor task execution