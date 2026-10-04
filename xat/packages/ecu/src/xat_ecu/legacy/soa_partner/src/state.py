
class CAN_CONSTANT:
    send_can_begin = False
    get_wanted_can = False


class UPSTREAM:
    get_method_response = False
    socket_can_dist = {}
    mode = 'normal'
    check_count = 13  # 结果比对方法比对的次数，由20修改为13
    check_interval = 0.3  # 2次结果比对之间的时间间隔
    partner_main_wait_second = 5  # partner主线程等待的秒数，由7修改为5
    method_loop_count = 13   # 上行方法执行的次数，由20修改为13
    method_loop_interval = 0.3  # 上行方法两次之间的间隔秒数


class DOWNSTREAM:
    real_value_list = []


class CASE_RUN:
    iter_num = 0
    count_group = 30
    set_finished = False
    can_sender_list = []
    pre_condition_method = False
    real_result = ""
    pdu_send_log_get_flag = False
    bgm_version = "6160110110"
    current_service = ""
    send_signal_of_last_case = []
