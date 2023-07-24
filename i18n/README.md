# controllers
xgettext -k_ -o i18n/controllers.pot backend/app/controllers/*.py
# for init
msginit -l i18n/zh_controllers -i i18n/controllers.pot
msginit -l i18n/en_controllers -i i18n/controllers.pot
# for update
msgmerge -U i18n/zh_controllers.po i18n/controllers.pot
msgmerge -U i18n/en_controllers.po i18n/controllers.pot
# gen po
msgfmt -o i18n/zh/LC_MESSAGES/controllers.mo i18n/zh_controllers.po
msgfmt -o i18n/en/LC_MESSAGES/controllers.mo i18n/en_controllers.po


# frontend
xgettext -k_ -o i18n/frontend.pot backend/app/pkgs/tools/i18b.py
# for init
msginit -l i18n/zh_frontend -i i18n/frontend.pot
msginit -l i18n/en_frontend -i i18n/frontend.pot
# for update
msgmerge -U i18n/zh_frontend.po i18n/frontend.pot
msgmerge -U i18n/en_frontend.po i18n/frontend.pot
# gen po
msgfmt -o i18n/zh/LC_MESSAGES/frontend.mo i18n/zh_frontend.po
msgfmt -o i18n/en/LC_MESSAGES/frontend.mo i18n/en_frontend.po

# prompt
xgettext -k_ -o i18n/prompt.pot backend/app/pkgs/prompt/*.py
# for init
msginit -l i18n/zh_prompt -i i18n/prompt.pot
msginit -l i18n/en_prompt -i i18n/prompt.pot
# for update
msgmerge -U i18n/zh_prompt.po i18n/prompt.pot
msgmerge -U i18n/en_prompt.po i18n/prompt.pot
# gen po
msgfmt -o i18n/zh/LC_MESSAGES/prompt.mo i18n/zh_prompt.po
msgfmt -o i18n/en/LC_MESSAGES/prompt.mo i18n/en_prompt.po