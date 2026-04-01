terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = ">= 1.7.0"
    }
  }
}

resource "random_id" "suffix" {
  byte_length = 2
}

provider "render" {
  api_key  = var.render_api_key
  owner_id = var.render_owner_id
}

variable "github_actor" {
  description = "GitHub username"
  type        = string
}

resource "render_web_service" "flask_app" {
  name   = "flask-render-iac-${var.github_actor}-${random_id.suffix.hex}"
  plan   = "free"
  region = "frankfurt"

  runtime_source = {
    image = {
      image_url = var.image_url
      tag       = var.image_tag
    }
  }

  env_vars = {
    "ENV" = {
      value = "production"
    }

    "DB_CONNECTION_STRING" = {
      value = render_postgres.db.connection_info.external_connection_string
    }
  }
}

resource "render_web_service" "adminer" {
  name   = "adminer-${var.github_actor}-${random_id.suffix.hex}"
  plan   = "free"
  region = "frankfurt"

  runtime_source = {
    image = {
      image_url = "adminer"
    }
  }
}

resource "render_postgres" "db" {
  name   = "postgres-${var.github_actor}"
  plan   = "free"
  region = "frankfurt"
  version = "18"
}

resource "render_static_site" "react_frontend" {
  name   = "react-frontend-${var.github_actor}-${random_id.suffix.hex}"

  repo_url        = "https://github.com/euzzeud/ATELIER_RENDER_2026"
  branch          = "main"
  root_directory  = "frontend"
  build_command   = "npm run build"
  publish_path    = "build"
}
