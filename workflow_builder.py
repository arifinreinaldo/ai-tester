"""
Workflow Builder Module
Create complex automation workflows by chaining recordings
"""

import json
import os
from datetime import datetime
from conditional_logic import ImageExistsCondition, PixelColorCondition


class WorkflowStep:
    """Base class for workflow steps"""

    def __init__(self, step_id, step_type, name=""):
        self.step_id = step_id
        self.step_type = step_type
        self.name = name or f"Step {step_id}"
        self.enabled = True

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'step_id': self.step_id,
            'step_type': self.step_type,
            'name': self.name,
            'enabled': self.enabled
        }

    def execute(self, context):
        """Execute the step - to be implemented by subclasses"""
        raise NotImplementedError


class PlayRecordingStep(WorkflowStep):
    """Step that plays a recording"""

    def __init__(self, step_id, slot_name, speed=1.0, name=""):
        super().__init__(step_id, "play_recording", name)
        self.slot_name = slot_name
        self.speed = speed

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'slot_name': self.slot_name,
            'speed': self.speed
        })
        return data

    def execute(self, context):
        """Execute the recording"""
        print(f"[{self.name}] Playing recording '{self.slot_name}' at {self.speed}x speed")

        recording_manager = context.get('recording_manager')
        player = context.get('player')

        if not recording_manager or not player:
            return {'success': False, 'error': 'Missing recording_manager or player'}

        actions = recording_manager.load_recording(self.slot_name)
        if not actions:
            return {'success': False, 'error': f'Recording {self.slot_name} not found'}

        try:
            player.load_actions(actions)
            player.play(speed_multiplier=self.speed)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class DelayStep(WorkflowStep):
    """Step that adds a delay"""

    def __init__(self, step_id, seconds, name=""):
        super().__init__(step_id, "delay", name)
        self.seconds = seconds

    def to_dict(self):
        data = super().to_dict()
        data['seconds'] = self.seconds
        return data

    def execute(self, context):
        """Execute delay"""
        import time
        print(f"[{self.name}] Waiting {self.seconds} seconds...")
        time.sleep(self.seconds)
        return {'success': True}


class ConditionalStep(WorkflowStep):
    """Step with if/then/else branches"""

    def __init__(self, step_id, condition_type, condition_params, then_steps=None, else_steps=None, name=""):
        super().__init__(step_id, "conditional", name)
        self.condition_type = condition_type
        self.condition_params = condition_params
        self.then_steps = then_steps or []
        self.else_steps = else_steps or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'condition_type': self.condition_type,
            'condition_params': self.condition_params,
            'then_steps': [s.to_dict() for s in self.then_steps],
            'else_steps': [s.to_dict() for s in self.else_steps]
        })
        return data

    def evaluate_condition(self, context):
        """Evaluate the condition"""
        if self.condition_type == 'image_exists':
            from image_recognition import ImageRecognition
            image_rec = ImageRecognition()
            image_path = self.condition_params.get('image_path')
            confidence = self.condition_params.get('confidence', 0.8)
            location = image_rec.find_image_on_screen(image_path, confidence)
            return location is not None

        elif self.condition_type == 'pixel_color':
            from image_recognition import ImageRecognition
            image_rec = ImageRecognition()
            x = self.condition_params.get('x')
            y = self.condition_params.get('y')
            expected = self.condition_params.get('expected_color')
            tolerance = self.condition_params.get('tolerance', 10)
            return image_rec.match_pixel_color(x, y, expected, tolerance)

        elif self.condition_type == 'variable':
            var_name = self.condition_params.get('var_name')
            operator = self.condition_params.get('operator')
            value = self.condition_params.get('value')

            variables = context.get('variables', {})
            var_value = variables.get(var_name)

            if operator == '==':
                return var_value == value
            elif operator == '!=':
                return var_value != value
            elif operator == '>':
                return var_value > value
            elif operator == '<':
                return var_value < value
            elif operator == '>=':
                return var_value >= value
            elif operator == '<=':
                return var_value <= value

        return False

    def execute(self, context):
        """Execute conditional step"""
        print(f"[{self.name}] Evaluating condition: {self.condition_type}")

        condition_result = self.evaluate_condition(context)

        if condition_result:
            print(f"[{self.name}] Condition TRUE - executing THEN branch ({len(self.then_steps)} steps)")
            for step in self.then_steps:
                if step.enabled:
                    result = step.execute(context)
                    if not result.get('success', False):
                        return result
        else:
            print(f"[{self.name}] Condition FALSE - executing ELSE branch ({len(self.else_steps)} steps)")
            for step in self.else_steps:
                if step.enabled:
                    result = step.execute(context)
                    if not result.get('success', False):
                        return result

        return {'success': True}


