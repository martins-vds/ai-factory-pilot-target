TAILWINDCSS_VERSION ?= v4.3.3
export TAILWINDCSS_VERSION

.PHONY: tailwind-install tailwind-build tailwind-watch

tailwind-install:
	tailwindcss_install

tailwind-build:
	tailwindcss -i assets/css/input.css -o assets/css/tailwind.css --minify

tailwind-watch:
	tailwindcss -i assets/css/input.css -o assets/css/tailwind.css --watch
