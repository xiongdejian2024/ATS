"""Small, typed Agent protocol; transport ownership is local to one controller."""

PROTOCOL_VERSION = 2
HEARTBEAT_TIMEOUT = 90.0
PING_INTERVAL = 30.0
SEND_TIMEOUT = 5.0
CLOSE_TIMEOUT = 1.0
MAX_FRAME_BYTES = 16 * 1024 * 1024
AGENT_MESSAGE_TYPES = frozenset(
    {
        "auth",
        "heartbeat",
        "pong",
        "task_result",
        "task_log",
        "test_suite_result",
        "test_suite_log",
        "test_suite_completed",
        "script_job_completed",
        "script_job_state",
        "log_batch",
        "workspace_list_response",
        "workspace_read_response",
        "workspace_write_response",
        "workspace_delete_response",
        "workspace_mkdir_response",
    }
)
