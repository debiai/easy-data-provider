APP_VERSION = "0.0.0"


def start_api_server(provider, host, port):
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="DebiAI Data-provider API",
        version=APP_VERSION,
        description="API for DebiAI data providers",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host=host, port=port)
