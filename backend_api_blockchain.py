import assets_backend

try:
    assets_backend.test_backend()
except Exception as e:
    print(e)
