main = {
    "authorized_users": [
        3406106054
    ],
    "bot": {
        "token": "xxx",
        "interaction_prefix": "#"
    },
    "debug": False,
    "mc": {
        "default_port": 8086,
        "server_list": {
            "test": {
                "port": 8087
            }
        }
    }
}

messages = {
    "get_cur_server": "当前频道链接的 MC 服务器为: {}",
    "set_cur_server": "将当前频道链接的 MC 服务器设置为 {}",
    "set_cur_server_failed": "设置当前频道的 MC 服务器失败，可能是该配置不存在。",
    "del_cur_server": "将当前频道链接的 MC 服务器设置为默认服务器",
    "on_cmd_error": "命令执行过程中遇到了未知异常，请查看日志以获取关于此错误的信息",
    "server_cmd_success": "指令执行成功",
    "server_cmd_auth_success": "服务器指令授权成功",
    "server_cmd_auth_needs_at": "该指令需要@人才能生效",
    "pat": {
        "successful_pat": "你成功地{0}{1}",
        "successful_tell": "消息已成功发送至 {1}",
        "player_is_offline": "{1} 当前并未上线或从未登录过服务器哦"
    },
    "world_names": {
        "mcg_gensokyo": "幻想乡",
        "mcg_nether": "旧地狱",
        "mcg_meikai": "冥界",
        "mcg_truemoon": "月都",
    }
}

images = {
    "tps": {
        "normal": "./images/good_tps.png",
        "potato": "./images/potato.png",
        "baked_potato": "./images/potato_baked.png"
    }
}