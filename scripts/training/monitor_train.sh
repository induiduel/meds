#!/bin/bash
# MedSoru Canlı Eğitim Terminal Monitörü
clear
echo -e "\033[1;36m====================================================================\033[0m"
echo -e "\033[1;32m      🏥 MEDSORU AI - RTX 4060 CANLI QLORA EĞİTİM MONİTÖRÜ 🏥      \033[0m"
echo -e "\033[1;36m====================================================================\033[0m"
echo -e "\033[1;33mLog Dosyası:\033[0m /home/indu/.gemini/antigravity/brain/67b7e289-541f-45a9-a023-0ec1ba6928c4/.system_generated/tasks/task-221.log"
echo -e "\033[1;33mDurdurmak İçin:\033[0m Ctrl + C"
echo -e "\033[1;36m--------------------------------------------------------------------\033[0m"
echo ""

# Canlı log takibi
tail -f -n 25 "/home/indu/.gemini/antigravity/brain/67b7e289-541f-45a9-a023-0ec1ba6928c4/.system_generated/tasks/task-221.log"
