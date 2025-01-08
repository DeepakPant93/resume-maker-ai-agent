# =============================
# Variable Documentation
# =============================

# PYPI_TOKEN: Authentication token for PyPI publishing
# Usage: make publish PYPI_TOKEN=your_pypi_token

# PACKAGE_NAME: Name of the Python package for dependency tree
# Usage: make print-dependency-tree PACKAGE_NAME=your_package_name


# =============================
# Project Configuration
# =============================
PROJECT_NAME = resume-maker-ai-agent
GITHUB_USERNAME = DeepakPant93
GITHUB_REPO = $(PROJECT_NAME)
PROJECT_SLUG = resume_maker_ai_agent
CLOUD_REGION = eastus
TAG = latest
IMAGE_NAME = deepak93p/$(PROJECT_SLUG)
RESOURCE_GROUP = $(PROJECT_NAME)-rg
APP_NAME = $(PROJECT_NAME)-app
APP_ENV_NAME = $(APP_NAME)-env
BUMP_TYPE = patch

# =============================
# Help (Default Target)
# =============================
.PHONY: help
help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

# =============================
# Installation and Setup
# =============================
.PHONY: bake-env
bake-env: clean-env ## Install the poetry environment and set up pre-commit hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install --all-extras
	@poetry run pre-commit install || true
	@max_retries=3; count=0; \
	while ! make lint; do \
		count=$$((count + 1)); \
		if [ $$count -ge $$max_retries ]; then \
			echo "Max retries reached. Exiting."; \
			exit 1; \
		fi; \
		echo "Retrying make lint ($$count/$$max_retries)..."; \
	done
	@poetry shell

.PHONY: clean-env
clean-env: ## Remove the poetry environment
	@echo "🚀 Removing virtual environment"
	@rm -rf .venv

.PHONY: reset-env
reset-env: clean-env bake-env ## Install the poetry environment and set up pre-commit hooks

.PHONY: init-repo
init-repo: ## Initialize git repository
	@echo "🚀 Initializing git repository"
	@git init
	@echo "🚀 Creating initial commit"
	@git add .
	@git commit -m "Initial commit"
	@echo "🚀 Adding remote repository"
	@git branch -M main
	@git remote add origin git@github.com:$(GITHUB_USERNAME)/$(GITHUB_REPO).git
	@echo "🚀 Pushing initial commit"
	@git push -u origin main


# =============================
# Code Quality and Testing
# =============================
.PHONY: lint
lint: ## Run code quality tools
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml'"
	@poetry check --lock
	@echo "🚀 Linting code with pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking with mypy"
	# @echo "🚀 Sorting imports with isort"
	# @poetry run isort resume_maker_ai_agent/
	# @echo "🚀 Linting code with Ruff"
	# @poetry run ruff format resume_maker_ai_agent/
	@poetry run mypy
	@echo "🚀 Checking for obsolete dependencies with deptry"
	@poetry run deptry .
	@echo "🚀 Checking for security vulnerabilities with bandit"
	@poetry run bandit -c pyproject.toml -r resume_maker_ai_agent/ -ll


.PHONY: test
test: ## Run tests with pytest
	@echo "🚀 Running tests with pytest"
	@poetry run pytest --cov --cov-config=pyproject.toml --cov-report=term-missing


# =============================
# Build and Release
# =============================
.PHONY: bake
bake: clean-bake ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean-bake
clean-bake: ## Clean build artifacts
	@rm -rf dist

.PHONY: bump
bump: ## Bump project version
	@echo "🚀 Bumping version"
	@poetry run bump-my-version bump $(BUMP_TYPE)

.PHONY: publish
publish: ## Publish a release to PyPI
	@echo "🚀 Publishing: Dry run"
	@poetry config pypi-token.pypi $(PYPI_TOKEN)
	@poetry publish --dry-run
	@echo "🚀 Publishing"
	@poetry publish

.PHONY: bake-and-publish
bake-and-publish: bake publish ## Build and publish to PyPI

.PHONY: update
update: ## Update project dependencies
	@echo "🚀 Updating project dependencies"
	@poetry update --all-extras
	@poetry run pre-commit install --overwrite
	@echo "Dependencies updated successfully"

# =============================
# Run and Documentation
# =============================
.PHONY: run
run: ## Run the project's main application
	@echo "🚀 Running the project"
	@poetry run streamlit run $(PROJECT_SLUG)/app2.py --server.port 7860

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@poetry run mkdocs serve

# =============================
# Docker
# =============================
.PHONY: bake-container
bake-container: ## Build Docker image
	@echo "🚀 Building Docker image"
	docker build -t $(IMAGE_NAME):$(TAG) -f Dockerfile .

.PHONY: container-push
container-push: ## Push Docker image to Docker Hub
	@echo "🚀 Pushing Docker image to Docker Hub"
	docker push $(IMAGE_NAME):$(TAG)

.PHONY: bake-container-and-push
bake-container-and-push: bake-container container-push ## Build and push Docker image to Docker Hub

.PHONY: clean-container
clean-container: ## Clean up Docker resources related to the app
	@echo "🚀 Deleting Docker image for app: $(IMAGE_NAME)"
	@docker images $(IMAGE_NAME) --format "{{.Repository}}:{{.Tag}}" | xargs -r docker rmi -f || echo "No image to delete"

	@echo "🚀 Deleting unused Docker volumes"
	@docker volume ls -qf dangling=true | xargs -r docker volume rm || echo "No unused volumes to delete"

	@echo "🚀 Deleting unused Docker networks"
	@docker network ls -q --filter "dangling=true" | xargs -r docker network rm || echo "No unused networks to delete"

	@echo "🚀 Cleaning up stopped containers"
	@docker ps -aq --filter "status=exited" | xargs -r docker rm || echo "No stopped containers to clean up"


# =============================
# Debug
# =============================

.PHONY: print-dependency-tree
print-dependency-tree: ## Print dependency tree
	@echo "Printing dependency tree..."
	@poetry run pipdeptree -p $(PACKAGE_NAME)


# =============================
# Cleanup
# =============================
.PHONY: teardown
teardown: clean-bake clean-container ## Clean up temporary files and directories and destroy the virtual environment, Docker image from your local machine
	@echo "🚀 Cleaning up temporary files and directories"
	@rm -rf .pytest_cache || true
	@rm -rf dist || true
	@rm -rf build || true
	@rm -rf htmlcov || true
	@rm -rf .venv || true
	@rm -rf .mypy_cache || true
	@rm -rf site || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@rm -rf .ruff_cache || true
	@echo "🚀 Clean up completed."

.PHONY: teardown-all
teardown-all: teardown ## Clean up temporary files and directories and destroy the virtual environment, Docker image, and Cloud resources
