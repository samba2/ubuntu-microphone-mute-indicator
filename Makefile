SCRIPT_TARGET_DIR=${HOME}/.local/share/microphone-mute-indicator
LAUNCHER_TARGET_DIR=${HOME}/.local/share/applications
DESKTOP_FILE=microphone-mute-indicator.desktop

install:
	mkdir -p ${SCRIPT_TARGET_DIR}
	cp ./microphone-mute-indicator.py ${SCRIPT_TARGET_DIR}
	cp ./microphone-disabled-symbolic.svg ${SCRIPT_TARGET_DIR}
	mkdir -p ${LAUNCHER_TARGET_DIR}
	cat ${DESKTOP_FILE} | envsubst > ${LAUNCHER_TARGET_DIR}/${DESKTOP_FILE}
	@echo "\nDone installing\n"

uninstall:
	rm -rvf ${SCRIPT_TARGET_DIR}
	rm -vf ${LAUNCHER_TARGET_DIR}/${DESKTOP_FILE}