class LoopStep(WorkflowStep):
    """Step that loops other steps"""

    def __init__(self, step_id, loop_type, loop_params, steps=None, name=""):
        super().__init__(step_id, "loop", name)
        self.loop_type = loop_type  # 'count', 'while', 'until'
        self.loop_params = loop_params
        self.steps = steps or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'loop_type': self.loop_type,
            'loop_params': self.loop_params,
            'steps': [s.to_dict() for s in self.steps]
        })
        return data

    def execute(self, context):
        """Execute loop"""
        if self.loop_type == 'count':
            count = self.loop_params.get('count', 1)
            print(f"[{self.name}] Looping {count} times...")

            for i in range(count):
                print(f"[{self.name}] Iteration {i+1}/{count}")
                for step in self.steps:
                    if step.enabled:
                        result = step.execute(context)
                        if not result.get('success', False):
                            return result

        elif self.loop_type == 'while' or self.loop_type == 'until':
            # Similar to conditional, but keeps looping
            max_iterations = self.loop_params.get('max_iterations', 100)
            print(f"[{self.name}] Looping {self.loop_type} condition (max {max_iterations} iterations)...")

            iteration = 0
            while iteration < max_iterations:
                # Create temp conditional to evaluate
                temp_cond = ConditionalStep(
                    -1,
                    self.loop_params.get('condition_type'),
                    self.loop_params.get('condition_params'),
                    name="Loop Condition"
                )

                condition_result = temp_cond.evaluate_condition(context)

                # For 'while', continue if true; for 'until', continue if false
                should_continue = condition_result if self.loop_type == 'while' else not condition_result

                if not should_continue:
                    break

                print(f"[{self.name}] Iteration {iteration+1}")
                for step in self.steps:
                    if step.enabled:
                        result = step.execute(context)
                        if not result.get('success', False):
                            return result

                iteration += 1

            if iteration >= max_iterations:
                print(f"[{self.name}] Max iterations reached")

        return {'success': True}


class TryCatchStep(WorkflowStep):
    """Step with error handling"""

    def __init__(self, step_id, try_steps=None, catch_steps=None, retry_count=0, name=""):
        super().__init__(step_id, "try_catch", name)
        self.try_steps = try_steps or []
        self.catch_steps = catch_steps or []
        self.retry_count = retry_count

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'try_steps': [s.to_dict() for s in self.try_steps],
            'catch_steps': [s.to_dict() for s in self.catch_steps],
            'retry_count': self.retry_count
        })
        return data

    def execute(self, context):
        """Execute with error handling"""
        attempts = 0
        max_attempts = self.retry_count + 1

        while attempts < max_attempts:
            attempts += 1
            print(f"[{self.name}] Attempt {attempts}/{max_attempts}")

            try:
                success = True
                for step in self.try_steps:
                    if step.enabled:
                        result = step.execute(context)
                        if not result.get('success', False):
                            success = False
                            raise Exception(result.get('error', 'Step failed'))

                if success:
                    return {'success': True}

            except Exception as e:
                print(f"[{self.name}] Error: {e}")

                if attempts >= max_attempts:
                    print(f"[{self.name}] All attempts failed - executing catch block")
                    for step in self.catch_steps:
                        if step.enabled:
                            step.execute(context)
                    return {'success': False, 'error': str(e)}
                else:
                    print(f"[{self.name}] Retrying...")

        return {'success': False}


