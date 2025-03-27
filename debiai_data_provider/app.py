from debiai_data_provider.data_provider import DataProvider
from debiai_data_provider.version import VERSION


def start_api_server(data_provider: DataProvider, host, port):
    import uvicorn
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from debiai_data_provider.controller.routes import router as controller_router

    app = FastAPI(
        title="DebiAI Data-provider API",
        version=VERSION,
        description="API for DebiAI data providers",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.data_provider = data_provider

    app.include_router(controller_router)

    uvicorn.run(app, host=host, port=port)
