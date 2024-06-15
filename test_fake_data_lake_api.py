import os

from fake_data_lake_api import FakeDataLakeApi

server = "http://127.0.0.1:5000"

fdla = FakeDataLakeApi(server)

metadata = {'name': 'john', 'emoji': '😎', 'number': 44}

bs = os.urandom(8192)
id = fdla.create(metadata=metadata, b=bs)
assert id is not None
res_metadata, res_bs = fdla.read(id)
assert metadata == res_metadata
assert bs == res_bs

metadata2 = {'name': 'fred', 'hats': 2, 'ears': '🌽'}
cs = os.urandom(4096)
fdla.update(id, metadata=metadata2, b=cs)
res_metadata2, res_cs = fdla.read(id)
assert metadata2 == res_metadata2
assert cs == res_cs
fdla.delete(id)
x,y = fdla.read(id) 
assert x is None and y is None

print('tests succedded')