class Workflow:
    """Complete workflow with multiple steps"""

    def __init__(self, name="Untitled Workflow"):
        self.name = name
        self.steps = []
        self.variables = {}
        self.created_at = datetime.now().isoformat()
        self.modified_at = self.created_at

    def add_step(self, step):
        """Add a step to workflow"""
        self.steps.append(step)
        self.modified_at = datetime.now().isoformat()

    def remove_step(self, step_id):
        """Remove a step"""
        self.steps = [s for s in self.steps if s.step_id != step_id]
        self.modified_at = datetime.now().isoformat()

    def move_step(self, step_id, new_position):
        """Move step to new position"""
        step = next((s for s in self.steps if s.step_id == step_id), None)
        if step:
            self.steps.remove(step)
            self.steps.insert(new_position, step)
            self.modified_at = datetime.now().isoformat()

    def get_step(self, step_id):
        """Get step by ID"""
        return next((s for s in self.steps if s.step_id == step_id), None)

    def execute(self, recording_manager, player):
        """Execute the entire workflow"""
        print(f"\n{'='*70}")
        print(f"EXECUTING WORKFLOW: {self.name}")
        print(f"{'='*70}")
        print(f"Total steps: {len(self.steps)}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")

        context = {
            'recording_manager': recording_manager,
            'player': player,
            'variables': self.variables.copy(),
            'workflow_name': self.name
        }

        for i, step in enumerate(self.steps):
            if not step.enabled:
                print(f"[Step {i+1}/{len(self.steps)}] Skipped (disabled)")
                continue

            print(f"\n[Step {i+1}/{len(self.steps)}] {step.name} ({step.step_type})")

            result = step.execute(context)

            if not result.get('success', False):
                error = result.get('error', 'Unknown error')
                print(f"\n{'='*70}")
                print(f"WORKFLOW FAILED at step {i+1}: {error}")
                print(f"{'='*70}\n")
                return False

        print(f"\n{'='*70}")
        print(f"WORKFLOW COMPLETED SUCCESSFULLY")
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        return True

    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'name': self.name,
            'steps': [s.to_dict() for s in self.steps],
            'variables': self.variables,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }

    def save(self, filename):
        """Save workflow to file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"Workflow saved to {filename}")

    @staticmethod
    def load(filename):
        """Load workflow from file"""
        with open(filename, 'r') as f:
            data = json.load(f)

        workflow = Workflow(data['name'])
        workflow.variables = data.get('variables', {})
        workflow.created_at = data.get('created_at', datetime.now().isoformat())
        workflow.modified_at = data.get('modified_at', datetime.now().isoformat())

        # Reconstruct steps
        for step_data in data['steps']:
            step = Workflow._reconstruct_step(step_data)
            if step:
                workflow.steps.append(step)

        print(f"Workflow loaded from {filename}")
        return workflow

    @staticmethod
    def _reconstruct_step(step_data):
        """Reconstruct step from dictionary"""
        step_type = step_data['step_type']
        step_id = step_data['step_id']
        name = step_data.get('name', '')

        if step_type == 'play_recording':
            step = PlayRecordingStep(
                step_id,
                step_data['slot_name'],
                step_data.get('speed', 1.0),
                name
            )
        elif step_type == 'delay':
            step = DelayStep(step_id, step_data['seconds'], name)
        elif step_type == 'conditional':
            then_steps = [Workflow._reconstruct_step(s) for s in step_data.get('then_steps', [])]
            else_steps = [Workflow._reconstruct_step(s) for s in step_data.get('else_steps', [])]
            step = ConditionalStep(
                step_id,
                step_data['condition_type'],
                step_data['condition_params'],
                then_steps,
                else_steps,
                name
            )
        elif step_type == 'loop':
            loop_steps = [Workflow._reconstruct_step(s) for s in step_data.get('steps', [])]
            step = LoopStep(
                step_id,
                step_data['loop_type'],
                step_data['loop_params'],
                loop_steps,
                name
            )
        elif step_type == 'try_catch':
            try_steps = [Workflow._reconstruct_step(s) for s in step_data.get('try_steps', [])]
            catch_steps = [Workflow._reconstruct_step(s) for s in step_data.get('catch_steps', [])]
            step = TryCatchStep(
                step_id,
                try_steps,
                catch_steps,
                step_data.get('retry_count', 0),
                name
            )
        else:
            return None

        step.enabled = step_data.get('enabled', True)
        return step


class WorkflowManager:
    """Manage multiple workflows"""

    def __init__(self, workflows_dir='workflows'):
        self.workflows_dir = workflows_dir
        self._ensure_dir_exists()

    def _ensure_dir_exists(self):
        """Ensure workflows directory exists"""
        if not os.path.exists(self.workflows_dir):
            os.makedirs(self.workflows_dir)

    def get_workflow_path(self, workflow_name):
        """Get path for workflow file"""
        return os.path.join(self.workflows_dir, f"{workflow_name}.json")

    def save_workflow(self, workflow):
        """Save workflow"""
        filepath = self.get_workflow_path(workflow.name)
        workflow.save(filepath)

    def load_workflow(self, workflow_name):
        """Load workflow"""
        filepath = self.get_workflow_path(workflow_name)
        if not os.path.exists(filepath):
            print(f"Workflow '{workflow_name}' not found")
            return None
        return Workflow.load(filepath)

    def list_workflows(self):
        """List all workflows"""
        import glob
        pattern = os.path.join(self.workflows_dir, "*.json")
        workflows = []

        for filepath in glob.glob(pattern):
            filename = os.path.basename(filepath)
            name = filename.replace('.json', '')

            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)

                workflows.append({
                    'name': name,
                    'steps': len(data.get('steps', [])),
                    'created': data.get('created_at', 'Unknown'),
                    'modified': data.get('modified_at', 'Unknown')
                })
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

        return sorted(workflows, key=lambda x: x['modified'], reverse=True)

    def delete_workflow(self, workflow_name):
        """Delete workflow"""
        filepath = self.get_workflow_path(workflow_name)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Workflow '{workflow_name}' deleted")
            return True
        else:
            print(f"Workflow '{workflow_name}' not found")
            return False
