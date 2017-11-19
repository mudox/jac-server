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
# JacKit window
#

root="${HOME}/Develop/Apple/Frameworks/JacKit/"
window_name='JacKit'
window="${session_name}:${window_name}"
tmux new-session                         \
  -s "${session_name}"                   \
  -n "${window_name}"                    \
  -x "$CLIENT_WIDTH" -y "$CLIENT_HEIGHT" \
  -c "${root}"                           \
  -d

#
# JacServer window
#

root="${HOME}/Develop/Python/jack-server/"
window_name='JacServer'
tmux new-window                 \
  -n "${window_name}"           \
  -a -t "${session_name}:{end}" \
  -c "${root}"                  \
  -d
sleep 1
tmux send-keys -t "${window}" "
v python *.py
"


tmux select-window -t "${session_name}:Editor"
