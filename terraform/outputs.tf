output "flask_service_name" {
  value = render_web_service.flask_app.name
}

output "flask_url" {
  value = render_web_service.flask_app.url
}

output "adminer_service_name" {
  value = render_web_service.adminer.name
}

output "adminer_url" {
  value = render_web_service.adminer.url
}

output "postgres_name" {
  value = render_postgres.db.name
}

output "postgres_connection_string" {
  value = render_postgres.db.connection_string
  sensitive = true
}

output "react_frontend_name" {
  value = render_static_site.react_frontend.name
}

output "react_frontend_url" {
  value = render_static_site.react_frontend.url
}
