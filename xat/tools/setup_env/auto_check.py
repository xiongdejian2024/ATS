import os

if __name__ == "__main__":
    if not os.path.exists("/root/autorun"):
        os.makedirs("/root/autorun")
        res = os.system('cd /root/monitor/agent/ && chmod 777 auto_check.sh && sh auto_check.sh')
        if res != 0:
            raise SystemExit('自动部署失败')
        else:
            print("自动SAT部署成功")
    else:
        print("已部署，无需重复部署")

    res = os.system('cd /root/autorun/sat/xat_cases/legacy/bgm/ && source ../../venv/bin/activate '
                    '&& pytest -s bgm_tools/test_check_prenv.py')
    if res != 0:
        raise SystemExit('环境检查执行成功')
    else:
        print("环境检查执行失败")
