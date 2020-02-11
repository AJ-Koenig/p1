# from .hash_str import get_csci_salt, get_user_id, hash_str
import os
import pandas as pd

from pset_1.hash_str import get_csci_salt, get_user_id, hash_str
from pset_1.io import atomic_write


def get_user_hash(username, salt=None):
    salt = salt or get_csci_salt()
    return hash_str(username, salt=salt)


if __name__ == "__main__":

    for user in ["gorlins", "<YOUR_GITHUB_USERNAME>"]:
        print("Id for {}: {}".format(user, get_user_id(user)))

    data_source = "data/hashed.xlsx"
    data_source_p = "data/hashed.parquet"


    # TODO: read in, save as new parquet file, read back just id column, print

    if os.path.exists(data_source_p):
        data = pd.read_parquet(data_source_p)
    else:
        raw_data = pd.read_excel(data_source,index_col=0)
        raw_data = raw_data.iloc[:,[0]]
        print(raw_data)

        with atomic_write(data_source_p,as_file=False) as f:
            raw_data.to_parquet(f)

        data = pd.read_parquet(data_source_p)


