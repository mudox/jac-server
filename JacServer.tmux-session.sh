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
# JacKit
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
tmux send-keys -t "${window}.1" "
vv -O ${window_name}.podspec Example/Podfile
"

#
# JacServer
#

root="${HOME}/Develop/Python/jacserver/"
window_name='JacServer'
window="${session_name}:${window_name}"
tmux new-window              \
  -a                         \
  -t "${session_name}:{end}" \
  -n "${window_name}"        \
  -c "${root}"               \
  -d
sleep 1
tmux send-keys -t "${window}" "
v python *.py
"

#
# Test
#

root="${HOME}/Library/Logs/JacKit"
window_name='Test'
window="${session_name}:${window_name}"
# .1 on the left side shows jacserver stdout
tmux new-window              \
  -a                         \
  -t "${session_name}:{end}" \
  -n "${window_name}"        \
  -c "${root}"               \
  -d                         \
  pipenv shell
# .2 at top right corner runs test.py
root="${HOME}/Develop/Python/jacserver/"
tmux split-window  \
  -t "${window}.1" \
  -h               \
  -l 60            \
  -c "${root}"     \
  pipenv shell

# .3 at botom right corner `tail -f` jacserver.py stderr
root="${HOME}/Library/Logs/JacKit"
tmux split-window  \
  -t "${window}.2" \
  -v               \
  -c "${root}"     \
  tail -f "${HOME}/Library/Logs/JacKit/jacserver.log"

tmux select-window -t "${session_name}:1.1"
echo "[${session_name}] started"
tmux list-window -t "${session_name}" -F ' - #W'
