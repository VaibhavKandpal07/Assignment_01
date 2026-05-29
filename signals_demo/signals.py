import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyModel

# ─────────────────────────────────────────────
# Question 1: Synchronous or Asynchronous?
# ─────────────────────────────────────────────
# Django signals are SYNCHRONOUS by default.
# The signal handler runs BEFORE the save() call returns.
# We prove this by sleeping inside the handler and checking total time.

@receiver(post_save, sender=MyModel)
def q1_sync_signal(sender, instance, **kwargs):
    print(f"[Q1] Signal handler STARTED at {time.strftime('%H:%M:%S')}")
    time.sleep(2)  # Simulate delay
    print(f"[Q1] Signal handler FINISHED at {time.strftime('%H:%M:%S')}")


# ─────────────────────────────────────────────
# Question 2: Same Thread as Caller?
# ─────────────────────────────────────────────
# Django signals run in the SAME THREAD as the caller.
# We prove this by comparing thread IDs.

@receiver(post_save, sender=MyModel)
def q2_thread_signal(sender, instance, **kwargs):
    signal_thread_id = threading.current_thread().ident
    print(f"[Q2] Signal Thread ID: {signal_thread_id}")


# ─────────────────────────────────────────────
# Question 3: Same Database Transaction as Caller?
# ─────────────────────────────────────────────
# Django signals run in the SAME DATABASE TRANSACTION as the caller.
# We prove this using transaction.on_commit — if the signal runs
# inside the transaction, on_commit will fire AFTER the signal.

from django.db import transaction

@receiver(post_save, sender=MyModel)
def q3_transaction_signal(sender, instance, **kwargs):
    print(f"[Q3] Inside signal — still within transaction (before commit)")
    transaction.on_commit(lambda: print(f"[Q3] on_commit fired — transaction committed NOW"))
