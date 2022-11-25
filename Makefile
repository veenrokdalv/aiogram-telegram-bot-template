_pybabel-extract:
	pybabel extract --input-dirs=. -o locales/bot.pot

_pybabel-init-locale:
	pybabel init -i locales/bot.pot -d locales -D bot -l en
	pybabel init -i locales/bot.pot -d locales -D bot -l ru

pybabel-compile:
	pybabel compile -d locales -D bot

pybabel-init:
	make _pybabel-extract
	make _pybabel-init-locale
