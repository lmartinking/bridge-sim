IMG_NAME := bridge-sim
NAMESPACE := bridge-sim


.PHONY: bridge-sim
bridge-sim: bridgesim
	podman build -t $(IMG_NAME) .


.PHONY: run
run:
	podman run --rm -p 8080:80 $(IMG_NAME)


.PHONY: pre-deploy
pre-deploy:
	kubectl create namespace $(NAMESPACE)


.PHONY: deploy
deploy:
	kubectl apply --validate=strict -f deployment.yaml -n $(NAMESPACE)
