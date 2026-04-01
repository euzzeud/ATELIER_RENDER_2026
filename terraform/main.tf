resource "render_postgres" "db" {
  name   = "postgres-${var.github_actor}"
  plan   = "free"
  region = "frankfurt"
}

resource "render_web_service" "flask_app" {
  name   = "flask-render-iac-${var.github_actor}"
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
  }
}

resource "render_web_service" "adminer" {
  name   = "adminer-${var.github_actor}"
  plan   = "free"
  region = "frankfurt"

  runtime_source = {
    image = {
      image_url = "adminer"
    }
  }
}