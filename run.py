import uvicorn


if __name__ == '__main__':
    uvicorn.run("pyruby_backend.main:app", reload=True)