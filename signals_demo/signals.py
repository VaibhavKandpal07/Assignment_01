import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyModel



@receiver(post_save, sender=MyModel)
def q1_sync_signal(sender, instance, **kwargs):
    print(f"[Q1] Signal handler STARTED at {time.strftime('%H:%M:%S')}")
    time.sleep(2)  # Simulate delay
    print(f"[Q1] Signal handler FINISHED at {time.strftime('%H:%M:%S')}")


@receiver(post_save, sender=MyModel)
def q2_thread_signal(sender, instance, **kwargs):
    signal_thread_id = threading.current_thread().ident
    print(f"[Q2] Signal Thread ID: {signal_thread_id}")



from django.db import transaction

@receiver(post_save, sender=MyModel)
def q3_transaction_signal(sender, instance, **kwargs):
    print(f"[Q3] Inside signal — still within transaction (before commit)")
    transaction.on_commit(lambda: print(f"[Q3] on_commit fired — transaction committed NOW"))
