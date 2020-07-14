import celery
import json
from celery.backends.base import DisabledBackend
from django.utils.translation import gettext_lazy as _
from django_celery_results.models import TaskResult


class QueueManager:
    def retry_queue(self, task_id):
        task = TaskResult.objects.filter(task_id=task_id).first()

        if task:
            if task.status == 'FAILURE':
                capp = celery.Celery()

                try:
                    ctask = capp.tasks[task.task_name]
                except KeyError:
                    return {
                        'message': "Unknown task '%s'" % task.task_name,
                        'status': 'NotFound'
                    }

                result = ctask.apply_async(
                    args=self.normalize_data(task.task_args),
                    kwargs=self.normalize_data(task.task_kwargs)
                )

                data = {'task_id': task.task_id}
                if self.backend_configured(result):
                    data.update(state=result.state)

                return {
                    'data': data,
                    'status': 'Found'
                }
            else:
                return {
                    'message': _('Task with ID (%(task_id)s) is not in FAILURE state, hence it cannot be retried.') % {
                        'task_id': task_id
                    },
                    'status': 'Forbidden'
                }

        return {
            'message': _('Task with ID (%(task_id)s) not found!') % {
                'task_id': task_id
            },
            'status': 'NotFound'
        }

    @staticmethod
    def backend_configured(result):
        return not isinstance(result.backend, DisabledBackend)

    @staticmethod
    def normalize_data(data):
        task_args_split = list(str(data).replace("'", '"'))

        if len(task_args_split) >= 2:
            task_args_split[0] = '['
            task_args_split[-1] = ']'

        return list(json.loads(''.join(task_args_split)))
