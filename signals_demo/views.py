import time
import threading
from django.http import HttpResponse
from django.db import transaction
from .models import MyModel


def test_q1_sync(request):
    """
    Q1: Proves signals are SYNCHRONOUS.
    Total time will be ~2s because the signal handler sleeps 2s
    and the save() does not return until the handler finishes.
    """
    start = time.time()
    print(f"[Q1] save() called at {time.strftime('%H:%M:%S')}")
    MyModel.objects.create(name="Q1 Test")
    end = time.time()
    elapsed = round(end - start, 2)
    print(f"[Q1] save() returned. Total time: {elapsed}s")
    return HttpResponse(
        f"<h2>Q1: Synchronous</h2>"
        f"<p>Total time for save(): <b>{elapsed}s</b></p>"
        f"<p>Because signal slept 2s and save() waited → SYNCHRONOUS ✅</p>"
    )


def test_q2_thread(request):
    """
    Q2: Proves signals run in the SAME THREAD as the caller.
    Caller thread ID == Signal thread ID.
    """
    caller_thread_id = threading.current_thread().ident
    print(f"[Q2] Caller Thread ID: {caller_thread_id}")
    MyModel.objects.create(name="Q2 Test")
    return HttpResponse(
        f"<h2>Q2: Same Thread</h2>"
        f"<p>Caller Thread ID: <b>{caller_thread_id}</b></p>"
        f"<p>Check server logs — Signal Thread ID will be identical ✅</p>"
    )


def test_q3_transaction(request):
    """
    Q3: Proves signals run in the SAME DB TRANSACTION as the caller.
    on_commit fires AFTER the signal, proving signal is inside the transaction.
    """
    with transaction.atomic():
        print("[Q3] Transaction STARTED")
        MyModel.objects.create(name="Q3 Test")
        print("[Q3] After create() — transaction still open")
    print("[Q3] Transaction COMMITTED")
    return HttpResponse(
        "<h2>Q3: Same Transaction</h2>"
        "<p>Check server logs:</p>"
        "<ol>"
        "<li>Transaction STARTED</li>"
        "<li>Signal fires: 'Inside signal — still within transaction'</li>"
        "<li>on_commit fires AFTER commit → proves signal was inside transaction ✅</li>"
        "</ol>"
    )
