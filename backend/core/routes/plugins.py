from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from core.database import get_db
from core.models import User
from core.security import get_current_user
from core.plugin_base import PluginMetadata

router = APIRouter(prefix="/api/plugins", tags=["Plugins"])

_plugin_manager = None


def set_plugin_manager(manager):
    """Set the plugin manager instance."""
    global _plugin_manager
    _plugin_manager = manager


def get_plugin_manager():
    """Get the plugin manager instance."""
    if _plugin_manager is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Plugin manager not initialized"
        )
    return _plugin_manager


@router.get("", response_model=List[PluginMetadata])
def list_plugins(current_user: User = Depends(get_current_user)):
    """List all loaded plugins with their metadata."""
    manager = get_plugin_manager()
    return manager.get_plugin_metadata()


@router.get("/dashboard")
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard data from all plugins."""
    manager = get_plugin_manager()
    
    dashboard_data = {}
    for name, plugin in manager.plugins.items():
        config = manager.plugin_configs.get(name, plugin.config)
        try:
            data = plugin.get_dashboard_query(db, limit=3)
            route = f"/{name}" if name != "careers" else "/career"
            dashboard_data[name] = {
                "display_name": config.display_name,
                "icon": config.icon,
                "color": config.color,
                "route": route,
                "layout": plugin.get_card_layout().model_dump(),
                **data
            }
        except Exception as e:
            route = f"/{name}" if name != "careers" else "/career"
            dashboard_data[name] = {
                "display_name": config.display_name,
                "icon": config.icon,
                "color": config.color,
                "route": route,
                "error": str(e),
                "items": [],
                "total": 0
            }
    
    return dashboard_data


@router.post("/{plugin_name}/reload")
def reload_plugin(
    plugin_name: str,
    current_user: User = Depends(get_current_user)
):
    """Reload a specific plugin."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    manager = get_plugin_manager()
    plugin = manager.reload_plugin(plugin_name)
    
    if plugin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin not found: {plugin_name}"
        )
    
    return {"message": f"Plugin reloaded: {plugin_name}"}


@router.put("/{plugin_name}/config")
def update_plugin_config(
    plugin_name: str,
    config_update: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Update plugin configuration."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    manager = get_plugin_manager()
    
    if plugin_name not in manager.plugin_configs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin not found: {plugin_name}"
        )
    
    config = manager.plugin_configs[plugin_name]
    
    for key, value in config_update.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            config.settings[key] = value
    
    manager.save_config()
    
    if plugin_name in manager.plugins:
        manager.plugins[plugin_name].on_config_change(config)
    
    return {"message": f"Plugin configuration updated: {plugin_name}"}
