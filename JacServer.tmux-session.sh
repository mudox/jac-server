#!/usr/bin/env bash
# vim: fdm=marker

CLIENT_WIDTH=213
CLIENT_HEIGHT=57

session_name='JacKit'
if tmux has-session -t ${session_name} &>/dev/null; then
  echo "session [${session_name}] already exisits, kill it!"
  tmux kill-session -t "${session_name}"
fi


#
# Editor
#

root="${HOME}/Develop/Python/jack-server/"
window_name='Editor'
window="${session_name}:${window_name}"
tmux new-session       \
  -s "${session_name}" \
  -n "${window_name}"  \
  -x "$CLIENT_WIDTH"   \
  -y "$CLIENT_HEIGHT"  \
  -c "${root}"         \
  -d

#
# Log
#

root="${HOME}/Git/vim-config"
window_name='Log'
window="${session_name}:${window_name}"
tmux new-window -a -d        \
  -t "${session_name}:{end}" \
  -n "${window_name}"        \
  -c "${root}"
sleep 1
tmux send-keys -t "${window}" "
vv vimrc
"

tmux select-window -t "${session_name}:Editor"
