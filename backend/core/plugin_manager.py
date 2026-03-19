import importlib
import importlib.util
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Type
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from fastapi import FastAPI
from core.plugin_base import BasePlugin, PluginConfig, PluginMetadata
from core.database import Base, engine
import logging

logger = logging.getLogger(__name__)


class PluginConfigHandler(FileSystemEventHandler):
    """Handles file system events for plugin config hot-reload."""
    
    def __init__(self, manager: "PluginManager"):
        self.manager = manager
    
    def on_modified(self, event):
        if event.src_path.endswith(self.manager.config_file):
            logger.info(f"Plugin config changed: {event.src_path}")
            self.manager.reload_config()


class PluginManager:
    """Manages loading, unloading, and hot-reloading of plugins."""
    
    def __init__(self, app: FastAPI, plugins_dir: str = "plugins", config_file: str = "plugins.yaml"):
        self.app = app
        self.plugins_dir = Path(plugins_dir)
        self.config_file = config_file
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_configs: Dict[str, PluginConfig] = {}
        self._observer: Optional[Observer] = None
    
    def load_config(self) -> Dict[str, PluginConfig]:
        """Load plugin configurations from YAML file."""
        config_path = self.plugins_dir / self.config_file
        if not config_path.exists():
            logger.warning(f"Plugin config not found: {config_path}")
            return {}
        
        with open(config_path, "r") as f:
            raw_config = yaml.safe_load(f) or {}
        
        configs = {}
        for name, cfg in raw_config.get("plugins", {}).items():
            configs[name] = PluginConfig(name=name, **cfg)
        
        return configs
    
    def save_config(self):
        """Save current plugin configurations to YAML file."""
        config_path = self.plugins_dir / self.config_file
        
        plugins_data = {}
        for name, config in self.plugin_configs.items():
            plugins_data[name] = {
                "enabled": config.enabled,
                "display_name": config.display_name,
                "description": config.description,
                "icon": config.icon,
                "color": config.color,
                "order": config.order,
                "settings": config.settings
            }
        
        with open(config_path, "w") as f:
            yaml.dump({"plugins": plugins_data}, f, default_flow_style=False)
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins in the plugins directory."""
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return []
        
        plugins = []
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                plugins.append(item.name)
            elif item.is_file() and item.suffix == ".py" and item.stem != "__init__":
                plugins.append(item.stem)
        
        return plugins
    
    def load_plugin(self, name: str) -> Optional[BasePlugin]:
        """Load a single plugin by name."""
        if name in self.plugins:
            logger.info(f"Plugin already loaded: {name}")
            return self.plugins[name]
        
        try:
            plugin_path = self.plugins_dir / name
            
            if plugin_path.is_dir():
                module_path = plugin_path / "__init__.py"
            else:
                module_path = self.plugins_dir / f"{name}.py"
            
            if not module_path.exists():
                logger.error(f"Plugin module not found: {module_path}")
                return None
            
            spec = importlib.util.spec_from_file_location(
                f"plugins.{name}",
                module_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[f"plugins.{name}"] = module
            spec.loader.exec_module(module)
            
            plugin_class = getattr(module, "Plugin", None)
            if plugin_class is None or not issubclass(plugin_class, BasePlugin):
                logger.error(f"Plugin class not found in {name}")
                return None
            
            config = self.plugin_configs.get(name)
            plugin = plugin_class(config)
            
            for model in plugin.get_models():
                if hasattr(model, "__table__"):
                    model.__table__.create(engine, checkfirst=True)
            
            router = plugin.get_router()
            self.app.include_router(router, prefix=f"/api/{name}", tags=[plugin.display_name])
            
            plugin.on_load()
            self.plugins[name] = plugin
            
            logger.info(f"Plugin loaded: {name}")
            return plugin
            
        except Exception as e:
            logger.exception(f"Failed to load plugin {name}: {e}")
            return None
    
    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin by name."""
        if name not in self.plugins:
            return False
        
        plugin = self.plugins[name]
        plugin.on_unload()
        
        routes_to_remove = []
        for route in self.app.routes:
            if hasattr(route, "path") and route.path.startswith(f"/api/{name}"):
                routes_to_remove.append(route)
        
        for route in routes_to_remove:
            self.app.routes.remove(route)
        
        del self.plugins[name]
        
        module_name = f"plugins.{name}"
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        logger.info(f"Plugin unloaded: {name}")
        return True
    
    def reload_plugin(self, name: str) -> Optional[BasePlugin]:
        """Reload a plugin by name."""
        self.unload_plugin(name)
        return self.load_plugin(name)
    
    def reload_config(self):
        """Reload plugin configurations and apply changes."""
        new_configs = self.load_config()
        
        for name, new_config in new_configs.items():
            old_config = self.plugin_configs.get(name)
            self.plugin_configs[name] = new_config
            
            if name in self.plugins:
                plugin = self.plugins[name]
                
                if old_config and old_config.enabled and not new_config.enabled:
                    self.unload_plugin(name)
                elif new_config.enabled:
                    plugin.on_config_change(new_config)
            
            elif new_config.enabled:
                self.load_plugin(name)
        
        logger.info("Plugin configurations reloaded")
    
    def load_all(self):
        """Load all enabled plugins."""
        self.plugin_configs = self.load_config()
        discovered = self.discover_plugins()
        
        for name in discovered:
            if name not in self.plugin_configs:
                self.plugin_configs[name] = PluginConfig(
                    name=name,
                    display_name=name.replace("_", " ").title(),
                    enabled=True
                )
        
        sorted_plugins = sorted(
            self.plugin_configs.items(),
            key=lambda x: x[1].order
        )
        
        for name, config in sorted_plugins:
            if config.enabled:
                self.load_plugin(name)
    
    def start_watcher(self):
        """Start watching for config file changes."""
        if self._observer is not None:
            return
        
        handler = PluginConfigHandler(self)
        self._observer = Observer()
        self._observer.schedule(handler, str(self.plugins_dir), recursive=False)
        self._observer.start()
        logger.info("Plugin config watcher started")
    
    def stop_watcher(self):
        """Stop watching for config file changes."""
        if self._observer is not None:
            self._observer.stop()
            self._observer.join()
            self._observer = None
            logger.info("Plugin config watcher stopped")
    
    def get_plugin_metadata(self) -> List[PluginMetadata]:
        """Get metadata for all loaded plugins."""
        metadata = []
        for name, plugin in self.plugins.items():
            config = self.plugin_configs.get(name, plugin.config)
            metadata.append(PluginMetadata(
                name=plugin.name,
                display_name=config.display_name,
                description=config.description,
                version=plugin.version,
                enabled=config.enabled,
                icon=config.icon,
                color=config.color,
                order=config.order,
                route_prefix=f"/api/{name}",
                card_layout=plugin.get_card_layout()
            ))
        return sorted(metadata, key=lambda x: x.order)
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a loaded plugin by name."""
        return self.plugins.get(name)
