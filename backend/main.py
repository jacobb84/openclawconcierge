import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import init_db, Base, engine
from core.models import User, APIKey
from core.routes.auth import router as auth_router
from core.routes.api_keys import router as api_keys_router
from core.routes.plugins import router as plugins_router, set_plugin_manager
from core.plugin_manager import PluginManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

plugin_manager: PluginManager = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global plugin_manager
    
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    plugin_manager = PluginManager(app, settings.PLUGINS_DIR, settings.PLUGINS_CONFIG)
    set_plugin_manager(plugin_manager)
    plugin_manager.load_all()
    plugin_manager.start_watcher()
    logger.info("Plugin manager initialized")
    
    yield
    
    plugin_manager.stop_watcher()
    logger.info("Application shutdown")


app = FastAPI(
    title="OpenClaw Concierge API",
    description="A plugin-based dashboard for tracking concerts, events, news, and career opportunities",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(api_keys_router)
app.include_router(plugins_router)


@app.get("/")
def health_check():
    return {"status": "healthy", "service": "OpenClaw Concierge API", "version": "2.0.0"}


@app.get("/api/health")
def api_health():
    return {"status": "healthy", "plugins_loaded": len(plugin_manager.plugins) if plugin_manager else 0}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
