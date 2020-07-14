from flower.utils.template import humanize


def format_task(task):
    task.args = humanize(task.args, length=500)
    task.kwargs = humanize(task.kwargs, length=500)
    task.result = humanize(task.result, length=500)
    return task
