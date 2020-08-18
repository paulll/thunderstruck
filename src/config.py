import os

chat_id = -1001358764091
channel_id = -1001359662376

do_forward_messages = True
do_remove_reposts = True
banlist_path = "/tmp/banned.json"
state_path = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/state.json"
)
