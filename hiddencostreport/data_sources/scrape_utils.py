import base64
from ..constants import DATADIR


def filename_encode(metric_name: str, metric_designer: str):
    return (base64.urlsafe_b64encode(f"{metric_designer}+{metric_name}".encode("UTF-8"))).decode("UTF-8")

def filename_decode(filename):
    decoded = base64.urlsafe_b64decode(filename).decode("UTF-8").split("+")
    return {"metric_designer": decoded[0], "metric_name": decoded[1]}
