"""通过 pytest 原生插件机制注册 XAT Hook 和 SAT/ECU fixture。"""

pytest_plugins = ("framework.hooks", "framework.integrations.plugin")
