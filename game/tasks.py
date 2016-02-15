from celery import shared_task

@shared_task(bind=True, queue='game_queue')
def run_game(self, game_id):
    pass
