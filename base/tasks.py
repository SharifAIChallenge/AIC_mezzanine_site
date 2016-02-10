from celery import shared_task


@shared_task(bind=True, queue='compile_queue')
def compile_code(self, submit_id):
    pass