URL ?= https://example.com

docker_build:
	docker build -t browser:latest -f docker/Dockerfile .
	docker build -t server:latest -f docker/Dockerfile.server .

docker_run:
	$(eval XAUTH_FILE := $(shell find /run/user/$$(id -u) -name '.mutter-Xwaylandauth*' 2>/dev/null | head -1))
	$(eval XAUTH_FILE := $(if $(XAUTH_FILE),$(XAUTH_FILE),$(HOME)/.Xauthority))
	@if [ "$$(uname)" = "Darwin" ]; then \
		docker run \
			--network="host" \
			-e DISPLAY=host.docker.internal:0 \
			-e LIBGL_ALWAYS_SOFTWARE=1 \
			-e XDG_RUNTIME_DIR=/tmp \
			-v $(PWD):/app/ \
			browser:latest \
			'$(URL)'; \
	else \
		docker run \
			--network="host" \
			--user $$(id -u):$$(id -g) \
			-e DISPLAY=$$DISPLAY \
			-e XDG_RUNTIME_DIR=$$XDG_RUNTIME_DIR \
			-e XAUTHORITY=/tmp/.Xauthority \
			-e HOME=/tmp \
			-e LIBGL_ALWAYS_SOFTWARE=1 \
			-v /tmp/.X11-unix:/tmp/.X11-unix \
			-v $(XAUTH_FILE):/tmp/.Xauthority:ro \
			-v $$XDG_RUNTIME_DIR:$$XDG_RUNTIME_DIR \
			-v $(PWD)/:/app/ \
			browser:latest \
			'$(URL)'; \
	fi


docker_run_server:
	@if [ "$$(uname)" = "Darwin" ]; then \
		docker run \
			-p 8000:8000 \
			-v $(PWD)/:/app/ \
			server:latest; \
	else \
		docker run \
			-p 8000:8000 \
			-v $(PWD)/:/app/ \
			--add-host=host.docker.internal:host-gateway \
			server:latest; \
	fi
